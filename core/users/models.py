from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class DiscordUser(models.Model):
    discord_id = models.CharField(max_length=20, unique=True)  # ID único de Discord
    username = models.CharField(max_length=100)  # Nombre de usuario
    discriminator = models.CharField(max_length=5)  # Discriminador (lo que sigue después del # en Discord)
    points = models.IntegerField(default=0)  # Puntos (puedes agregar lo que quieras)
    banned_lvl = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])  # Estado de baneo
    ban_start_time = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.username
    


