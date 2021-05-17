from discord.ext import commands
from core.cog_config import CogExtension
from core.db import JsonApi
import asyncio
import discord


class Voice(CogExtension):
    @commands.group()
    @commands.has_any_role('總召', 'Administrator')
    async def voice(self, ctx):
        pass

    # remove member in voice channel
    @voice.command()
    async def kick_timer(self, ctx, channel_id: int, countdown: int):
        countdown_duration = countdown
        voice_channel = self.bot.get_channel(channel_id)

        def content(s):
            return f':exclamation: 所有成員將在 {s} 秒後被移出 {voice_channel.name}'

        message = await ctx.send(content(countdown_duration))
        while countdown_duration > 0:
            await message.edit(content=content(countdown_duration))
            await asyncio.sleep(1)
            countdown_duration -= 1

        await message.delete()

        for member in voice_channel.members:
            await member.move_to(None)

    @voice.command()
    @commands.has_any_role('總召', 'Administrator')
    async def set_default_connect(self, ctx, channel_id: int, mode: int):
        protect_target_channel = ctx.guild.get_channel(channel_id)
        await protect_target_channel.set_permissions(ctx.guild.default_role, connect=bool(mode))

        # dynamic creating personal voice channel
        @voice.command(aliases=['make'])
        async def make_channel_for(self, ctx, members: commands.Greedy[discord.Member]):
            terminal_channel = ctx.guild.get_channel(839170475309006979)

            if ctx.author.voice.channel != terminal_channel:
                return await ctx.send(f':x: 請先加入 {terminal_channel.name} 以使用這個指令！')

            make_channel = await ctx.guild.create_voice_channel(
                name=f"{members[0].display_name}'s party",
                category=terminal_channel.category
            )

            for member in members:
                if member.voice.channel is None:
                    continue

                perms = {
                    "connect": True,
                    "request_to_speak": True,
                    "speak": True,
                    "stream": True,
                    "use_voice_activation": True
                }
                await make_channel.set_permissions(member, **perms)
                await member.move_to(make_channel)

            await make_channel.set_permissions(ctx.guild.default_role, connect=False)
            await ctx.send(f':white_check_mark: 已創建頻道 {make_channel.name}！')

        @commands.Cog.listener()
        async def on_voice_state_update(self, member, before, after):
            if not before.channel.name.endswith('party'):
                return

            if before.channel is None or before.channel == after.channel:
                return

            if before.channel.name == f"{member.display_name}'s party":
                await before.channel.delete()

            if not before.channel.members:
                await before.channel.delete()

    # for meeting usage
    @commands.group(aliases=['meeting'])
    @commands.has_any_role('總召', 'Administrator')
    async def voice_meeting(self, ctx):
        pass

    @voice_meeting.command()
    async def on(self, ctx, channel_id: int):
        target_channel = ctx.guild.get_channel(channel_id)
        if target_channel is None:
            return await ctx.send(':x: 這是一個無效頻道！')

        dyn_json = JsonApi().get('DynamicSetting')

        if channel_id in dyn_json["voice_in_meeting"]:
            return await ctx.send(f':x: 頻道 {target_channel.name} 已在開會模式中！')

        dyn_json["voice_in_meeting"].append(channel_id)
        JsonApi().put('DynamicSetting', dyn_json)

        await target_channel.set_permissions(ctx.guild.default_role, connect=False)
        await ctx.send(':white_check_mark: 指令執行完畢！')

    @voice_meeting.command()
    async def off(self, ctx, channel_id: int):
        target_channel = ctx.guild.get_channel(channel_id)
        if target_channel is None:
            return await ctx.send(':x: 這是一個無效頻道！')

        dyn_json = JsonApi().get('DynamicSetting')

        if channel_id not in dyn_json["voice_in_meeting"]:
            return await ctx.send(f':x: 頻道 {target_channel.name} 不在開會模式中！')

        dyn_json["voice_in_meeting"].remove(channel_id)
        JsonApi().put('DynamicSetting', dyn_json)

        await target_channel.set_permissions(ctx.guild.default_role, connect=True)
        await ctx.send(':white_check_mark: 指令執行完畢！')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        voice_in_protect = JsonApi().get('DynamicSetting')["voice_in_meeting"]

        if before.channel is not None and after.channel != before.channel and before.channel.id in voice_in_protect:
            await member.move_to(before.channel)


def setup(bot):
    bot.add_cog(Voice(bot))
