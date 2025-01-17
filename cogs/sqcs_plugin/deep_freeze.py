from discord.ext import commands
from core.cog_config import CogExtension
import core.db.mongodb as mongo
from core.utils import DiscordExt


class DeepFreeze(CogExtension):

    @commands.group()
    @commands.has_any_role('總召', 'Administrator')
    async def df(self, ctx):
        pass

    @df.command()
    async def mani(self, ctx, member_id: int, status: int):
        if status not in [0, 1]:
            return await ctx.send(':x: 狀態參數必須為 0 或 1！')

        fluct_cursor, = await mongo.get_cursors('LightCube', ['MainFluctlights'])
        try:
            execute = {
                "$set": {
                    "deep_freeze": bool(status)
                }
            }
            fluct_cursor.update_one({"_id": member_id}, execute)
            member = ctx.guild.get_member(member_id)

            await member.send(f':exclamation: 你的 `deep freeze` 狀態被設定為 {bool(status)} 了！')
            await ctx.send(':white_check_mark: 指令執行完畢！')
        except Exception as e:
            return await ctx.send(content=e, delete_after=8)

    @df.command()
    async def list(self, ctx):
        await ctx.send(':hourglass_flowing_sand: 尋找中...')

        fluct_cursor, = await mongo.get_cursors('LightCube', ['MainFluctlights'])
        data = fluct_cursor.find({"deep_freeze": {"$eq": True}})

        if data.count() == 0:
            return await ctx.send(':x: 沒有成員在凍結狀態中！')

        member_list = str()
        for member in data:
            member_name = await DiscordExt.get_member_nick_name(ctx.guild, member["_id"])

            member_list += member_name + '\n'

            if len(member_list) > 1600:
                await ctx.send(member_list)
                member_list = ''

        if len(member_list) > 0:
            await ctx.send(member_list)

        await ctx.send(':white_check_mark: 記錄尋找完畢！')


def setup(bot):
    bot.add_cog(DeepFreeze(bot))
