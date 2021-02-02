# Standard library imports
import random
from datetime import datetime

# Third-party imports
import discord
from discord.ext import commands, tasks


token = open("token.txt", "r").read().strip()
crit_channel_id = 802620586513530895

submission_list = []

intents = discord.Intents(messages=True, guilds=False, members=False)
lmy_bot = commands.Bot(command_prefix="!", intents=intents)


def get_name(author):
    return author.nick or author.name


@lmy_bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(lmy_bot))


# Cogs
lmy_bot.load_extension("cogs.admin")
lmy_bot.load_extension("cogs.member")


lmy_bot.run(token)
