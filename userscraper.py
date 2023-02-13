import discord
from openpyxl import Workbook
wb = Workbook()
ws = wb.active

ws.append(["Name"])

intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    server = client.get_guild(YOUR_SERVER_ID)
    members = server.members
    for member in members:
        print(member.name)
        ws.append([member.name + "#" + member.discriminator])


client.run("YOUR_BOT_TOKEN")




wb.save("members.xlsx")
