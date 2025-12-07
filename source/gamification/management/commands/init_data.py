from django.core.management.base import BaseCommand
from gamification.models import Rank, Item, Quest

class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho game Khoa Cử'

    def handle(self, *args, **kwargs):
        # 1. Tạo Hệ thống Rank (Dựa trên tài liệu yêu cầu)
        ranks = [
            (0, "Bạch Đinh", 0),          # Level 0
            (1, "Nho Sinh", 100),         # Cần 100 XP
            (2, "Tú Tài", 500),           # Cần 500 XP
            (3, "Cử Nhân", 1500),         # Cần 1500 XP
            (4, "Tiến Sĩ", 5000),         # Cần 5000 XP
            (5, "Trạng Nguyên", 10000),   # Max Level
        ]
        
        for tier, name, min_xp in ranks:
            Rank.objects.update_or_create(tier=tier, defaults={'name': name, 'min_xp': min_xp})
        
        self.stdout.write(self.style.SUCCESS('Đã tạo xong hệ thống Quan Phẩm!'))

        # 2. Tạo Vật phẩm mẫu (Item)
        items = [
            ("Bút Lông", "ITEM", 50, "COSMETIC"),       # Giá 50
            ("Mũ Cánh Chuồn", "HAT", 200, "COSMETIC"),  # Giá 200
            ("Phao Thi", "HINT", 20, "POWERUP"),        # Giá 20 (Dùng 1 lần)
        ]
        
        for name, code, price, itype in items:
            Item.objects.update_or_create(
                name=name, 
                defaults={'price': price, 'item_type': itype, 'attributes': {'code': code}}
            )

        self.stdout.write(self.style.SUCCESS('Đã nhập hàng về Kho Vật Phẩm!'))

        # -----------------------------------------------------------
        # 3. Tạo Nhiệm vụ mẫu (Quest) - PHẦN MỚI THÊM
        # -----------------------------------------------------------
        quests = [
            {
                "title": "Khai bút đầu xuân",
                "description": "Nhiệm vụ nhập môn: Hãy viết chương trình in ra dòng chữ 'Hello World' để chào hỏi quan giám khảo.",
                "xp_reward": 50,
                "currency_reward": 10,
                "validation_data": {"input": "", "output": "Hello World"}
            },
            {
                "title": "Phép tính lương thảo",
                "description": "Giúp thủ kho tính toán: Hãy in ra kết quả của phép tính 15 + 25.",
                "xp_reward": 100,
                "currency_reward": 20,
                "validation_data": {"input": "", "output": "40"}
            },
            {
                "title": "Điểm danh binh sĩ",
                "description": "Sử dụng vòng lặp (loop) để in ra các số từ 0 đến 4, mỗi số một dòng.",
                "xp_reward": 150,
                "currency_reward": 30,
                "validation_data": {"input": "", "output": "0\n1\n2\n3\n4"}
            }
        ]

        for q in quests:
            Quest.objects.update_or_create(
                title=q["title"],
                defaults={
                    "description": q["description"],
                    "xp_reward": q["xp_reward"],
                    "currency_reward": q["currency_reward"],
                    "validation_data": q["validation_data"]
                }
            )

        self.stdout.write(self.style.SUCCESS('✅ Đã niêm yết Đề Thi (Quest) lên bảng vàng!'))