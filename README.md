# database partitioning

## 파티셔닝

테이블의 데이터를 일정 기준에 따라 나누는 기법으로 성능 향상과 관리 편의성 증대가 가능, 시간(날짜) 또는 용량에 따라 자동으로 테이블을 나누는 방법이 일반적

### 예시

> postgresql

```sql
CREATE TABLE user_activity (
    user_id INT,
    action TEXT,
    created_at TIMESTAMP NOT NULL
) PARTITION BY RANGE (created_at);

-- 2024년 1월 데이터를 위한 파티션
CREATE TABLE user_activity_2024_01 PARTITION OF user_activity
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- 2024년 2월 데이터를 위한 파티션
CREATE TABLE user_activity_2024_02 PARTITION OF user_activity
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

위와 같이 postgresql에 **Range Partitioning**을 사용하여 파티셔닝이 가능

> django

```python
# models.py
from django.db import models

class UserActivity(models.Model):
    user_id = models.IntegerField()
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 기본 테이블은 여전히 존재하지만, 파티션 테이블에서 실제 데이터를 처리함
        db_table = 'user_activity'
```

위와 같이 작성하면 django에서 보낸 데이터가 postgresql에서 자동으로 처리
