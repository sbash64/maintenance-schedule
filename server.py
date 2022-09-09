import io
import datetime

from aiohttp import web
import aiohttp

from maintenance_schedule.remind import (
    HowOften,
    Maintenance,
    new_schedule,
    add_to_schedule,
)
from maintenance_schedule.parse import parse_maintenance


async def websocket_handler(request):
    schedule = new_schedule()
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == "close":
                await ws.close()
            else:
                add_to_schedule(
                    schedule,
                    parse_maintenance(msg.data),
                    datetime.date.today(),
                )
                response = io.StringIO()
                print(schedule, file=response)
                responseMessage = response.getvalue()
                response.close()
                await ws.send_str(responseMessage)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print("ws connection closed with exception %s" % ws.exception())
    print("websocket connection closed")
    return ws


app = web.Application()
app.add_routes([web.get("/", lambda request: web.FileResponse("index.html"))])
app.add_routes([web.get("/browser.js", lambda request: web.FileResponse("browser.js"))])
app.add_routes([web.get("/ws", websocket_handler)])
web.run_app(app)
