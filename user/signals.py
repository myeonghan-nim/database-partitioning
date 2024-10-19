import datetime

from django.db import connection
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import UserActivity


# 임시로 테스트를 위해 분 단위로 파티션을 생성하는 시그널
@receiver(pre_save, sender=UserActivity)
def create_partition_if_needed(sender, instance, **kwargs):
    # created_at 필드가 없으면 현재 시간을 사용
    if not instance.created_at:
        instance.created_at = datetime.datetime.now()

    # 파티션 테이블 이름을 'user_activity_YYYYMMDD_HHMM' 형식으로 설정
    partition_name = instance.created_at.strftime("user_activity_%Y%m%d_%H%M")

    # 파티션 테이블이 존재하는지 확인하는 SQL
    check_partition_query = f"""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = '{partition_name}'
        );
    """

    with connection.cursor() as cursor:
        cursor.execute(check_partition_query)
        partition_exists = cursor.fetchone()[0]

        # 파티션이 없으면 새로 생성
        if not partition_exists:
            # 파티션 생성 SQL
            create_partition_query = f"""
                CREATE TABLE IF NOT EXISTS {partition_name} PARTITION OF user_activity
                FOR VALUES FROM ('{instance.created_at.strftime('%Y-%m-%d %H:%M:00')}')
                TO ('{(instance.created_at + datetime.timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:00')}');
            """
            cursor.execute(create_partition_query)
