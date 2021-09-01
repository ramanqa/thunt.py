import asyncio
import datetime
import random
import websockets
from cryptography.fernet import Fernet

enkey = "Rq6jreLf2EmkllCuzg1DNC7FLnyytt6Q2f4tweo3sDo="
fernet = Fernet(enkey)

async def wsroute(websocket, path):
    async for message in websocket:
        en = fernet.encrypt(message.encode())
        await websocket.send(en.decode())

start_server = websockets.serve(wsroute, "0.0.0.0", 5001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
