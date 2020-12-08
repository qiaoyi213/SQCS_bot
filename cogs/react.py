from core.classes import Cog_Extension
from discord.ext import commands
from functions import *
from core.setup import *
import discord
import json


class React(Cog_Extension):

    # bots communication event
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot == 'False' or ctx.author == self.bot.user or (
                ctx.channel != getChannel('_ToMV') or ctx.channel != getChannel('_ToSyn')):
            return

        MsgCont = str(ctx.content).split(' ')

        if MsgCont[0] == 'sw' and ctx.channel == getChannel('_ToMV'):
            temp_file = open('jsons/lecture.json', mode='r', encoding='utf8')
            lect_data = json.load(temp_file)
            temp_file.close()

            lect_data['temp_sw'] = MsgCont[1]

            temp_file = open('jsons/lecture.json', mode='w', encoding='utf8')
            json.dump(lect_data, temp_file)
            temp_file.close()
            return

    @commands.command()
    async def msg_re(self, ctx, *, msg):
        re_msg = msg.split('\n')
        for msg in re_msg:
            await ctx.send(msg)

        await getChannel('_Report').send(f'[Command]msg_re used by member {ctx.author.id}. {now_time_info("whole")}')


def setup(bot):
    bot.add_cog(React(bot))