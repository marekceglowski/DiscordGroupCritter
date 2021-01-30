import discord


async def dm(author, text):
    if author.dm_channel is None:
        await author.create_dm()
    await author.dm_channel.send(text, embed=None)

async def get_replied_message(message):
    return await message.channel.fetch_message(message.reference.message_id)