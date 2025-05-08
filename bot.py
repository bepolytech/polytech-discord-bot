import disnake
from disnake.ext import commands
import logging
import os
import asyncio
import signal
from os import getenv
from dotenv import load_dotenv
from webserver import run_webserver, stop_webserver
load_dotenv()

# Logging setup
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(name)s: %(message)s"
)

logger = logging.getLogger(__name__)

# Bot setup
intents = disnake.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.InteractionBot(intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"Bot ready. Logged in as {bot.user} (ID: {bot.user.id})")

# Load cogs dynamically, see /cogs/ directory for commands
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        logger.info(f"Loaded extension: {filename}")

# Unified async entry point with graceful shutdown
async def main():
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def shutdown():
        logger.info("Shutdown signal received.")
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, shutdown)

    #await run_webserver(bot) # TODO: implement webserver later
    bot_task = asyncio.create_task(bot.start(getenv("BOT_TOKEN")))

    await stop_event.wait()
    logger.info("Shutting down bot...")
    await bot.close()
    #await stop_webserver() # TODO:

if __name__ == "__main__":
    asyncio.run(main())
