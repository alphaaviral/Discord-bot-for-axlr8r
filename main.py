import os
import discord
import pandas as pd
# import smtplib,ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import requests
import json

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.messages=True
client = discord.Client(intents = intents)
df = pd.read_csv("data.csv")
ids = df["Discord id (Don't have it? We would suggest you to make one)"].tolist()
names = df["Name"].tolist()
entrynos = df["Entry Number"].tolist()
groups = df["Groups"].tolist()

# print(df)
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    self = client.get_user(760079854501756939)
    await self.send(content="Bot online")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.add_reaction("✅")
        await message.delete(delay = 1)

    # if message.content.startswith('$send_invite'):
    #     await create_invite(message)

    if message.content.startswith('??202'):
        try:
            if(len(message.author.roles)>1):    
                await message.author.send("You are already in a group")
                await message.add_reaction("🛑")
                await message.delete(delay = 2)
                print(len(message.author.roles))
            else:
                message_con = message.content[2:]
                for i in range(len(entrynos)):
                    if entrynos[i].casefold() == message_con.casefold():
                        role = discord.utils.get(message.guild.roles, name="Group "+groups[i])
                        fresherrole = discord.utils.get(message.guild.roles, name="Fresher")
                        await message.author.add_roles(role, fresherrole)
                        await message.add_reaction("✅")
                        await message.delete(delay = 2)
                        await message.author.send(content = "You have been assigned the group " + groups[i])
                        await message.author.edit(nick = names[i])
                        data = {
                            'entry number': entrynos[i],
                            'discord id': message.author.name+"#"+message.author.discriminator,
                        }
                        r = requests.post(url = "https://axlr8r-bot-default-rtdb.firebaseio.com/fresher-data.json", data =json.dumps(data))
                        # print(r.status_code)
                        return
                await message.add_reaction("🛑")
                await message.delete(delay = 2)
                await message.author.send(content = "You entered an invalid entry number (You did not fill the form floated after the main orientation :). Contact a mod for more info!)")
        except:
            print("Error")
            self = client.get_user(760079854501756939)
            await self.send(content="AN ERROR OCCURED https://dashboard.heroku.com/apps/axlr8r-bot/logs")

@client.event
async def on_member_join(member):
    try:
        nameanddis = member.name+"#"+member.discriminator
        id = member.id
        for i in range(len(ids)):
            if type(ids[i])==str:
                if ids[i].replace(" ", "").replace("@", "").replace("(","").replace(")", "").casefold() == nameanddis.replace(" ", "").casefold() or ids[i]==id or ids[i].replace(" ", "").replace("@", "").replace("(","").replace(")", "").casefold() == member.name.replace(" ", "").casefold():
                    role = discord.utils.get(member.guild.roles, name="Group "+groups[i])
                    fresherrole = discord.utils.get(member.guild.roles, name="Fresher")
                    await member.add_roles(role, fresherrole) # Gives the role to the user
                    await member.edit(nick= names[i])  
                    data = {
                            'entry number': entrynos[i],
                            'discord id': member.name+"#"+member.discriminator,
                        }
                    r = requests.post(url = "https://axlr8r-bot-default-rtdb.firebaseio.com/fresher-data.json", data =json.dumps(data))
                         
    except:
        print("error")
        self = client.get_user(760079854501756939)
        await self.send(content="AN ERROR OCCURED https://dashboard.heroku.com/apps/axlr8r-bot/logs")
# async def create_invite(message):
#     guild = message.guild
#     channel = guild.get_channel(947579944920313870)
#     invite = await channel.create_invite(max_uses=1, temporary=True, unique=True, reason="Kerberos")

#     port=465
#     password= os.getenv("gmailpw")
#     context = ssl.create_default_context()
#     a = MIMEMultipart("alternative")
#     a["Subject"] = "AXLR8R Formula Racing - Discord Invite"
#     a["From"] = os.getenv("emailid")
#     a["To"] = ""                                         #to email id

#    # Create the plain-text and HTML version of your message
#     text = """\
#     Hi,
#     How are you?
#     Real Python has many great tutorials:
#     www.realpython.com"""
#     html = """\
#     <html>
#     <body>
#         <h2>Hi</h2>
#         <h3>In reference to the google form you filled regarding recruitment for AXLR8R Formula Racing, here is your invite link for our discord server.
#         Please note that this invite link is personalised for you(it only works once), hence we request you to not share it.</h3>
#         <a href="{}">CLICK ME TO JOIN DISCORD!</a> 
#         <img src="https://i.ibb.co/yQc7CHr/axlr8r-logo.png" alt="axlr8r-logo" border="0">
#     </body>
#     </html>
#     """.format(invite.url)
#     part1 = MIMEText(text, "plain")
#     part2 = MIMEText(html, "html")
#     a.attach(part1)
#     a.attach(part2)

#     with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#         server.login("alphaaviral@gmail.com", password)
#         server.sendmail("alphaaviral@gmail.com","ph1200687@iitd.ac.in",a.as_string())
client.run(os.getenv("botpw"))