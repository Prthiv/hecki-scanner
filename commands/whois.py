import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import run_whois, validate_domain

class WhoisCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="whois", description="Perform WHOIS lookup on a domain")
    @app_commands.describe(domain="The domain to lookup (e.g., example.com)")
    async def whois(self, interaction: discord.Interaction, domain: str):
        await interaction.response.defer()

        try:
            if not validate_domain(domain):
                raise ValueError("Invalid domain format")

            # Initialize embed with enhanced design
            embed = discord.Embed(
                title=f"WHOIS Report • {domain}",
                color=discord.Color.from_rgb(88, 101, 242),  # Discord Blurple color
                description=f"Initiating WHOIS lookup for {domain}..."
            )
            embed.set_author(name="Security Analysis", icon_url="https://i.imgur.com/JLy9KkQ.png")
            embed.set_footer(text="Security Bot v2.0")
            embed.add_field(name="Status", value="```⋯ Initializing lookup```", inline=False)
            
            # Send initial loading message
            loading_msg = await interaction.followup.send(embed=embed)
            
            # Update with scan progress
            embed.set_field_at(-1, name="📊 Scan Progress", value="```🔍 WHOIS lookup in progress...```", inline=False)
            await loading_msg.edit(embed=embed)
            
            result = run_whois(domain)
            
            # Finalize with results
            embed.set_field_at(-1, name="📊 Scan Progress", value="```✅ WHOIS lookup completed!```", inline=False)
            embed.add_field(name="📋 WHOIS Information", value=f"```\n{result[:950] or 'No WHOIS data available'}\n```", inline=False)
            embed.description = f"🎉 WHOIS lookup completed for {domain}!"
            embed.color = discord.Color.green()
            await loading_msg.edit(embed=embed)

        except Exception as e:
            error_embed = discord.Embed(
                title="Unable to Complete Lookup",
                description=str(e),
                color=discord.Color.from_rgb(237, 66, 69)  # Discord Red color
            )
            await interaction.followup.send(embed=error_embed)

async def setup(bot):
    await bot.add_cog(WhoisCommand(bot))