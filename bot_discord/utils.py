from config import API_URL
import requests
import aiohttp

#file that calls django api

async def createUser(member):
    data = {
        "discord_id": str(member.id),
        "username": member.name,
        "discriminator": member.discriminator
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8000/users/create/", json=data) as response:
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
        async with session.put(f"http://127.0.0.1:8000/users/{member.id}/message/", json=data) as response:
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
    response = requests.get(f"http://127.0.0.1:8000/users/{member.id}/", json=data)
    if response.status_code == 200:
        return response.json()  # <-- devuelve los datos del usuario
    else:
        return None