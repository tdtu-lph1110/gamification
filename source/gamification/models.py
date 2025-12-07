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

# 4. Bảng Items (Vật phẩm trong cửa hàng)
class Item(models.Model):
    class ItemType(models.TextChoices):
        COSMETIC = 'COSMETIC', 'Trang trí'
        POWERUP = 'POWERUP', 'Vật phẩm chức năng'

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    item_type = models.CharField(max_length=20, choices=ItemType.choices)
    price = models.PositiveIntegerField(default=0) # Giá mua bằng Currency
    image_url = models.URLField(max_length=500, blank=True, null=True)
    
    # Thuộc tính game (JSON): VD {"bonus_xp": 10, "durability": 5}
    attributes = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name

# 5. Bảng UserItems (Hành trang - Inventory)
# Quan hệ N-N: Một User có nhiều Item, Một Item có thể thuộc về nhiều User
class UserItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField(default=1)
    is_equipped = models.BooleanField(default=False) # Đang mặc/sử dụng hay không
    acquired_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item') # Một người không nên có 2 dòng cho cùng 1 item (thay vào đó tăng quantity)

# 6. Bảng Quests (Nhiệm vụ / Bài tập)
class Quest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Phần thưởng
    xp_reward = models.PositiveIntegerField(default=10)
    currency_reward = models.PositiveIntegerField(default=5)
    
    # Logic kiểm tra code (quan trọng cho phần Sandbox sau này)
    # Ví dụ: test_case_input, expected_output
    validation_data = models.JSONField(default=dict, blank=True) 

    def __str__(self):
        return self.title

# 7. Bảng UserQuest (Tiến độ làm bài)
class UserQuest(models.Model):
    class Status(models.TextChoices):
        TODO = 'TODO', 'Chưa làm'
        IN_PROGRESS = 'IN_PROGRESS', 'Đang làm'
        COMPLETED = 'COMPLETED', 'Hoàn thành'
        FAILED = 'FAILED', 'Thất bại'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quest_progress')
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    
    # Lưu code người dùng đã nộp lần cuối
    last_submitted_code = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'quest')









