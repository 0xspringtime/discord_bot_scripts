import discord
from discord.ext import commands
import yt_dlp

intents = discord.Intents.all()

intents.message_content = True

Bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

ydl_opts = {
    'format': 'bestaudio',
}

queue = []

@Bot.event
async def on_ready():
    print(f'We have logged in as {Bot.user}')

@Bot.command(aliases=['j'])
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@Bot.command(aliases=['p'])
async def play(ctx, url : str):
    # Ensure bot is in the voice channel
    if ctx.voice_client is None:
        if ctx.message.author.voice:
            await ctx.message.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel")
            return

    queue.append(url)  # Add the url to the queue

    if not ctx.voice_client.is_playing():  # If not already playing audio, start playing
        await play_next(ctx)

async def play_next(ctx):
    if len(queue) > 0:
        url = queue.pop(0)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            file = ydl.extract_info(url, download=False)
            url2 = file['url']
            ctx.voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: ctx.bot.loop.create_task(play_next(ctx)))

@Bot.command(aliases=['l'])
async def leave(ctx):
    voice_Bot = ctx.voice_Bot
    if voice_Bot is not None:
        await voice_Bot.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@Bot.command(aliases=['q'])
async def queue_info(ctx):
    if not queue:
        await ctx.send("No songs in the queue.")
        return

    msg = "Songs in the queue:\n"
    for i, url in enumerate(queue):
        msg += f"{i+1}. {url}\n"

    await ctx.send(msg)

@Bot.command(aliases=['s'])
async def skip(ctx):
    # Check for user permissions
    user_perms = ctx.message.channel.permissions_for(ctx.message.author)
    voice_channel = ctx.message.author.voice.channel
    num_members = len(voice_channel.members) - 1 # exclude the bot itself

    if user_perms.manage_roles:
        ctx.voice_client.stop()
        await ctx.send('Skipping...')
        return await play_next(ctx)
    else:
        return await ctx.send("You don't have permission to skip the song.")

@Bot.command()
async def h(ctx):
    embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())

    embed.add_field(name="!join or !j", value="Connects the bot to your voice channel.", inline=False)
    embed.add_field(name="!play [url] or !p [url]", value="Adds the song to the queue and plays if not already playing.", inline=False)
    embed.add_field(name="!leave or !l", value="Disconnects the bot from the voice channel.", inline=False)
    embed.add_field(name="!queue_info or !q", value="Displays the songs in the queue.", inline=False)
    embed.add_field(name="!skip or !s", value="Skips the currently playing song.", inline=False)
    embed.add_field(name="!help", value="Displays the help information.", inline=False)

    await ctx.send(embed=embed)


Bot.run('')

