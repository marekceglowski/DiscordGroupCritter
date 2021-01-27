import discord
from discord.ext import commands
import services.db_service as _db
import services.discord_service as _discord

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot