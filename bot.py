import discord
from discord.ext import commands
import os
import asyncio
import sys

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import logging
from dotenv import load_dotenv
from commands.recon import ReconCommand
from commands.whois import WhoisCommand
from commands.scan import ScanCommand
from commands.subdomains import SubdomainsCommand
from commands.ipresolve import IpresolveCommand


from utils.helpers import clear_log_file

# Load environment variables from .env
load_dotenv()

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(filename='logs/recon.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Register commands
async def setup_bot():
    await bot.add_cog(ReconCommand(bot))
    await bot.add_cog(WhoisCommand(bot))
    await bot.add_cog(ScanCommand(bot))
    await bot.add_cog(SubdomainsCommand(bot))
    await bot.add_cog(IpresolveCommand(bot))
    await bot.add_cog(SubdirCommand(bot))


@bot.command(name='clear_log')
async def clear_log(ctx):
    """Clear the recon.log file"""
    success = clear_log_file()
    if success:
        await ctx.send('Recon log cleared successfully!')
    else:
        await ctx.send('Failed to clear recon log. Check logs for details.')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await setup_bot()
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Error syncing commands: {e}')

# Run the bot
if __name__ == '__main__':
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    if not DISCORD_TOKEN:
        raise ValueError("DISCORD_TOKEN not set in .env file")
    bot.run(DISCORD_TOKEN)