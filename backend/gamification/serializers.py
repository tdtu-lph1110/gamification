from rest_framework import serializers
from .models import User, Rank, Item, Quest, UserQuest, UserItem

class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = '__all__'

class UserQuestSerializer(serializers.ModelSerializer):
    quest_title = serializers.ReadOnlyField(source='quest.title')

    class Meta:
        model = UserQuest
        fields = ['quest', 'quest_title', 'status', 'completed_at', 'last_submitted_code']

class UserSerializer(serializers.ModelSerializer):
    current_rank = RankSerializer(read_only=True) # Hiện chi tiết rank thay vì chỉ hiện ID
    quest_progress = UserQuestSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'total_xp', 'currency', 
            'current_rank', 'current_streak', 'quest_progress'
        ]

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = '__all__'
