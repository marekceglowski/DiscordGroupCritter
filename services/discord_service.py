import discord

group_crit_channel_id = 802620586513530895

async def dm(author, text):
    if author.dm_channel is None:
        await author.create_dm()
    await author.dm_channel.send(text, embed=None)


def is_group_crit_channel(ctx):
    return ctx.channel.id == group_crit_channel_id
