from aternosapi import AternosAPI
import discord
from discord.ext import commands, tasks

headers_cookie = "Headers Cookie"
TOKEN = "Token"
server = AternosAPI(headers_cookie, TOKEN)

client = commands.Bot(command_prefix = ["-"])
client.remove_command('help')

async def cmd(cmd, ctx):
    if cmd == "start":
        await ctx.send(server.StartServer())
    elif cmd == "stop":
        await ctx.send(server.StopServer())
    elif cmd == "status":
        await ctx.send(server.GetStatus())
    elif cmd == "info":
        await ctx.send(server.GetServerInfo())

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game('Watching over the SMP'))
    print('Initialized!')

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Current Commands", description="A description", color=0x00ff00)
    embed.add_field(name="start", value="Starts the server.", inline=True)
    embed.add_field(name="stop", value="Stops the server.", inline=True)
    embed.add_field(name="status", value="Shows the current status of the server.", inline=True)
    embed.add_field(name="info", value="Shows server information.", inline=True)
    await ctx.send(embed = embed)

@client.command()
async def start(ctx):
    await ctx.send("Starting...")
    await cmd("start", ctx)

@client.command()
async def stop(ctx):
    await ctx.send("Stopping...")
    await cmd("stop", ctx)

@client.command()
async def info(ctx):
    await cmd("info", ctx)

@client.command()
async def status(ctx):
    await cmd("status", ctx)
        
client.run("Token")
