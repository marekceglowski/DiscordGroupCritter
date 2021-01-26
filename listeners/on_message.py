import discord
from discord.ext import commands


class OnMessage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.lmy_bot.user:
            return
        # Add Feedback (auto)
        if message.channel.id == crit_channel_id:
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