import discord
from discord.ext import commands
import os

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

client = commands.Bot(command_prefix=".")
client.remove_command("help")
token = os.getenv("DISCORD_BOT_TOKEN")

max_tokens = int(os.getenv("MAX_TOKENS",14))

@client.event
async def on_ready() :
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("Listening to .help"))
    print("I am online")

@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title="Help", description="")
    em.add_field(name="ai functions", value=".ai \"<prompt>\", for example: ```.ai \"Who wrote staying alive?\"```")
    await ctx.send(embed=em)
@client.command()
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

@client.command(name="whoami")
async def whoami(ctx) :
    await ctx.send(f"You are {ctx.message.author.name}")

@client.command()
async def clear(ctx, amount=3) :
    await ctx.channel.purge(limit=amount)

@client.command()
async def ai(ctx, toprompt="") :
    if toprompt == "":
        await ctx.send(f"Answer: You forgot to provide me a question, dumbass")
    else:
        question = f"Bot answers user's questions.\nUser: {toprompt}\nBot: "
        print(question)
        response = openai.Completion.create(engine="davinci", prompt=question, max_tokens=max_tokens, stop=".")
        choises = response["choices"]
        print(response)
        if len(choises) > 0:
            await ctx.send(f"Answer: {choises[0]['text']}")

client.run(token)
