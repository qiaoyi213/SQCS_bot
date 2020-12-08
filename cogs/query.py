from core.classes import *
from core.classes import Cog_Extension
from discord.ext import commands
from functions import *
from core.setup import *
import discord
import json

class Query(Cog_Extension):

    @commands.group()
    async def query(self, ctx):
        pass

    @query.command()
    async def quiz(self, ctx):
        info.execute('SELECT * FROM quiz;')

        status = str()
        for data in info.fetchall():
            member = await self.bot.guilds[0].fetch_member(data[0])
            status += f'{member.nick}: {data[1]}\n'

        await ctx.send(status)

def setup(bot):
    bot.add_cog(Query(bot))