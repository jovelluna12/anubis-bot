import discord
from keep_alive import keep_alive
import random
from discord.ext import commands
import os
from dotenv import load_dotenv
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO

load_dotenv()
token=os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()

intents.message_content = True
intents.members=True
intents.presences=True

client=commands.Bot(command_prefix="anubis-",intents=intents)

@client.event
async def on_ready():
    pass

@client.event
async def on_member_join(member):

    avatar_bytes=await member.display_avatar.read()

    img=Image.open("photo.jpg")
    font=ImageFont.truetype('Blackout.otf',24)
    draw=ImageDraw.Draw(img)

    img2 = Image.open(BytesIO(avatar_bytes))
    img2.resize((80,80),box=(50,50,200,200)).save("img2.png")

    img_paste=Image.open("img2.png")
    Image.Image.paste(img, img_paste, (115, 10))
    membername=str(member.name)
    text="Welcome to the Server"
    text2=f"{membername}"

    draw.text((52, 100),text,(235,227,227),font=font)
    draw.text((80, 130), text2, (235, 227, 227), font=font)
    img.save("welcome.png")

    try:
        channel=member.guild.system_channel
        await channel.send(f"Hello {member.mention}, welcome to {member.guild}")
        await channel.send(file=discord.File("welcome.png"))

        os.remove('welcome.png')
        os.remove('img2.png')

    except discord.Forbidden:
        pass

@client.command()
async def bonk(ctx, arg):
    try:
        name=await commands.MemberConverter().convert(ctx,arg)
        if name is not None:
            if name is ctx.author:
                await ctx.send(f"{ctx.author.mention} realized he was getting sus and bonked himself!")
                await ctx.send(file=discord.File('photos/selfbonk.gif'))
            else:
                await ctx.send(f"{name.mention} was bonked by {ctx.author.mention}")

                choice=[discord.File('photos/bonk1.gif'),discord.File('photos/bonk2.gif'),discord.File('photos/bonk3.gif'),discord.File('photos/bonk4.gif')]
                f=random.choice(choice)
                await ctx.send(file=f)
    except discord.ext.commands.errors.MemberNotFound:
        await ctx.send("Could not Find that User")

@client.command()
async def beat(ctx,arg):
    try:
        name = await commands.MemberConverter().convert(ctx, arg)
        if name is not None:
            if name is ctx.author:
                await ctx.send(f"{name.mention} couldn't take it anymore and wanted to beat himself up")
                selfbeat=[discord.File('photos/selfbeat1.gif'),discord.File('photos/selfbeat2.gif'),discord.File('photos/selfbeat3.gif'),discord.File('photos/selfbeat4.gif')]
                f = random.choice(selfbeat)
                await ctx.send(file=f)
            else:
                await ctx.send(f"{name.mention} got beaten up by {ctx.author.mention}")
                beat=[discord.File('photos/beat1.gif'),discord.File('photos/beat2.gif'),discord.File('photos/beat3.gif'),discord.File('photos/beat4.gif')]
                f = random.choice(beat)
                await ctx.send(file=f)
    except discord.ext.commands.errors.MemberNotFound:
        await ctx.send("Could not Find that User")
keep_alive()
try:
  client.run(token)
except:
  os.system("kill 1")