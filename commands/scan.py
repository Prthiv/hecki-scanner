import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import run_nmap_scan, validate_domain_or_ip

class ScanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="scan", description="Scan ports on a domain or IP")
    @app_commands.describe(target="The domain or IP to scan (e.g., example.com or 1.2.3.4)")
    async def scan(self, interaction: discord.Interaction, target: str):
        await interaction.response.defer()

        try:
            if not validate_domain_or_ip(target):
                raise ValueError("Invalid domain or IP format")

            # Initialize embed with enhanced design
            embed = discord.Embed(
                title=f"Port Scan Report • {target}",
                color=discord.Color.from_rgb(88, 101, 242),  # Discord Blurple color
                description=f"Initiating port scan for {target}..."
            )
            embed.set_author(name="Security Analysis", icon_url="https://i.imgur.com/JLy9KkQ.png")
            embed.set_footer(text="Security Bot v2.0")
            embed.add_field(name="Status", value="```⋯ Initializing scan```", inline=False)
            
            # Send initial loading message
            loading_msg = await interaction.followup.send(embed=embed)
            
            # Update with scan progress
            embed.set_field_at(-1, name="📊 Scan Progress", value="```🔍 Scanning ports in progress...```", inline=False)
            await loading_msg.edit(embed=embed)
            
            result = run_nmap_scan(target)
            
            # Finalize with results
            embed.set_field_at(-1, name="📊 Scan Progress", value="```✅ Port scan completed!```", inline=False)
            embed.add_field(name="🔌 Port Scan Results", value=f"```\n{result[:950] or 'No open ports detected'}\n```", inline=False)
            embed.description = f"🎉 Port scan completed for {target}!"
            embed.color = discord.Color.green()
            await loading_msg.edit(embed=embed)

        except Exception as e:
            error_embed = discord.Embed(
                title="Unable to Complete Scan",
                description=str(e),
                color=discord.Color.from_rgb(237, 66, 69)  # Discord Red color
            )
            await interaction.followup.send(embed=error_embed)

async def setup(bot):
    await bot.add_cog(ScanCommand(bot))