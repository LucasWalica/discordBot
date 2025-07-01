from django.urls import path 
from .views import DiscordUserCreate, DiscordUserDetailView, DiscordUserAddLvlOnMessage, DiscordUserBan

urlpatterns = [
    path('users/create/', DiscordUserCreate.as_view()),
    path('users/<str:discord_id>/', DiscordUserDetailView.as_view()),
    path('users/<str:discord_id>/message/', DiscordUserAddLvlOnMessage.as_view()),
    path('users/<str:discord_id>/ban/', DiscordUserBan.as_view())
]
