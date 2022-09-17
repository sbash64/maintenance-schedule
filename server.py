import io
import datetime

from aiohttp import web
import aiohttp

from maintenance_schedule.remind import (
    new_schedule,
    add_to_schedule,
    remove_from_schedule,
)
from maintenance_schedule.parse import parse_maintenance, parse_from_date


async def websocket_handler(request):
    schedule = new_schedule()
    websocket_response = web.WebSocketResponse()
    await websocket_response.prepare(request)
    async for message in websocket_response:
        if message.type == aiohttp.WSMsgType.TEXT:
            if message.data == "close":
                await websocket_response.close()
            else:
                add_to_schedule(
                    schedule,
                    parse_maintenance(message.data),
                    parse_from_date(message.data, datetime.date.today()),
                )
                response = io.StringIO()
                print(schedule, file=response)
                response_message = response.getvalue()
                response.close()
                await websocket_response.send_str(response_message)
        elif message.type == aiohttp.WSMsgType.ERROR:
            print(
                f"websocket connection closed with exception {websocket_response.exception()}"
            )
    print("websocket connection closed")
    return websocket_response


application = web.Application()
application.add_routes([web.get("/", lambda request: web.FileResponse("index.html"))])
application.add_routes(
    [web.get("/browser.js", lambda request: web.FileResponse("browser.js"))]
)
application.add_routes([web.get("/ws", websocket_handler)])
web.run_app(application)
