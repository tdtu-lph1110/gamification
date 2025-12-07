from rest_framework.authentication import TokenAuthentication

class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # 1. Thử lấy token từ Cookie trước
        token = request.COOKIES.get('auth_token')
        if token:
            return self.authenticate_credentials(token)
        
        # 2. Nếu không có cookie, thử lấy từ Header như cũ (Fallback)
        return super().authenticate(request)