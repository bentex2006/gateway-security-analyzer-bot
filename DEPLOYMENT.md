# Deployment Guide

## Quick Start

### 1. Prerequisites
- Python 3.11 or higher
- Git
- Telegram Bot Token (from @BotFather)

### 2. Local Setup
```bash
git clone <repository-url>
cd gateway-security-analyzer-bot
cp .env.example .env
# Edit .env with your bot token and admin IDs
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 3. Environment Variables
Create `.env` file with:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=7581739321,6496521179
```

## Deployment Options

### Option 1: VPS Deployment (Recommended)
1. Clone repository to your VPS
2. Set up environment variables
3. Install dependencies
4. Use the provided systemd service file:
   ```bash
   sudo cp gateway-bot.service /etc/systemd/system/
   sudo systemctl enable gateway-bot
   sudo systemctl start gateway-bot
   ```

### Option 2: Docker Deployment
```bash
docker-compose up -d
```

### Option 3: GitHub Actions + VPS
1. Set up repository secrets:
   - `SERVER_HOST`: Your VPS IP
   - `SERVER_USER`: SSH username
   - `SERVER_KEY`: SSH private key
2. Push to main branch for automatic deployment

## Bot Commands

### User Commands
- `/start` - Welcome message with bot information
- `/help` - Display available commands
- `/url <website>` - Analyze a website

### Admin Commands
- `/approve <user_id>` - Approve user access
- `/groupuse <on/off>` - Enable/disable group usage
- `/auth <on/off>` - Toggle approval requirement
- `/stats` - View bot statistics

## Features
- Website security analysis
- SSL certificate validation
- Payment gateway detection
- CMS identification
- CAPTCHA system detection
- Cloudflare protection analysis
- Admin approval system
- Group usage controls

## Support
For issues or questions, contact the bot administrators.