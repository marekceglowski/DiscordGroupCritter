import discord

group_crit_channel_id = 802620586513530895

def is_group_crit_channel(ctx):
    return ctx.channel.id == group_crit_channel_id
