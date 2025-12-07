from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Rank, Item, Quest, UserQuest, UserItem, PointLog
from .serializers import UserSerializer, RankSerializer, ItemSerializer, QuestSerializer
from djoser.views import TokenCreateView, TokenDestroyView
from django.conf import settings

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API để lấy thông tin User. 
    Chỉ cho phép đọc (ReadOnly) vì việc cộng điểm phải qua API riêng bảo mật hơn.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_class = [permissions.IsAuthenticated] # Bật dòng này khi đã ghép login

class RankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rank.objects.all().order_by('tier')
    serializer_class = RankSerializer
    # Cho phép tất cả mọi người (kể cả chưa login) đều xem được
    permission_classes = [permissions.AllowAny]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    # API: POST /api/items/{id}/buy/
    @action(detail=True, methods=['post'])
    def buy(self, request, pk=None):
        item = self.get_object()
        user = User.objects.get(pk=request.data.get('user_id')) # Tạm thời lấy ID từ body (sau này lấy từ Token)

        # 1. Kiểm tra tiền 
        if user.currency < item.price:
            return Response({"error": "Nhà ngươi không đủ Quan Tiền!"}, status=400)

        # 2. Thực hiện giao dịch 
        with transaction.atomic():
            # Trừ tiền
            user.currency -= item.price
            user.save()

            # Thêm vào kho (Inventory)
            user_item, created = UserItem.objects.get_or_create(user=user, item=item)
            if not created:
                user_item.quantity += 1 # Nếu có rồi thì tăng số lượng
                user_item.save()

            # Ghi vào Sổ Công Đức 
            PointLog.objects.create(
                user=user,
                action_type='SHOP',
                currency_change=-item.price,
                description=f"Mua vật phẩm: {item.name}"
            )

        return Response({"status": "Giao dịch thành công", "new_balance": user.currency})

class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer 

    # API: POST /api/quests/{id}/submit/
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        quest = self.get_object()
        user = User.objects.get(pk=request.data.get('user_id'))
        code_submitted = request.data.get('code', '')

        # --- MOCK LOGIC (Giả lập Sandbox) ---
        # Quy ước: Nếu code có chữ "print", coi như đúng. Ngược lại là sai.
        is_correct = "print" in code_submitted 
        # ------------------------------------

        if is_correct:
            # Cộng thưởng (Signal sẽ tự động kích hoạt để check thăng hạng)
            user.total_xp += quest.xp_reward
            user.currency += quest.currency_reward
            user.save()

            # Lưu tiến độ
            UserQuest.objects.update_or_create(
                user=user, quest=quest,
                defaults={'status': 'COMPLETED', 'last_submitted_code': code_submitted}
            )
            
            # Ghi Log
            PointLog.objects.create(
                user=user, action_type='QUEST',
                xp_change=quest.xp_reward, currency_change=quest.currency_reward,
                description=f"Hoàn thành nhiệm vụ: {quest.title}"
            )

            return Response({"result": "Passed", "message": "Chúc mừng! Đỗ đạt!"})
        else:
            return Response({"result": "Failed", "message": "Code lỗi rồi, về ôn lại kinh sử đi!"})
        
class CustomTokenCreateView(TokenCreateView):
    def _action(self, serializer):
        # Gọi logic login gốc của Djoser để lấy token
        response = super()._action(serializer)
        token_string = response.data['auth_token']
        
        # Gắn Token vào HttpOnly Cookie
        response.set_cookie(
            key='auth_token',
            value=token_string,
            httponly=True,   # JS không đọc được (Chống XSS)
            samesite='Lax',  # Chống CSRF cơ bản
            secure=False,    # Đặt True nếu chạy Production (HTTPS)
            max_age=60*60*24*7 # Cookie sống 7 ngày
        )
        
        del response.data['auth_token'] 
        
        return response

class CustomTokenDestroyView(TokenDestroyView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Xóa cookie khi user đăng xuất
        response.delete_cookie('auth_token')
        return response