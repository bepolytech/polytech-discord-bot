from disnake.ext import commands
import disnake
import logging

logger = logging.getLogger(__name__)

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        description="Replies with pong."
    )
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        logger.info(f"/ping used by {inter.author}")
        await inter.response.send_message("Pong!")

# The setup function is used by disnake to load the cog dynamically
# It is automatically called by `bot.load_extension("cogs.example")`
def setup(bot):
    bot.add_cog(Example(bot))
