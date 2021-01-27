from .member import Member


def setup(bot):
    bot.add_cog(Member(bot))
