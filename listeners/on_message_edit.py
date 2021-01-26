import discord
from discord.ext import commands


class OnMessageEdit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author == self.lmy_bot.user:
            after.edit(content=after.content, embed=None)