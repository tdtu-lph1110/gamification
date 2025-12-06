from django.contrib import admin
from .models import User, Rank, PointLog

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'total_xp', 'current_rank', 'currency')

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('tier', 'name', 'min_xp')

@admin.register(PointLog)
class PointLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'xp_change', 'created_at')