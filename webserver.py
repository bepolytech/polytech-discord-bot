from aiohttp import web
import logging

logger = logging.getLogger(__name__)

routes = web.RouteTableDef()

@routes.get("/")
async def root_handler(request):
    return web.Response(text="Bot is running.")

# ---- TEST : ----
@routes.post("/trigger")
async def trigger_handler(request):
    data = await request.json()
    bot = request.app["bot"]
    logger.info("Received external trigger: %s", data)

    # Example action: send a message to a hardcoded channel ID
    channel_id = data.get("channel_id")
    message = data.get("message", "No message provided.")
    if channel_id:
        channel = bot.get_channel(int(channel_id))
        if channel:
            await channel.send(message)
            return web.Response(text="Message sent.")
        return web.Response(text="Channel not found.", status=404)
    return web.Response(text="Missing channel_id.", status=400)
# --------

app = web.Application()
async def run_webserver(bot):
    app.add_routes(routes)
    app["bot"] = bot
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=8080)
    await site.start()
    logger.info("Web server started on http://0.0.0.0:8080")

async def stop_webserver():
    # Gracefully shuts down the web server
    logger.info("Shutting down web server...")
    await app.cleanup()  # Cleans up all aiohttp resources, closing connections and finalizing any running tasks.
