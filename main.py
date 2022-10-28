# This example requires the 'message_content' intent.
import discord

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
    name=await commands.MemberConverter().convert(ctx,arg)
    if name is not None:
        await ctx.send(f"{name.mention} was bonked by {ctx.author.mention}")
        numbers = [1, 2, 3, 4]
        choice=random.choice(numbers)
        if choice == 1:
            f=discord.File('photos/bonk1.gif')
        if choice == 2:
            f=discord.File('photos/bonk2.gif')
        if choice == 3:
            f = discord.File('photos/bonk3.gif')
        if choice == 4:
            f = discord.File('photos/bonk4.gif')
        await ctx.send(file=f)

    else:
        await ctx.send("Could not Find that User")

@client.command()
async def beat(ctx,arg):
    name = await commands.MemberConverter().convert(ctx, arg)
    if name is not None:
        if name is ctx.author:
            await ctx.send(f"{name.mention} couldn't take it anymore and wanted to beat himself up")
            numbers = [1, 2, 3, 4]
            choice = random.choice(numbers)
            if choice == 1:
                f = discord.File('photos/selfbeat1.gif')
            if choice == 2:
                f = discord.File('photos/selfbeat2.gif')
            if choice == 3:
                f = discord.File('photos/selfbeat3.gif')
            if choice == 4:
                f = discord.File('photos/selfbeat4.gif')
            await ctx.send(file=f)
        else:
            await ctx.send(f"{name.mention} got beaten up by {ctx.author.mention}")
            numbers = [1, 2, 3, 4]
            choice = random.choice(numbers)
            if choice == 1:
                f = discord.File('photos/beat1.gif')
            if choice == 2:
                f = discord.File('photos/beat2.gif')
            if choice == 3:
                f = discord.File('photos/beat3.gif')
            if choice == 4:
                f = discord.File('photos/beat4.gif')
            await ctx.send(file=f)

    else:
        await ctx.send("Could not Find that User")

client.run(token)