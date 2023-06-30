import discord
from discord.ext import commands
import yt_dlp

intents = discord.Intents.all()

intents.message_content = True

Bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

ydl_opts = {
    'format': 'bestaudio',
}


@Bot.event
async def on_ready():

    print(f'We have logged in as {Bot.user}')

@Bot.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@Bot.command()
async def play(ctx, url : str):
    # Ensure bot is in the voice channel
    if ctx.voice_client is None:
        if ctx.message.author.voice:
            await ctx.message.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel")
            return
    else:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        file = ydl.extract_info(url, download=False)
        url2 = file['url']
        ctx.voice_client.play(discord.FFmpegPCMAudio(url2))

@Bot.command()
async def leave(ctx):
    voice_Bot = ctx.voice_Bot
    if voice_Bot is not None:
        await voice_Bot.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

Bot.run('')

