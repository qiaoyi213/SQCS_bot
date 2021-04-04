from core.classes import Cog_Extension
from discord.ext import commands
import core.functions as func
from core.setup import jdata, client, fluctlight_client
import random


class Query(Cog_Extension):

    @commands.group()
    async def query(self, ctx):
        pass

    @query.command()
    @commands.has_any_role('總召', 'Administrator')
    async def quiz(self, ctx):
        await func.report_cmd(self.bot, ctx, f'[CMD EXECUTED][query][quiz]')

        quiz_cursor = client["quiz_event"]
        data = quiz_cursor.find({})

        status = str()
        for item in data:
            member_name = (await ctx.guild.fetch_member(item["_id"])).nick
            if member_name is None:
                member_name = (await ctx.guild.fetch_member(item["_id"])).name

            status += f'{member_name}: {item["correct"]}\n'

            if len(status) > 1600:
                await ctx.send(status)

        if len(status) > 0:
            await ctx.send(status)

    @query.command()
    async def my_data(self, ctx):
        await func.report_cmd(self.bot, ctx, f'[CMD EXECUTED][query][my_data]')

        await ctx.author.send(embed=(await personal_info(ctx.author.id)))

    @query.command()
    @commands.has_any_role('總召', 'Administrator')
    async def member_data(self, ctx, target_id: int):
        await func.report_cmd(self.bot, ctx, f'[CMD EXECUTED][query][member_data][target_id: {target_id}]')

        await ctx.author.send(embed=(await personal_info(target_id)))


async def personal_info(member_id):
    fluctlight_cursor = fluctlight_client["light-cube-info"]
    data = fluctlight_cursor.find_one({"_id": member_id})

    # method used when checking a dict is empty or not
    if not data:
        return func.create_embed('Object info', 'default', 0xe46bf9, ['Error'], ['Logging error'])

    value_title = ['Object Id', 'Score', 'Durability', 'Object Control Authority', 'System Control Authority',
                   'Contribution', 'Levelling Index', "Deep Freeze"]
    obj_info = [data["_id"], data["score"], data["du"], data["oc_auth"], data["sc_auth"], data["contrib"],
                data["lvl_ind"], data["deep_freeze"]]

    rand_icon = random.choice(jdata['fluctlight_gifs'])
    return func.create_embed('Object info', rand_icon, 0xe46bf9, value_title, obj_info)


def setup(bot):
    bot.add_cog(Query(bot))
