from django.db import models

# Create your models here.
class DiscordUser(models.Model):
    discord_id = models.CharField(max_length=20, unique=True)  # ID único de Discord
    username = models.CharField(max_length=100)  # Nombre de usuario
    discriminator = models.CharField(max_length=5)  # Discriminador (lo que sigue después del # en Discord)
    points = models.IntegerField(default=0)  # Puntos (puedes agregar lo que quieras)
    is_banned = models.BooleanField(default=False)  # Estado de baneo

    def __str__(self):
        return self.username
    


