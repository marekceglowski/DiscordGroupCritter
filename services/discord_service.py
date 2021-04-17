import discord
import utils.split_util as split_util

group_crit_channel_id = 802620586513530895


async def dm(user, text, wrap_at=2000):
    split_text = split_util.split(text, wrap_at)
    for chunk in split_text:
        await user.send(chunk)


def is_group_crit_channel(ctx):
    return ctx.channel.id == group_crit_channel_id
