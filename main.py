import discord
from discord.ext import commands
import random
import time
import asyncio
import async_timeout
import datetime
import platform
import requests
import urllib.parse

startTime = int(time.time())
colorTable = [
    0xFF0000,
    0xFFFF00,
    0x00FF00,
    0x00FFFF,
    0x0000FF,
    0xFF00FF,
]
adminTable = [
    "490248803837018112"
]
interval = 1
Prefix = "r!"
token = "TOKEN"
client = commands.Bot(command_prefix="r!")
client.remove_command("help")


def log(Mystring):
    print(Mystring)


@client.command(pass_context=True)
async def invite(ctx):
    await client.say("<@{}> the link : http://le-dev-ttatane.fun/bot/rainbow/".format(ctx.message.author.id))


@client.command(pass_context=True)
async def support(ctx):
    await client.say("<@{}> the link : https://discord.gg/gDRBhDm".format(ctx.message.author.id))

@client.command()
async def help():
    embed = discord.Embed(title="help", color=colorTable[random.randint(0, len(colorTable) - 1)])
    embed.add_field(name=Prefix+"stats", value="view bot stats", inline=False)
#    embed.add_field(name=Prefix+"PythonInfo", value="get Python info (dev)", inline=False)
    embed.add_field(name=Prefix+"invite", value="get link to invite", inline=False)
    embed.add_field(name=Prefix+"support",value="get link to join support", inline=False)
    embed.set_footer(text="by disbot Team")
    await client.say(embed=embed)

@client.command(pass_context=True)
async def logout(ctx):
    if ctx.message.author.id in adminTable:
        await client.logout()
        await client.close()
        exit()
    else:
        client.say("**NOPE**")

@client.command()
async def stats():
    embed = discord.Embed(title="stats", color=colorTable[random.randint(0, len(colorTable) - 1)])
    embed.add_field(name="role rainbow Number", value=str(NumberRainbow), inline=True)
    embed.add_field(name="time of this session", value=str(str(datetime.timedelta(seconds=(int(time.time() - startTime))))), inline=True)
    embed.add_field(name="Server Number", value=str(len(client.servers)), inline=True)
    embed.set_footer(text="by disbot Team")
    await client.say(embed=embed)


#@client.command()
#async def PythonInfo():
#    embed = discord.Embed(title="Python Info", color=colorTable[random.randint(0, len(colorTable) - 1)])
#    embed.add_field(name="Bits", value=platform.architecture()[0], inline=True)
#    embed.add_field(name="Os", value=str(platform.system()+" "+platform.release()), inline=True)
#    embed.add_field(name="Python Version", value=str(platform.python_version()), inline=True)
#    embed.add_field(name="Python Compiler", value=str(platform.python_compiler()), inline = False)
#    embed.add_field(name="Machine", value=str(platform.machine()), inline=True)
#    embed.add_field(name="Processor", value=str(platform.processor()), inline=True)
#    embed.set_footer(text="by disbot Team")
#    await client.say(embed=embed)d)

def GetRoleById(ID):
    for server in client.servers:
        for role in server.roles:
            if role.id == ID:
                return role
    else:
        return False


def GetServerById(ID):
    for server in client.servers:
        if server.id == ID:
            return server
    return False

def GetAllRainBowRole(before_role_table):
    after_role_table = []
    for server in client.servers:
        for role in server.roles:
            if role.name.upper() == "RAINBOW" or "[RB]" in role.name.upper():
                after_role_table.append(role)
                after_role_table.append(server)
    i = 0
    while i < len(after_role_table):
        if not after_role_table[i] in before_role_table:
            log("[ LOG ] : role {} added in list".format(after_role_table[i].id))
        i += 2
    while i < len(before_role_table):
        if not before_role_table[i] in after_role_table:
            log("[ LOG ] : role {} remove in list".format(before_role_table[i].id))
        i += 2
    return after_role_table

async def role_task():
    while True:
        try:
            message_no_permission_role = []
            role_table = []
            role_table = GetAllRainBowRole(role_table)
            global NumberRainbow
            NumberRainbow = int(len(role_table) / 2)
            localtime = int(time.time())
            while True:
                i = 0
                for color in colorTable:
                    while i < len(role_table):
                        try:
                            await client.edit_role(role=role_table[i], server=role_table[i+1], colour=discord.Colour(color))
                            asyncio.sleep(1)
                        except discord.Forbidden:
                            if not role_table[i].id in message_no_permission_role:
                                debug = True
                                for channel in role_table[i+1].channels:
                                    if str(channel.type) == "text" and debug:
                                        try:
                                            embed = discord.Embed(title="ERROR", color=0xFF0000)
                                            embed.set_thumbnail(url="https://y2uysw.db.files.1drv.com/y4mzHf-4Px05YSIig8G4HifTxCvt95L6H7Tc3EPST8nuapNIiUBI1YZInUrb-0_HVwbrgemhR4IiJJj5nkAQhV0mf0ASESZMIVypjq4wX1v2x3Zs2if_pZ6ibxLNXBfzaJXGPXqbw5YavISZp2BF3HPPxgIga7Q3tk5LIC1i0fkWQgsw7USzCMG6w6EjCOPklH_5Q4sEk_w_BO62Pr2IbLBLw")
                                            embed.add_field(name="forbidden", value="I can not change the role of <@&{}> because I do not have permission".format(role_table[i].id), inline=False)
                                            await client.send_message(channel, embed=embed)
                                            message_no_permission_role.append(role_table[i].id)
                                            debug = False
                                        except:
                                            pass
                        except Exception as e:
                            log("[ ERROR ] : "+str(e))
                        i += 2
                    asyncio.sleep(interval / 1000)
                    i = 0
                if (localtime + 10) < int(time.time()):
                    role_table = GetAllRainBowRole(role_table)
                    NumberRainbow = int(len(role_table) / 2)
                    localtime = int(time.time())
        except Exception as e:
            log("Error : "+str(e))


@client.event
async def on_server_join(server):
    log("[ LOG ] : {} joined ".format(server.name))
    embed = discord.Embed(title="help")
    embed.add_field(name="Step 1", value="create role named : rainbow", inline=False)
    embed.add_field(name="Step 2", value="wait 10 seconds if the role does not change color there is a problem", inline=False)
    embed.set_footer(text="by disbot Team")
    for channel in server.channels:
        if str(channel.type) == "text":
            await client.send_message(channel, embed=embed)
            return True

@client.event
async def on_ready():
        log('Logged in as')
        log(client.user.name)
        log(client.user.id)
        log('------')
        client.loop.create_task(role_task())
        await client.change_presence(game=discord.Game(name="r!help | By Ttatanepvp123"))

client.run(token)
