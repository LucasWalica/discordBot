import os 
from discord.ext import commands 
from dotenv import load_dotenv
import discord 

from utils import createUser, userSendingMessage, getUserData
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
intents = discord.Intents.default()
intents.message_content = True 
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)



@bot.command()
async def helpMe(ctx):
    await ctx.send(
        "---------- Panel de ayuda del bot ----------\n"
        "!voiceChannel _capacidad_ (número) _nombre_ (texto)\n"
        "!lvl para ver tu nivel"
    )


@bot.command()
async def voiceChannel(ctx, capacity: int = 10, *, channel_name: str = "Nuevo Canal de Voz"):
    # Verificar si el autor tiene permisos para gestionar canales
    if ctx.author.guild_permissions.manage_channels:
        guild = ctx.guild  # Obtén el servidor actual

        # Crear el canal de voz con el nombre dado
        new_channel = await guild.create_voice_channel(
            channel_name, user_limit=capacity
        )
        
        # Informar que el canal fue creado
        await ctx.send(f"Se ha creado un canal de voz llamado '{new_channel.name}' con capacidad para {capacity} usuarios.")
    else:
        await ctx.send("No tienes permisos suficientes para crear un canal de voz.")

@bot.event
async def on_voice_state_update(member, before, after):
    # Verificar si el miembro dejó el canal de voz
    if before.channel != after.channel:  # El miembro cambió de canal
        if before.channel is not None and len(before.channel.members) == 0:  # Si el canal está vacío
            # Eliminar el canal vacío
            await before.channel.delete()
            print(f"Canal de voz '{before.channel.name}' eliminado porque está vacío.")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command()
async def lvl(ctx):
    data = getUserData(ctx.author)  # Llama a la función correctamente
    if data:
        puntos = data.get("points", 0)
        await ctx.send(f"💪 {ctx.author.name}, tienes {puntos} puntos!")
    else:
        await ctx.send(f"❌ {ctx.author.name}, no te encontré en la base de datos.")
    


@bot.event
async def on_message(message):
    if message.author.bot:
        return  # evitar que los bots se registren a sí mismos
    
    user_data = getUserData(message.author)

    if user_data:
        puntos = user_data.get("points", 0)

        if puntos >= 200:
            vip_role = discord.utils.get(message.guild.roles, name="VIP")
            if vip_role:
                if vip_role not in message.author.roles:
                    await message.author.add_roles(vip_role)
                    await message.channel.send(
                        f"Felicidades {message.author.mention}, ahora eres VIP! 💎"
                    )

    await userSendingMessage(message.author)
    await bot.process_commands(message)  # importante para que !ping, !lvl funcionen

@bot.event
async def on_member_join(member):
    await createUser(member)
    rol = discord.utils.get(member.guild.roles, name="Miembro")
    if rol:
        await member.add_roles(rol)
    channel = discord.utils.get(member.guild.text_channels, name="general")  # Cambia 'general' por el nombre real

    if channel:
        await channel.send(f"👋 Bienvenido {member.mention} al servidor!")




@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    
    for guild in bot.guilds:  # Recorre cada servidor donde esté el bot
        print(f"🔍 Sincronizando usuarios del servidor: {guild.name}")
        for member in guild.members:
            if member.bot:
                continue  # Saltar bots, solo usuarios reales
            
            try:
               await createUser(member)
            except Exception as e:
                print(f"💥 Error conectando con Django para {member.name}: {e}")


bot.run(TOKEN)