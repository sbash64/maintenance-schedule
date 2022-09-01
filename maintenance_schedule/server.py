import asyncio
import websockets


async def handle_websocket(websocket):
    async for message in websocket:
        await websocket.send(message)


async def serve_websocket():
    async with websockets.serve(handle_websocket, port=8001):
        await asyncio.Future()


async def handle_tcp(reader, writer):
    data = await reader.read(100)
    writer.write(data)
    await writer.drain()
    writer.close()


async def serve_tcp():
    server = await asyncio.start_server(handle_tcp, port=8000)
    async with server:
        await server.serve_forever()


async def main():
    await asyncio.gather(serve_tcp(), serve_websocket())


asyncio.run(main())
