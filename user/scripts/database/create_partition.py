import datetime

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Create partitions automatically"

    def handle(self, *args, **kwargs):
        now = datetime.datetime.now()
        next_month = (now.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)

        table_name = f"user_activity_{next_month.year}_{next_month.month:02d}"

        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table_name} PARTITION OF user_activity
                FOR VALUES FROM ('{next_month.year}-{next_month.month:02d}-01')
                TO ('{next_month.year}-{next_month.month + 1:02d}-01');
                """
            )

        self.stdout.write(self.style.SUCCESS(f"Partition {table_name} created successfully."))
