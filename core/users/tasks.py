from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import DiscordUser

@shared_task
def check_ban_times():
    ahora = timezone.now()
    niveles = {
        1: timedelta(minutes=10),
        2: timedelta(minutes=30),
        3: timedelta(days=1),
        4: timedelta(weeks=1),
        5: timedelta(days=30),
    }

    usuarios = DiscordUser.objects.filter(banned_lvl__gt=0)

    desbaneados = 0
    for user in usuarios:
        tiempo_castigo = niveles.get(user.banned_lvl)
        if user.ban_start_time and ahora >= user.ban_start_time + tiempo_castigo:
            user.banned_lvl = 0
            user.ban_start_time = None
            user.save()
            desbaneados += 1

    return f"{desbaneados} usuarios desbaneados."
