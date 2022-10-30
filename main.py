import asyncio
import io

import discord
from keep_alive import keep_alive
import random
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO
import requests,json,aiohttp

load_dotenv()
token=os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()

intents.message_content = True
intents.members=True
intents.presences=True

description="A Basic BOT with Limited Functionalities"

client=commands.Bot(command_prefix="anubis-",description=description,help_command=None,intents=intents)

@client.event
async def on_ready():
    try:
        await client.tree.sync()
        print("Ready")
    except Exception as e:
        print(e)
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
        await channel.send(f"Hello {member.mention}, welcome to {member.guild}",file=discord.File("welcome.png"))

        os.remove('welcome.png')
        os.remove('img2.png')

    except discord.Forbidden:
        pass

@client.command()
async def bonk(ctx, user_to_bonk):
    async with ctx.channel.typing():
        await asyncio.sleep(1)
    try:
        name=await commands.MemberConverter().convert(ctx,user_to_bonk)
        if name is not None:
            if name is ctx.author:
                await ctx.reply(f"{ctx.author.mention} realized he was getting sus and bonked himself!",file=discord.File('photos/selfbonk.gif'))
            else:
                choice=[
                    discord.File('photos/bonk1.gif'),
                    discord.File('photos/bonk2.gif'),
                    discord.File('photos/bonk3.gif'),
                    discord.File('photos/bonk4.gif')
                        ]
                f=random.choice(choice)
                await ctx.reply(f"{name.mention} was bonked by {ctx.author.mention}",file=f)
    except discord.ext.commands.errors.MemberNotFound:
        await ctx.reply("Could not Find that User")

@client.command()
async def beat(ctx,user_to_beat):
    async with ctx.channel.typing():
        await asyncio.sleep(1)
    try:
        name = await commands.MemberConverter().convert(ctx, user_to_beat)
        if name is not None:
            if name is ctx.author:
                selfbeat = [
                    discord.File('photos/selfbeat1.gif'),
                    discord.File('photos/selfbeat2.gif'),
                    discord.File('photos/selfbeat3.gif'),
                    discord.File('photos/selfbeat4.gif')
                ]
                f = random.choice(selfbeat)
                await ctx.reply(f"{name.mention} couldn't take it anymore and wanted to beat himself up",file=f)
            else:
                beat = [
                    discord.File('photos/beat1.gif'),
                    discord.File('photos/beat2.gif'),
                    discord.File('photos/beat3.gif'),
                    discord.File('photos/beat4.gif')
                ]
                f = random.choice(beat)
                await ctx.reply(f"{name.mention} got beaten up by {ctx.author.mention}",file=f)
    except discord.ext.commands.errors.MemberNotFound:
        await ctx.reply("Could not Find that User")

@client.tree.command(name="confess")
@app_commands.describe(receiver="Message Receiver",message="The Message")
async def confess(interaction: discord.Interaction, receiver: discord.Member,message: str):
    await interaction.response.send_message(f"Message Successfully Sent",ephemeral=True)
    channel=interaction.channel
    created_at=interaction.created_at.strftime("%B-%d-%Y %H:%M:%S")
    await channel.send(f"> Anonymous Messaging\n> To: {receiver.mention}\n> {message}\n> \n> Message Created at: {created_at}")

@client.command()
async def joke(ctx):
    if ctx.message.content=="anubis-joke":
        # Link for Joke API: https://github.com/15Dkatz/official_joke_api
        endpoint="https://official-joke-api.appspot.com/random_joke"
        joke=requests.get(endpoint)
        joke_text=json.loads(joke.text)
        setup=joke_text["setup"]
        punchline=joke_text["punchline"]
        await ctx.reply(f"{setup}\n{punchline}")
    else:
        ctx.message.delete()
        ctx.send("Invalid Command. Make sure that you Invoked the Right Command with no Spelling Mistakes")

@client.command()
async def meme(ctx):
    if ctx.message.content=="anubis-meme":
        # Link for Meme API: https://github.com/D3vd/Meme_Api
        endpoint="https://meme-api.herokuapp.com/gimme"
        meme=requests.get(endpoint)
        meme_preview=json.loads(meme.text)
        preview=meme_preview["preview"][2]

        async with aiohttp.ClientSession() as session:
            async with session.get(preview) as url:
                img=await url.read()
                with open("meme_image.jpg","wb") as handle:
                    handle.write(img)

                await ctx.reply(file=discord.File("meme_image.jpg"))
                os.remove("meme_image.jpg")
    else:
        ctx.send("Invalid Command. Make sure that you Invoked the Right Command with no Spelling Mistakes")


@client.command()
async def help (ctx):
    if ctx.message.content=="anubis-help":
        await ctx.reply("```Commands List\n\nNon-Slash Commands\nCommand Prefix: anubis-\nhelp: Views this Help Message\nbonk: Bonks a User\nbeat: Beats a User\njoke: Sends a Random Joke\nmeme: Sends a Random Meme\n\nSlash Commands\nconfess: Sends Anonymous Message\n\nSend anubis-help_{name-of-command} for more Details about that Command```")
    else:
        await ctx.reply("Invalid Command. Make sure that you Invoked the Right Command with no Spelling Mistakes")

@client.command()
async def help_joke(ctx):
    if ctx.message.content=="anubis-help_joke":
        await ctx.reply('```Joke\nNon-Slash Command\nSends a Random Joke\n\nArguments: None \nAll Jokes were taken at https://github.com/15Dkatz/official_joke_api```')
    else:
        await ctx.reply("Invalid Command. Make sure that you Invoked the Right Command with no Spelling Mistakes")

@client.command()
async def help_meme(ctx):
    if ctx.message.content=="anubis-help_meme":
        await ctx.reply('```Meme\nNon-Slash Command\nSends a Random Meme\n\nArguments: None \nAll Memes were taken at https://github.com/D3vd/Meme_Api```')
    else:
        await ctx.reply("Invalid Command. Make sure that you Invoked the Right Command with no Spelling Mistakes")

@client.command()
async def help_bonk(ctx):
    if ctx.message.content=="anubis-help_bonk":
        await ctx.reply('```Bonk\nNon-Slash Command\nBonks a User\n\nArguments: user_to_bonk: Name of User to Bonk: This can be a User name in Plain Text, a User Name with Tag, or the User Mentioned ```')
    else:
        await ctx.reply("Invalid Command. Make sure that you Invoked the Right Command with no Spelling Mistakes")
@client.command()
async def help_beat(ctx):
    if ctx.message.content=="anubis-help_beat":
        await ctx.reply('```Beat\nNon-Slash Command\nBeat a User\n\nArguments: user_to_beat: Name of User to Beat. This can be a User name in Plain Text, a User Name with Tag, or the User Mentioned ```')
    else:
        await ctx.reply("Invalid Command. Make sure that you Invoked the Right Command with no Spelling Mistakes")
@client.command()
async def help_confess(ctx):
    if ctx.message.content=="anubis-help_confess":
        await ctx.reply('```Confess\nSlash Command\nSend Anonymous Message to a User\n\nArguments: Name of Receiver```')
    else:
        await ctx.reply("Invalid Command. Make sure that you Invoked the Right Command with no Spelling Mistakes")
# @client.event
# async def on_command_error(ctx,error):
#     await ctx.reply(f"Invalid Command\n{error}")

keep_alive()
try:
  client.run(token)

except:
  os.system("kill 1")