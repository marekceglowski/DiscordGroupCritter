# Standard library imports
import random
from datetime import datetime

# Third-party imports
import discord
from discord.ext import commands, tasks

# Application-specific imports
from models.submission import Submission
import commands.add as add
import commands.check as check
import commands.count as count
import commands.critrandom as critrandom
import listeners.on_message as on_message
import listeners.on_message_edit as on_message_edit


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


# Commands
lmy_bot.add_cog(add.Add(lmy_bot))
lmy_bot.add_cog(check.Check(lmy_bot))
lmy_bot.add_cog(count.Count(lmy_bot))
lmy_bot.add_cog(critrandom.CritRandom(lmy_bot))
lmy_bot.add_cog(on_message.OnMessage(lmy_bot))

lmy_bot.run(token)
