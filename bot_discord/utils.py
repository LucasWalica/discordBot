from config import API_URL
import requests
import aiohttp
from transformers import pipeline


#analizador de sentimientos 
analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

#file that calls django api
async def createUser(member):
    data = {
        "discord_id": str(member.id),
        "username": member.name,
        "discriminator": member.discriminator
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post("http://web:8000/users/create/", json=data) as response:
            if response.status == 201:  # CreateAPIView responde con 201 si todo salió bien
                print(f"Usuario {member.name}#{member.discriminator} creado en la base de datos.")
            else:
                print(f"Error al registrar usuario: {await response.json()}")


async def userSendingMessage(member):
    data = {
        "discord_id": str(member.id),
        "username": member.name,
        "discriminator": member.discriminator
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(f"http://web:8000/users/{member.id}/message/", json=data) as response:
            if response.status == 200:  # CreateAPIView responde con 201 si todo salió bien
                print(f"Usuario {member.name}#{member.discriminator} creado en la base de datos.")
            else:
                print(f"Error al registrar usuario: {response.json()}")


def getUserData(member):
    data = {
        "discord_id": str(member.id),
        "username": member.name,
        "discriminator": member.discriminator
    }
    response = requests.get(f"http://web:8000/users/{member.id}/")
    if response.status_code == 200:
        return response.json()  # <-- devuelve los datos del usuario
    else:
        return None
    

async def checkMessageContent(member, message):
    result = analyzer(message.content)[0]
    if result['label'] == "1 star":
        banned_lvl = await banUser(member)
        return banned_lvl



async def banUser(member):
    data = {
        "discord_id": str(member.id),
        "username": member.name,
        "discriminator": member.discriminator
    }

    async with aiohttp.ClientSession() as session:
        async with session.put(f"http://web:8000/users/{member.id}/ban/", json=data) as response:
            if response.status == 200:
                json_response = await response.json()
                banned_lvl = json_response.get("user_banned_lvl")
                print(f"El usuario ahora tiene nivel de baneo: {banned_lvl}")
                return banned_lvl
            else:
                error = await response.text()
                print(f"Error al banear usuario: {error}")
                return None