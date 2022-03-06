import os
import discord
import pandas as pd
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.messages=True
client = discord.Client(intents = intents)
df = pd.read_csv("test.csv")
ids = df["Discord id (Don't have it? We would suggest you to make one)"].tolist()
names = df["Name"].tolist()
entrynos = df["Entry Number"].tolist()
groups = df["group"].tolist()
# print(df)
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Say hello!')
        # role = discord.utils.get(message.guild.roles, name="member") #  Gets the member role as a `role` object
        # await message.author.add_roles(role) # Gives the role to the user

    if message.content.startswith('$send_invite'):
        await create_invite(message)

    if message.content.startswith('??202') and (message.content.isupper() or message.content.islower()):
        message_con = message.content[2:]
        # print(groups)
        for i in range(len(entrynos)):
            if entrynos[i].casefold() == message_con.casefold():
                # print(groups[i])
                role = discord.utils.get(message.guild.roles, name="Group "+groups[i])
                await message.author.add_roles(role)
                await message.add_reaction("✅")
                await message.delete(delay = 2)
                await message.author.edit(nick = names[i])
                df.at[i, "Discord id (Don't have it? We would suggest you to make one)"] = message.author.name+"#"+message.author.discriminator
                df.to_csv("test.csv", index=False)
                break

@client.event
async def on_member_join(member):
    # print("ok")
    # print("Recognised that a member called " + member.name + " joined")
    # print(member.guild.roles)
    # role = discord.utils.get(member.guild.roles, name="member") #  Gets the member role as a `role` object
    
    # print(ids)
    # print(member.name)
    nameanddis = member.name+"#"+member.discriminator
    id = member.id
    for i in range(len(ids)):
        if type(ids[i])==str:
            if ids[i].replace(" ", "").casefold() == nameanddis.replace(" ", "").casefold() or ids[i]==id or ids[i].replace(" ", "").casefold() == member.name.replace(" ", "").casefold():
                role = discord.utils.get(member.guild.roles, name="Group "+groups[i])
                await member.add_roles(role) # Gives the role to the user
                await member.edit(nick= names[i])    

async def create_invite(message):
    guild = message.guild
    channel = guild.get_channel(947579944920313870)
    invite = await channel.create_invite(max_uses=1, temporary=True, unique=True, reason="Kerberos")

    port=465
    password= os.getenv("gmailpw")
    context = ssl.create_default_context()
    a = MIMEMultipart("alternative")
    a["Subject"] = "AXLR8R Formula Racing - Discord Invite"
    a["From"] = os.getenv("emailid")
    a["To"] = ""                                         #to email id

   # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <html>
    <body>
        <h2>Hi</h2>
        <h3>In reference to the google form you filled regarding recruitment for AXLR8R Formula Racing, here is your invite link for our discord server.
        Please note that this invite link is personalised for you(it only works once), hence we request you to not share it.</h3>
        <a href="{}">CLICK ME TO JOIN DISCORD!</a> 
        <img src="https://i.ibb.co/yQc7CHr/axlr8r-logo.png" alt="axlr8r-logo" border="0">
    </body>
    </html>
    """.format(invite.url)
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    a.attach(part1)
    a.attach(part2)

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("alphaaviral@gmail.com", password)
        server.sendmail("alphaaviral@gmail.com","ph1200687@iitd.ac.in",a.as_string())
client.run(os.getenv("botpw"))