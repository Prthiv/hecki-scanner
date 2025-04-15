import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import resolve_ip_or_domain, validate_domain_or_ip

class IpresolveCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ipresolve", description="Resolve a domain to IP or IP to hostname")
    @app_commands.describe(target="The domain or IP to resolve (e.g., example.com or 1.2.3.4)")
    async def ipresolve(self, interaction: discord.Interaction, target: str):
        await interaction.response.defer()

        try:
            if not validate_domain_or_ip(target):
                raise ValueError("Invalid domain or IP format")

            result = resolve_ip_or_domain(target)
            embed = discord.Embed(
                title=f"Resolution Report • {target}",
                color=discord.Color.from_rgb(88, 101, 242),  # Discord Blurple color
                description=f"Resolving {target}..."
            )
            embed.set_author(name="Security Analysis", icon_url="https://i.imgur.com/JLy9KkQ.png")
            embed.set_footer(text="Security Bot v2.0")
            embed.add_field(name="Status",
                            value="```⋯ Processing request```",
                            inline=False)
            
            loading_msg = await interaction.followup.send(embed=embed)
            
            embed.set_field_at(-1, name="📊 Resolution Progress",
                               value="```✅ Resolution completed!```",
                               inline=False)
            embed.add_field(name="📋 Resolution Results", value=f"```\n{result[:950]}\n```", inline=False)
            embed.description = f"🎉 Resolution complete for {target}!"
            embed.color = discord.Color.green()
            await interaction.followup.send(embed=embed)

        except Exception as e:
            error_embed = discord.Embed(
                title="Unable to Complete Resolution",
                description=str(e),
                color=discord.Color.from_rgb(237, 66, 69)  # Discord Red color
            )
            await interaction.followup.send(embed=error_embed)

async def setup(bot):
    await bot.add_cog(IpresolveCommand(bot))