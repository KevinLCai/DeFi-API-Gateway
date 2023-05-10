import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        response = f"Server received: {message}"
        await websocket.send(response)
        print(f"Sent response: {response}")

async def main():
    async with websockets.serve(echo, "localhost", 3000):
        print("WebSocket server started")
        await asyncio.Future()  # run forever

asyncio.run(main())
