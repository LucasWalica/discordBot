from django.urls import path 
from .views import DiscordUserCreate, DiscordUserDetailView, DiscordUserAddLvlOnMessage

urlpatterns = [
    path('users/create/', DiscordUserCreate.as_view()),
    path('users/<str:discord_id>/', DiscordUserDetailView.as_view()),
    path('users/<str:discord_id>/message/', DiscordUserAddLvlOnMessage.as_view())
]
