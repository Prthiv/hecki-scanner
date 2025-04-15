import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import run_sublist3r, validate_domain

class SubdomainsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="subdomains", description="Enumerate subdomains for a domain")
    @app_commands.describe(domain="The domain to enumerate (e.g., example.com)")
    async def subdomains(self, interaction: discord.Interaction, domain: str):
        await interaction.response.defer()

        try:
            if not validate_domain(domain):
                raise ValueError("Invalid domain format")

            # Initialize embed with enhanced design
            embed = discord.Embed(
                title=f"Subdomain Report • {domain}",
                color=discord.Color.from_rgb(88, 101, 242),  # Discord Blurple color
                description=f"Initiating subdomain enumeration for {domain}..."
            )
            embed.set_author(name="Security Analysis", icon_url="https://i.imgur.com/JLy9KkQ.png")
            embed.set_footer(text="Security Bot v2.0")
            embed.add_field(name="Status", value="```⋯ Initializing scan```", inline=False)
            
            # Send initial loading message
            loading_msg = await interaction.followup.send(embed=embed)
            
            # Update with scan progress
            embed.set_field_at(-1, name="📊 Scan Progress", value="```🔍 Searching for subdomains...```", inline=False)
            await loading_msg.edit(embed=embed)
            
            subdomains = run_sublist3r(domain)
            
            # Finalize with results
            embed.set_field_at(-1, name="📊 Scan Progress", value="```✅ Subdomain search completed!```", inline=False)
            subdomain_text = "\n".join(subdomains[:20]) if subdomains else "No subdomains detected"
            embed.add_field(name="🌐 Subdomains Discovered", value=f"```\n{subdomain_text[:950]}\n```", inline=False)
            embed.description = f"🎉 Subdomain enumeration completed for {domain}!"
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
    await bot.add_cog(SubdomainsCommand(bot))