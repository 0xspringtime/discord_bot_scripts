import os
import discord

intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")
    guild = client.get_guild(USER_GUILD)
    emoji_folder = "./emoji_folder"
    os.makedirs(emoji_folder, exist_ok=True)
    for emoji in guild.emojis:
        with open(f"{emoji_folder}/{emoji.name}.png", "wb") as f:
            await emoji.save(f)

client.run('BOT_ID')
