from rest_framework import serializers
from .models import DiscordUser

class DiscordUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscordUser
        fields = ['discord_id', 'username', 'discriminator','points','is_banned']