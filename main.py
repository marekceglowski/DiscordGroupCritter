import discord
import random
from tinydb import TinyDB, Query
from datetime import datetime
import os
import requests
import json

client = discord.Client()
token = open("token.txt", "r").read().strip()

db = TinyDB('db.json')
submission_tbl = db.table('submissions')
feedback_tbl = db.table('feedback')
crit_stats = db.table('crit_stats')
completed_crits = db.table('completed_crits')

submission_list = []


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
    sub = Submission(message.id, message.author, message.content[len('!add '):], message.jump_url, datetime.now(), [])
    submission_list.append(sub)
    return len(submission_list)


def get_queue_pos(submission_id):
    for idx, sub in enumerate(submission_list, start=1):
        if sub.id == id:
            return idx


##### Client Events #####

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message_edit(before, after):
    if after.author == client.user:
        after.edit(content=after.content, embed=None)
        return


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Add Submission
    if message.content.startswith('!add '):
        pos = add_to_queue(message)
        await dm(message.author, 'Submission added! Current position in queue: '
                 + str(pos) + "\n" + 'Link: ||<' + message.jump_url + '>||\n')

    # Count Submissions
    if message.content.startswith('!count'):
        await message.channel.send('Number of items in the queue is ' + str(len(submission_list)) + '.')

    # Check Submissions
    if message.content.startswith('!check'):
        user_subs = []
        response_str = ''
        for idx, sub in enumerate(submission_list, start=1):
            if message.author.id == sub.user.id:
                user_subs.append((sub, idx))
        if len(user_subs) == 0:
            response_str = 'You currently have no submissions in the queue!'
        else:
            response_str = '> .\n**=========================**\n' + \
                           '> **Submissions in the group crit queue:**\n' + \
                           '> **=========================**\n\n'
            for s_idx, item in enumerate(user_subs, start=1):
                response_str += '> **[Submission ' + str(s_idx) + ']** \n> ' + item[0].time.strftime(
                    '%Y-%m-%d %H:%M:%S') + \
                                ' -- Position in queue: ' + str(item[1]) + '\n' + '> Link: ||<' + item[
                                    0].jump_url + '>||\n'
                if item[0].feedback is not None and len(item[0].feedback) > 0:
                    response_str += '> Feedback Recieved: \n'
                    for f_idx, fb in enumerate(item[0].feedback, start=1):
                        response_str += '>    (' + str(f_idx) + ') ||<' + fb.jump_url + '>||\n'
                response_str += '\n\n'
        response_str + '\n\n.'
        await dm(message.author, response_str)
        if not isinstance(message.channel, discord.DMChannel):
            await message.delete()

    # Crit Random
    if message.content.startswith('!crit random'):
        sub = random.choice(submission_list)
        text = 'Random submission to review:\n' + \
               'Submission #' + str(get_queue_pos(sub.id)) + '\n' + \
               'Link: ' + sub.jump_url + '\n' + \
               '*Go to the above link, and reply to the message to give feedback.*\n.'
        dm(message.author, text)

    # Add Feedback (auto)
    if message.reference is not None:
        for sub in submission_list:
            if sub.id == message.reference.message_id:
                if sub.feedback is None:
                    sub.feedback = []
                fb = Submission(message.id, message.author, message.content, message.jump_url, datetime.now(), None)
                sub.feedback.append(fb)

        print(message.reference)


client.run(token)
