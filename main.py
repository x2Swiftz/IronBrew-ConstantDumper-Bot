import requests
import discord
from discord.ext import commands
import json
from datetime import date
import io
import os
from discord.utils import get
import lupa
lua = lupa.LuaRuntime(unpack_returned_tuples=True)
bot_config = json.loads(open("config.json", "r").read())
client = commands.Bot(command_prefix=bot_config["bot_prefix"])






@client.event
async def on_ready():
	print("Bot is ready!")


@client.command(pass_context=True)
async def ping(ctx):
	await ctx.send("> `Pong! " + str(round(client.latency * 1000)) + "ms`")


@client.command(pass_context=True)
async def const(ctx, *args):
	today = date.today()
	# await client.delete_message(ctx.message)

	try:
		attachment_url = ctx.message.attachments[0].url
		script_to_obfuscate = str(requests.get(attachment_url).text)
		f=open('script.lua')  
		f1=open('process.lua','w')
		for x in f.readlines():
				f1.write(x)
		f.close()
		f1.close()
		fin = open("process.lua", "rt")
		data = fin.read()
		data = data.replace('--here', script_to_obfuscate)
		fin.close()
		#open the input file in write mode
		fin = open("process.lua", "wt")
		#overrite the input file with the resulting data
		fin.write(data)
		#close the file
		fin.close()
		data = lua.execute(open('process.lua').read())
		whitelist = open("constants.txt", "r")
		whitelist_to = whitelist.read()
	except:
			script_to_obfuscate = "none"
	if script_to_obfuscate == "none":
		await ctx.send("> `Error lmao`")
	else:
		if whitelist_to != "The file weren't able to be found !" and whitelist_to != script_to_obfuscate:
			d1 = str(today.strftime("%m") + "_" + today.strftime("%d") + "_" + today.strftime("%y"))
			f = io.StringIO(whitelist_to)
			await ctx.channel.send(content="> `Constant dumping completed!`",
			file=discord.File(f, d1 + "_constants" + ".txt"))
		else:
			embed = discord.Embed(title=bot_config["bot_name"], description="", color=0xFF0000)
			embed.add_field(name="Error", value="`Syntax Error.`", inline=False)
			embed.set_footer(text=bot_config["bot_name"] + " | " + str(
				today.strftime("%m") + "/" + today.strftime("%d") + "/" + today.strftime("%y")))
			await ctx.send(embed=embed)


client.run(bot_config["bot_token"])