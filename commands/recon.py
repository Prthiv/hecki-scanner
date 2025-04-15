import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import run_whois, run_nmap_scan, run_sublist3r, validate_domain

class ReconCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="recon", description="Perform full reconnaissance on a domain")
    @app_commands.describe(domain="The domain to recon (e.g., example.com)")
    async def recon(self, interaction: discord.Interaction, domain: str):
        await interaction.response.defer()  # Defer for long-running tasks

        try:
            # Validate domain
            if not validate_domain(domain):
                raise ValueError("Invalid domain format")

            # Initialize embed with enhanced design
            embed = discord.Embed(
                title=f"Recon Report • {domain}",
                color=discord.Color.from_rgb(88, 101, 242),  # Discord Blurple color
                description=f"Initiating comprehensive scan for {domain}..."
            )
            embed.set_author(name="Security Analysis", icon_url="https://i.imgur.com/JLy9KkQ.png")
            embed.set_footer(text="Security Bot v2.0")
            embed.add_field(name="Status", value="```⋯ Initializing scan```", inline=False)
            
            # Send initial loading message
            loading_msg = await interaction.followup.send(embed=embed)
            
            # WHOIS lookup with enhanced progress indicator
            embed.set_field_at(-1, name="📊 Scan Progress", value="```🔍 WHOIS lookup in progress...```", inline=False)
            await loading_msg.edit(embed=embed)
            whois_result = run_whois(domain)
            embed.set_field_at(-1, name="📊 Scan Progress", value="```✅ WHOIS lookup completed!```", inline=False)
            
            # Split WHOIS results into chunks if needed
            whois_chunks = [whois_result[i:i+1000] for i in range(0, len(whois_result), 1000)]
            for i, chunk in enumerate(whois_chunks):
                field_name = "📋 WHOIS Information" if i == 0 else "📋 WHOIS Information (continued)"
                embed.add_field(name=field_name, value=f"```\n{chunk}\n```", inline=False)
            
            # Nmap scan with enhanced progress indicator
            embed.set_field_at(-1, name="📊 Scan Progress", value="```🔍 Port scanning in progress...```", inline=False)
            await loading_msg.edit(embed=embed)
            nmap_result = run_nmap_scan(domain)
            embed.set_field_at(-1, name="📊 Scan Progress", value="```✅ Port scan completed!```", inline=False)
            
            # Split port scan results into chunks if needed
            nmap_chunks = [nmap_result[i:i+1000] for i in range(0, len(nmap_result), 1000)]
            for i, chunk in enumerate(nmap_chunks):
                field_name = "🔌 Port Scan Results" if i == 0 else "🔌 Port Scan Results (continued)"
                embed.add_field(name=field_name, value=f"```\n{chunk}\n```", inline=False)
            
            # Subdomain enumeration with enhanced progress indicator
            embed.set_field_at(-1, name="📊 Scan Progress", value="```🔍 Searching for subdomains...```", inline=False)
            await loading_msg.edit(embed=embed)
            subdomains = run_sublist3r(domain)
            embed.set_field_at(-1, name="📊 Scan Progress", value="```✅ Subdomain search completed!```", inline=False)
            
            # Format and split subdomain results into chunks if needed
            if subdomains:
                subdomain_text = "\n".join(subdomains)
                subdomain_chunks = [subdomain_text[i:i+1000] for i in range(0, len(subdomain_text), 1000)]
                for i, chunk in enumerate(subdomain_chunks):
                    field_name = "🌐 Subdomains Discovered" if i == 0 else "🌐 Subdomains Discovered (continued)"
                    embed.add_field(name=field_name, value=f"```\n{chunk}\n```", inline=False)
            else:
                embed.add_field(name="🌐 Subdomains Discovered", value="```\nNo subdomains detected\n```", inline=False)
            
            # Finalize with enhanced completion message
            embed.description = f"🎉 Comprehensive scan completed for {domain}!"
            embed.color = discord.Color.green()
            embed.set_field_at(-1, name="📊 Scan Progress", value="```🏁 All tasks completed successfully!```", inline=False)
            embed.set_footer(text="🔒 Security Bot v2.0 | Scan completed", icon_url="https://i.imgur.com/JLy9KkQ.png")
            await loading_msg.edit(embed=embed)

        except Exception as e:
            error_embed = discord.Embed(
                title="Unable to Complete Scan",
                description=str(e),
                color=discord.Color.from_rgb(237, 66, 69)  # Discord Red color
            )
            await interaction.followup.send(embed=error_embed)

async def setup(bot):
    await bot.add_cog(ReconCommand(bot))