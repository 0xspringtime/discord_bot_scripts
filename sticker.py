import os
import discord

intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")
    guild = client.get_guild(GUILD_ID)
    stickerf = "./stickerf"
    os.makedirs(stickerf, exist_ok=True)
    for sticker in guild.stickers:
        with open(f"{stickerf}/{sticker.name}.png", "wb") as f:
            await sticker.save(f)

client.run('BOT_ID')
