from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RankViewSet, ItemViewSet, QuestViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'ranks', RankViewSet)
router.register(r'items', ItemViewSet)
router.register(r'quests', QuestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]