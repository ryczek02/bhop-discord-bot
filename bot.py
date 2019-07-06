import discord
from discord.ext import commands
import mysql.connector
import re
from steam import SteamID
import valve.source.a2s
import valve.rcon
 
###########################################################################
 
### DISCORD - SERVER CONFIGURATION
 
SERVER_ADDRESS = ("XXX.XX.XXX.XX", XXXXXX) # IP AND PORT
RCON_PASSWORD = "XXXXXXX" # RCON PASSWORD
SERVER_SQUARE_IMGURL = "XXX.XX/XXX.PNG"
 
### MYSQL CONFIGURATON
 
mydb = mysql.connector.connect(
  host="XXXXXXXX", # HOST
  user="XXXXXXXX", # USERNAME
  passwd="XXXXXXXX", # PASSWORD
  database="XXXXXXXX" # DATABASE
)

### BOT CONFIGURATION
TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # OAuth2 TOKEN
PLAYER_COMMANDS = 596859166446977024 # COMMANDS CHANNELID
CONSOLE_COMMANDS = 597108276945092672 # CONSOLE CHANNELID
VIP_CHANNEL = 597181870236762132 # VIP AUTH CHANNELID
 
###########################################################################
 
with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
    info = server.info()
    players = server.players()
 
bot = commands.Bot(command_prefix='.')

#########################
####### SEQUENCES #######
#########################
 
###TO DO: MAKE 12HOUR SEQUENCE THAT REFRESHING TOP10

CRSRECORDS = mydb.cursor()
 
CRSRECORDS.execute("select auth, count(auth) as attended from playertimes group by auth order by 2 desc limit 10;")
 
RECORD = CRSRECORDS.fetchall()
 

users = []
urls = []
for x in range(1):
    users.append("user" + str(x))
a=0
for y in users:
    y = SteamID(RECORD[a][0])
    y = y.community_url
    urls.append(y)
    a=a+1
 
###END TO DO

#########################
###   USER COMMANDS   ###
#########################


@bot.command()
async def bvip(ctx, arg):
    if ctx.message.channel.id == VIP_CHANNEL:
        sql2 = "UPDATE users SET vip = 1 WHERE auth = '" + arg + "';"
        crs = mydb.cursor(buffered=True)
        crs.execute(sql2)
        await mydb.commit()
 
@bot.command()
async def map(ctx, arg):
    if ctx.message.channel.id == PLAYER_COMMANDS:
        sql = "SELECT time, auth FROM playertimes WHERE map = '" + arg + "'"
        crs = mydb.cursor(buffered=True)
        crs.execute(sql)
        maptime = crs.fetchone()
        user = SteamID(maptime[1])
        user = user.community_url
        await ctx.send("Best time on map: ***" + arg + "*** is ***" + str(maptime[0]) + "*** sekund, ustanowiony przez " + user)
 
@bot.command()
async def maps(ctx):
    if ctx.message.channel.id == PLAYER_COMMANDS:
        sql = "SELECT DISTINCT map FROM playertimes"
        crs = mydb.cursor(buffered=True)
        crs.execute(sql)
        maptime = crs.fetchall()
        data = ""
        for x in maptime:
            data+="***" + x[0] + "***" +", "
        await ctx.send("Map list: " + data[:-2] + ".")
 
@bot.command()
async def top10(ctx):
    if ctx.message.channel.id == 596815597942210570:
        embed = discord.Embed(
            title = "By number of records",
            description = "",
            colour = discord.Colour.green()
        )
       
        user1 = SteamID(rekord[0][0])
        user1 = user1.community_url
        embed.set_thumbnail(url="SERVER_SQUARE_IMGURL")
        embed.set_author(name="Players rank")
        embed.add_field(name="1. " + urls[0], value="Records on server: " + str(RECORD[0][1]), inline=False)
        await ctx.send(embed=embed)
 
@bot.command()
async def sinfo(ctx):
    if ctx.message.channel.id == PLAYER_COMMANDS:
        embed = discord.Embed(
            title = "Name",
            description = "{server_name}".format(**info),
            colour = discord.Colour.green()
        )
 
        embed.set_thumbnail(url="SERVER_SQUARE_IMGURL")
        embed.set_author(name="SERVER STATS:")
        embed.add_field(name="Online players", value="{player_count}/{max_players}".format(**info), inline=False)
        embed.add_field(name="IP", value=SERVER_ADDRESS[0] + ":" + str(SERVER_ADDRESS[1]), inline=False)
        embed.add_field(name="Map", value="{map}".format(**info), inline=False)
 
        await ctx.send(embed=embed)
 
#########################
####     CONSOLE     ####
#########################
 
@bot.command()
async def c(ctx, *args):
    if ctx.message.channel.id == 597108276945092672:
        bc = ""
        for warg in args:
            bc += warg
            bc += " "
        print(bc)
        with valve.rcon.RCON(SERVER_ADDRESS, RCON_PASSWORD) as rcon:
            await ctx.send("Executing command: ***" + bc + "***")
            await ctx.send(rcon(bc))
            print(rcon(bc))
 
bot.run(TOKEN)
