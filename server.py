import io

from aiohttp import web
import aiohttp

from maintenance_schedule.remind import new_schedule
from maintenance_schedule.parse import parse_method


async def handle_text_message(websocket_response, message, schedule):
    if message == "close":
        await websocket_response.close()
    else:
        parse_method(message)(message, schedule)
        response = io.StringIO()
        print(schedule, file=response)
        response_message = response.getvalue()
        response.close()
        await websocket_response.send_str(response_message)


async def handle_message(websocket_response, message, schedule):
    if message.type == aiohttp.WSMsgType.TEXT:
        await handle_text_message(websocket_response, message.data, schedule)
    elif message.type == aiohttp.WSMsgType.ERROR:
        print(
            f"websocket connection closed with exception {websocket_response.exception()}"
        )


async def websocket_handler(request):
    schedule = new_schedule()
    websocket_response = web.WebSocketResponse()
    await websocket_response.prepare(request)
    async for message in websocket_response:
        await handle_message(websocket_response, message, schedule)
    print("websocket connection closed")
    return websocket_response


application = web.Application()
application.add_routes(
    [
        web.get("/", lambda request: web.FileResponse("index.html")),
        web.get("/browser.js", lambda request: web.FileResponse("browser.js")),
        web.get("/ws", websocket_handler),
    ]
)
web.run_app(application)
