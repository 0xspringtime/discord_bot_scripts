import discord

intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    channel = client.get_channel("channel")
    messages = []
    async for message in channel.history(limit=None):
        if message.attachments:
            for attachment in message.attachments:
                # download the media file
                await attachment.save('./"folder"/' + attachment.filename)
                print(f'Saved {attachment.filename}')
    print('Done saving media.')
    await client.close()


client.run("APIKEY")
