# Gateway Security Analyzer Bot

A comprehensive Telegram bot for website security and technology analysis. This bot analyzes websites for various security features, payment systems, technology stacks, and security configurations.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://telegram.org/)

## 🚀 Features

### Website Analysis
- **Cloudflare Detection**: Identifies Cloudflare protection and CDN services
- **CAPTCHA Systems**: Detects reCAPTCHA, hCaptcha, Turnstile, and other bot protection
- **GraphQL Endpoints**: Discovers GraphQL APIs and playground interfaces
- **CMS Detection**: Identifies WordPress, WooCommerce, Shopify, and other platforms
- **Payment Gateways**: Detects Stripe, PayPal, Square, and 20+ payment providers
- **SSL Analysis**: Certificate validation, expiry dates, and security configuration
- **Security Headers**: Analyzes HSTS, CSP, X-Frame-Options, and modern security headers
- **WAF Detection**: Identifies Web Application Firewalls and security services

### Bot Management
- **Admin Controls**: User approval system with configurable access
- **Group Support**: Enable/disable bot usage in groups
- **Authentication Toggle**: Flexible approval requirements
- **Professional Formatting**: Animated GIFs and styled responses

## 📋 What It Analyzes

### Security Features
- SSL/TLS certificates and configuration
- Security headers (HSTS, CSP, X-Frame-Options, etc.)
- Web Application Firewall (WAF) detection
- Cloudflare and CDN services
- CAPTCHA and bot protection systems

### Technology Stack
- Content Management Systems (WordPress, Shopify, etc.)
- E-commerce platforms (WooCommerce)
- GraphQL endpoints and APIs
- Server technologies and frameworks

### Payment Systems
- Payment gateways (Stripe, PayPal, Square, etc.)
- E-commerce checkout processes
- Credit card form detection
- Shopping cart functionality

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- A Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Your Telegram User ID

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/gateway-security-analyzer-bot.git
   cd gateway-security-analyzer-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your bot token and admin IDs
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

### Docker Setup

1. **Using Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Using Docker directly**
   ```bash
   docker build -t gateway-analyzer-bot .
   docker run -d --env-file .env gateway-analyzer-bot
   ```

## 🚀 Deployment

### GitHub Actions (Recommended)

1. **Fork this repository**

2. **Set up repository secrets**
   - Go to Settings → Secrets and variables → Actions
   - Add these secrets:
     - `BOT_TOKEN`: Your Telegram bot token
     - `ADMIN_IDS`: Comma-separated admin user IDs
     - `SERVER_HOST`: Your VPS IP address
     - `SERVER_USER`: VPS username
     - `SERVER_KEY`: SSH private key

3. **Deploy automatically**
   - Push to main branch
   - GitHub Actions will deploy to your VPS

### Manual VPS Deployment

1. **Connect to your VPS**
   ```bash
   ssh user@your-vps-ip
   ```

2. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/gateway-security-analyzer-bot.git
   cd gateway-security-analyzer-bot
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your credentials
   ```

4. **Create systemd service**
   ```bash
   sudo cp gateway-bot.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable gateway-bot
   sudo systemctl start gateway-bot
   ```

### Heroku Deployment

1. **Install Heroku CLI**

2. **Deploy to Heroku**
   ```bash
   heroku create your-bot-name
   heroku config:set BOT_TOKEN=your_bot_token
   heroku config:set ADMIN_IDS=your_admin_ids
   git push heroku main
   ```

### Railway Deployment

1. **Connect GitHub repository to Railway**
2. **Set environment variables in Railway dashboard**
3. **Deploy automatically from GitHub**

## 📖 Usage

### Bot Commands

- `/start` - Initialize the bot and see welcome message
- `/help` - Display help information and available commands
- `/url <website>` - Analyze a website for security and technology features

### Admin Commands

- `/approve <user_id>` - Approve a user to use the bot
- `/groupuse <enable|disable>` - Enable/disable bot usage in groups
- `/auth <on|off>` - Toggle user approval requirements
- `/stats` - View bot usage statistics

### Example Usage

```
/url https://example.com
```

The bot will analyze the website and return:
- Security features and headers
- Payment system detection
- Technology stack identification
- SSL certificate information
- Cloudflare and CDN detection

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `BOT_TOKEN` | Telegram Bot Token from BotFather | Yes | - |
| `ADMIN_IDS` | Comma-separated admin user IDs | Yes | - |
| `DATABASE_FILE` | Path to JSON database file | No | `bot_data.json` |

### Admin Configuration

1. **Get your Telegram User ID**
   - Message [@userinfobot](https://t.me/userinfobot) on Telegram
   - Add your ID to `ADMIN_IDS` environment variable

2. **Bot Setup**
   - Create a bot with [@BotFather](https://t.me/botfather)
   - Get the bot token
   - Add token to `BOT_TOKEN` environment variable

## 🏗️ Architecture

The bot follows a modular architecture:

- **Main Application** (`main.py`): Entry point and bot orchestration
- **Configuration** (`config.py`): Centralized settings and patterns
- **Database** (`database.py`): JSON-based user management
- **Handlers**: Command processors for different functionalities
- **Analyzers**: Specialized modules for website analysis
- **Utilities**: Common functions for validation and formatting

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

Test specific functionality:
```bash
# Test website analysis
python -c "from analyzers.website_analyzer import WebsiteAnalyzer; print('Tests passed')"
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and security research purposes only. Users are responsible for:

- Obtaining proper authorization before analyzing websites
- Complying with applicable laws and regulations
- Using the tool ethically and responsibly
- Respecting website terms of service and robots.txt

The authors are not responsible for any misuse of this tool or any damages that may result from its use.

## 🙏 Credits

- **Original Concept**: Inspired by security research and web analysis tools
- **Development**: Created with assistance from AI technology
- **Special Thanks**: Skittle and SigmaX for inspiration and guidance

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/gateway-security-analyzer-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/gateway-security-analyzer-bot/discussions)
- **Documentation**: This README and inline code comments

## 🔄 Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and updates.

---

**Note**: This project was developed with AI assistance to ensure comprehensive functionality and security best practices.