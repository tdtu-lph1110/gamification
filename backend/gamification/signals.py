from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Rank, PointLog

@receiver(post_save, sender=User)
def check_user_rank_upgrade(sender, instance, created, **kwargs):
    """
    Tự động kiểm tra và cập nhật Rank khi User được lưu (có thay đổi XP).
    """
    if created:
        return # Bỏ qua lúc mới tạo user

    # Lấy Rank cao nhất mà user đủ điểm đạt được
    # Logic: Lấy tất cả rank có min_xp <= user.total_xp, sắp xếp giảm dần, lấy cái đầu tiên
    eligible_rank = Rank.objects.filter(min_xp__lte=instance.total_xp).order_by('-min_xp').first()

    if eligible_rank and instance.current_rank != eligible_rank:
        old_rank = instance.current_rank
        instance.current_rank = eligible_rank
        # Quan trọng: Dùng update() để tránh vòng lặp vô hạn (recursion) nếu gọi save()
        User.objects.filter(id=instance.id).update(current_rank=eligible_rank)
        
        # Ghi log sự kiện thăng hạng
        PointLog.objects.create(
            user=instance,
            action_type='BONUS',
            xp_change=0,
            currency_change=0, # Có thể thưởng tiền khi lên cấp ở đây
            description=f"Thăng hạng từ {old_rank} lên {eligible_rank}"
        )