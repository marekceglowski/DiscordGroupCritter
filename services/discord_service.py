import discord


async def dm(author, text):
    if author.dm_channel is None:
        await author.create_dm()
    await author.dm_channel.send(text, embed=None)
