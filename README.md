# Security Tools Discord Bot

A Discord bot that provides various security tools and reconnaissance capabilities including Nmap scanning, WHOIS lookup, subdomain enumeration, and more.

## Prerequisites

- Python 3.x
- Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications))
- Nmap (Manual installation required)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Prthiv/hecki-scanner
cd hecki-scanner
```

2. Install Nmap:
   - Download and install Nmap from the `tools` folder or from [Nmap's official website](https://nmap.org/download.html)
   - Make sure Nmap is added to your system's PATH

3. Install Python dependencies:
```bash
Every tools are In "/tools", add to Path if needed
```

4. Configure environment variables:
   - Create a `.env` file in the root directory
   - Add your Discord bot token:
```env
DISCORD_TOKEN=your_discord_bot_token_here
```

## Features

- **WHOIS Lookup**: Get domain registration information
- **Subdomain Enumeration**: Discover subdomains of a target domain
- **Nmap Scanning**: Perform network scans
- **IP Resolution**: Resolve domain names to IP addresses
- **Reconnaissance**: Various recon tools and utilities

## Usage

1. Start the bot:
```bash
python bot.py
```

2. Invite the bot to your Discord server using the OAuth2 URL from your Discord Developer Portal

3. Use the available commands in your Discord server

## Note

- The bot comes bundled with tools like WHOIS and Subfinder - no separate installation needed
- Only Nmap needs to be installed manually
- Make sure to follow security best practices and legal guidelines when using the tools
- Keep your Discord bot token secure and never share it publicly

## Contributing

Feel free to open issues or submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
