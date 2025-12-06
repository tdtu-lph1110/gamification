import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField 

# 1. Bảng Ranks (Phẩm Hàm)
class Rank(models.Model):
    name = models.CharField(max_length=50, unique=True) # Tú Tài, Cử Nhân
    tier = models.PositiveIntegerField(unique=True)     # 1, 2, 3
    min_xp = models.BigIntegerField()
    
    # Metadata lưu JSON (Màu sắc, Icon, Khung avatar...)
    # Ví dụ: {"color": "#FF0000", "icon_url": "..."}
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['tier']
        # Constraint: Đảm bảo tier không âm (dù PositiveInt đã lo, nhưng thêm DB constraint cho chắc)
        constraints = [
            models.CheckConstraint(check=models.Q(tier__gte=0), name='rank_tier_non_negative'),
            models.CheckConstraint(check=models.Q(min_xp__gte=0), name='rank_xp_non_negative'),
        ]

    def __str__(self):
        return f"{self.tier} - {self.name}"

# 2. Bảng Users (Sĩ Tử)
class User(AbstractUser):
    # Dùng UUID làm ID thay vì số tự tăng (An toàn hơn)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Các chỉ số Game
    total_xp = models.BigIntegerField(default=0, db_index=True) # Index giúp query Leaderboard nhanh
    currency = models.BigIntegerField(default=0)
    
    # Quan hệ với Rank
    current_rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Streak
    current_streak = models.IntegerField(default=0)
    last_activity_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            # Constraint: Đảm bảo tiền không bao giờ âm
            models.CheckConstraint(check=models.Q(currency__gte=0), name='currency_non_negative'),
        ]

# 3. Bảng PointLogs (Sổ Công Đức - Lịch sử)
class PointLog(models.Model):
    # Các loại hành động (Enum)
    class ActionType(models.TextChoices):
        DAILY_LOGIN = 'LOGIN', 'Đăng nhập'
        QUEST = 'QUEST', 'Nhiệm vụ'
        BONUS = 'BONUS', 'Thưởng'
        PENALTY = 'PENALTY', 'Phạt'
        SHOP = 'SHOP', 'Mua sắm'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')
    xp_change = models.IntegerField(default=0)
    currency_change = models.IntegerField(default=0)
    
    action_type = models.CharField(max_length=20, choices=ActionType.choices)
    description = models.TextField()
    
    # Lưu thêm dữ liệu phụ (VD: ID bài tập, ID item đã mua) vào JSON
    extra_data = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Index user và thời gian để sau này query lịch sử của 1 người cho nhanh
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]