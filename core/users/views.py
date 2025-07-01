from django.shortcuts import render
from .models import DiscordUser
from rest_framework import generics
from rest_framework.parsers import JSONParser
from .serializers import DiscordUserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

# Create your views here.

class DiscordUserCreate(generics.CreateAPIView):
    parser_classes = [JSONParser]
    queryset = DiscordUser.objects.all()
    serializer_class = DiscordUserSerializer

    def create(self, request, *args, **kwargs):
        discord_id = request.data.get('discord_id')

        if not discord_id:
            return Response({"error": "No se proporcionó discord_id"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = DiscordUser.objects.get_or_create(
            discord_id=discord_id,
            defaults={
                'username': request.data.get('username'),
                'discriminator': request.data.get('discriminator')
            }
        )

        serializer = self.get_serializer(user)

        if created:
            return Response(
                {"status": "created", "user": serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"status": "exists", "user": serializer.data},
                status=status.HTTP_200_OK
            )

class DiscordUserDetailView(generics.RetrieveAPIView):
    parser_classes = [JSONParser]
    queryset = DiscordUser.objects.all()
    serializer_class = DiscordUserSerializer
    lookup_field = 'discord_id'



class DiscordUserAddLvlOnMessage(generics.UpdateAPIView):
    parser_classes = [JSONParser]
    queryset = DiscordUser.objects.all()
    serializer_class = DiscordUserSerializer
    lookup_field = 'discord_id'

    def update(self, request, *args, **kwargs):
        discord_id = self.kwargs['discord_id']
        user = get_object_or_404(DiscordUser, discord_id=discord_id)
        user.points += 10
        user.save()
        return Response({'status': 'ok', 'new_points': user.points})
    


class DiscordUserBan(generics.UpdateAPIView):
    parser_classes = [JSONParser]
    queryset = DiscordUser.objects.all()
    serializer_class = DiscordUserSerializer
    lookup_field = 'discord_id'

    def update(self, request, *args, **kwargs):
        discord_id = self.kwargs['discord_id']
        user = get_object_or_404(DiscordUser, discord_id=discord_id)
        if user.banned_lvl<=4:
            user.banned_lvl+=1
            if user.banned_lvl==5:
                user.ban_start_time = datetime.now()
            user.save()
        return Response({"user_banned_lvl":f"{user.banned_lvl}"})