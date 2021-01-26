import os
import requests
import json
import random
import discord
from tinydb import TinyDB, Query
from datetime import datetime
from discord.ext import commands, tasks


token = open("token.txt", "r").read().strip()
crit_channel_id = 802620586513530895

submission_list = []

intents = discord.Intents(messages=True, guilds=False, members=False)
lmy_bot = commands.Bot(command_prefix="!", intents=intents)

##### Models ######


class Submission:
    def __init__(self, id, user, content, jump_url, time, feedback):
        self.id = id
        self.user = user
        self.content = content
        self.jump_url = jump_url
        self.time = time
        self.feedback = feedback


##### Functions #####


def get_name(author):
    return author.nick or author.name


async def dm(author, text):
    if author.dm_channel is None:
        await author.create_dm()
    await author.dm_channel.send(text, embed=None)


def add_to_queue(message):
    sub = Submission(
        message.id,
        message.author,
        message.content,
        message.jump_url,
        datetime.now(),
        [],
    )
    submission_list.append(sub)
    return len(submission_list)


def get_queue_pos(submission_id):
    for idx, sub in enumerate(submission_list, start=1):
        if sub.id == id:
            return idx


class CritBot(commands.Cog):
    """
    Crit bot
    """

    def __init__(self, lmy_bot):
        self.lmy_bot = lmy_bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.lmy_bot.user:
            return
        # Add Feedback (auto)
        # TODO: maybe make check global
        # if message.channel.id == crit_channel_id:
        if message.reference is not None:
            for sub in submission_list:
                if sub.id == message.reference.message_id:
                    if sub.feedback is None:
                        sub.feedback = []
                    fb = Submission(
                        message.id,
                        message.author,
                        message.content,
                        message.jump_url,
                        datetime.now(),
                        None,
                    )
                    sub.feedback.append(fb)

            print(message.reference)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author == self.lmy_bot.user:
            after.edit(content=after.content, embed=None)

    @commands.command(
        name="add",
        help="Adds a link to the message prepended by !add to the submission queue",
    )
    async def add_crit(self, ctx, *, arg):
        pos = add_to_queue(ctx.message)
        await dm(
            ctx.author,
            "Submission added! Current position in queue: "
            + str(pos)
            + "\n"
            + "Link: ||<"
            + ctx.message.jump_url
            + ">||\n",
        )

    @commands.command(
        name="count", help="Returns the number of items in the queue for review"
    )
    async def count_crits(self, ctx):
        await ctx.send(
            "Number of items in the queue is " + str(len(submission_list)) + "."
        )

    @commands.command(
        name="check",
        help="Returns your entered items and any responses they have received",
    )
    async def check_crit(self, ctx):
        user_subs = []
        response_str = ""
        for idx, sub in enumerate(submission_list, start=1):
            if ctx.author.id == sub.user.id:
                user_subs.append((sub, idx))
        if len(user_subs) == 0:
            response_str = "You currently have no submissions in the queue!"
        else:
            response_str = (
                "> .\n**=========================**\n"
                + "> **Submissions in the group crit queue:**\n"
                + "> **=========================**\n\n"
            )
            for s_idx, item in enumerate(user_subs, start=1):
                response_str += (
                    "> **[Submission "
                    + str(s_idx)
                    + "]** \n> "
                    + item[0].time.strftime("%Y-%m-%d %H:%M:%S")
                    + " -- Position in queue: "
                    + str(item[1])
                    + "\n"
                    + "> Link: ||<"
                    + item[0].jump_url
                    + ">||\n"
                )
                if item[0].feedback is not None and len(item[0].feedback) > 0:
                    response_str += "> Feedback Recieved: \n"
                    for f_idx, fb in enumerate(item[0].feedback, start=1):
                        response_str += (
                            ">    (" + str(f_idx) + ") ||<" + fb.jump_url + ">||\n"
                        )
                response_str += "\n\n"
        response_str + "\n\n."
        await dm(ctx.author, response_str)

    @commands.command(
        name="critRandom", help="Returns a random submission from the queue"
    )
    async def get_crit_random(self, ctx):
        # Crit Random
        sub = random.choice(submission_list)
        text = (
            "Random submission to review:\n"
            + "Submission #"
            + str(get_queue_pos(sub.id))
            + "\n"
            + "Link: "
            + sub.jump_url
            + "\n"
            + "*Go to the above link, and reply to the message to give feedback.*\n."
        )
        await dm(ctx.author, text)


@lmy_bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(lmy_bot))


lmy_bot.add_cog(CritBot(lmy_bot))
lmy_bot.run(token)
