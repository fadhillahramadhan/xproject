# 🚀 Interactive Telegram Bot Deployment Guide

Complete guide to deploy your Interactive Telegram Trading Bot with real-time command support.

## 📋 Quick Start Options

### 🖥️ Option 1: Local Development (Testing)

### ☁️ Option 2: VPS Deployment (Recommended)

### 🚀 Option 3: Cloud Deployment (Scalable)

### 🐳 Option 4: Docker Deployment (Portable)

---

## 🖥️ Option 1: Local Development (Testing)

Perfect for testing before deploying to production.

### Prerequisites

-   Python 3.8+
-   Git
-   Telegram Bot Token
-   OpenAI API Key

### Steps

1. **Install Dependencies**

```bash
# Install Python packages
pip install -r requirements.txt

# Additional packages for interactive bot
pip install python-telegram-bot==20.7
```

2. **Setup Environment**

```bash
# Create .env file
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
OPENAI_API_KEY=your_openai_api_key_here
```

3. **Run Interactive Bot**

```bash
# Method 1: Direct run
python interactive_telegram_bot.py

# Method 2: Using startup script
python start_interactive_bot.py
```

4. **Test Commands**

-   Send `/start` to your bot
-   Try `/analyze BTC`
-   Test `/help` command

---

## ☁️ Option 2: VPS Deployment (Recommended)

Best for 24/7 operation with reliable uptime.

### Recommended VPS Providers

-   **DigitalOcean**: $5-10/month droplets
-   **Linode**: $5-10/month instances
-   **Vultr**: $5-10/month servers
-   **AWS EC2**: t3.micro (free tier)

### Server Requirements

-   **OS**: Ubuntu 20.04+ / Debian 11+
-   **RAM**: 2GB minimum (4GB recommended)
-   **Storage**: 20GB SSD
-   **CPU**: 2 vCPU recommended
-   **Network**: Stable internet (100 Mbps+)

### Deployment Steps

1. **Create Server & Connect**

```bash
# Connect to your VPS
ssh root@your_server_ip

# Update system
apt update && apt upgrade -y

# Create user for bot
adduser tradingbot
usermod -aG sudo tradingbot
su - tradingbot
```

2. **Install Dependencies**

```bash
# Install Python and tools
sudo apt install -y python3 python3-pip python3-venv git curl wget
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y pkg-config libfreetype6-dev libpng-dev
sudo apt install -y htop nano screen tmux

# Install Node.js (for some dependencies)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

3. **Setup Application**

```bash
# Create directory
sudo mkdir -p /opt/trading-bot
sudo chown tradingbot:tradingbot /opt/trading-bot
cd /opt/trading-bot

# Clone or upload your bot files
git clone https://github.com/yourusername/TradingBot.git .
# OR upload files manually
```

4. **Setup Python Environment**

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Install interactive bot specific packages
pip install python-telegram-bot==20.7
```

5. **Configure Environment**

```bash
# Create environment file
nano .env

# Add your credentials:
TELEGRAM_BOT_TOKEN=7722311907:AAEpV1FPB9qr2jAXehLN33cVNaOLRtqkKwI
TELEGRAM_CHAT_ID=your_chat_id_here
OPENAI_API_KEY=your_openai_api_key_here
```

6. **Create Systemd Service**

```bash
sudo nano /etc/systemd/system/trading-bot-interactive.service
```

Add this content:

```ini
[Unit]
Description=Interactive Telegram Trading Bot
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=tradingbot
Group=tradingbot
WorkingDirectory=/opt/trading-bot
Environment=PATH=/opt/trading-bot/venv/bin
ExecStart=/opt/trading-bot/venv/bin/python /opt/trading-bot/interactive_telegram_bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
```

7. **Enable and Start Service**

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable trading-bot-interactive

# Start service
sudo systemctl start trading-bot-interactive

# Check status
sudo systemctl status trading-bot-interactive

# View logs
sudo journalctl -u trading-bot-interactive -f
```

---

## 🚀 Option 3: Cloud Deployment

### AWS EC2 Deployment

1. **Launch EC2 Instance**

```bash
# Use t3.micro (free tier) or t3.small
# Ubuntu 22.04 LTS AMI
# Configure security group (SSH: 22, HTTPS: 443)
```

2. **Deploy with User Data Script**

```bash
#!/bin/bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv git

# Create trading bot user
adduser --disabled-password --gecos "" tradingbot
mkdir -p /opt/trading-bot
chown tradingbot:tradingbot /opt/trading-bot

# Clone repository (replace with your repo)
cd /opt/trading-bot
git clone https://github.com/yourusername/TradingBot.git .

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install python-telegram-bot==20.7

# Create systemd service
cat > /etc/systemd/system/trading-bot.service << EOF
[Unit]
Description=Interactive Trading Bot
After=network.target

[Service]
Type=simple
User=tradingbot
WorkingDirectory=/opt/trading-bot
Environment=PATH=/opt/trading-bot/venv/bin
ExecStart=/opt/trading-bot/venv/bin/python interactive_telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable trading-bot
```

### Google Cloud Platform

1. **Create Compute Engine Instance**

```bash
# Use e2-micro (free tier)
# Ubuntu 22.04 LTS
# Allow HTTP/HTTPS traffic
```

2. **Use Startup Script**

```bash
# Add startup script in metadata
# Same as AWS user data script above
```

---

## 🐳 Option 4: Docker Deployment

Perfect for containerized deployment and easy scaling.

1. **Create Dockerfile**

```dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    pkg-config \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-telegram-bot==20.7

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Expose port (if needed)
EXPOSE 8000

# Run the interactive bot
CMD ["python", "interactive_telegram_bot.py"]
```

2. **Create Docker Compose**

```yaml
version: '3.8'

services:
    trading-bot:
        build: .
        restart: unless-stopped
        environment:
            - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
            - TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
            - OPENAI_API_KEY=${OPENAI_API_KEY}
        env_file:
            - .env
        volumes:
            - ./logs:/app/logs
        logging:
            driver: 'json-file'
            options:
                max-size: '10m'
                max-file: '3'
```

3. **Deploy with Docker**

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🔧 Configuration & Testing

### Environment Variables

```bash
# Required
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
OPENAI_API_KEY=your_openai_key

# Optional
ENABLE_CHATGPT_CONFIRMATION=True
ENABLE_CHATGPT_VISION=True
CHATGPT_MODEL=gpt-4o-mini
RSI_OVERBOUGHT_THRESHOLD=80
STOP_LOSS_PERCENTAGE=0.15
TAKE_PROFIT_PERCENTAGE=0.25
```

### Testing Commands

```bash
# Basic functionality
/start
/help
/analyze BTC
/analyze ANTM.JK

# Watchlist management
/watchlist
/watchlist add ETH
/watchlist add BBCA.JK

# Quick analysis (no command)
BTC
ETH
SUNI.JK

# Signals
/signals
```

---

## 📊 Monitoring & Maintenance

### Log Management

```bash
# View real-time logs
sudo journalctl -u trading-bot-interactive -f

# View recent logs
sudo journalctl -u trading-bot-interactive -n 50

# Log rotation
sudo nano /etc/logrotate.d/trading-bot
```

### Service Management

```bash
# Restart bot
sudo systemctl restart trading-bot-interactive

# Stop bot
sudo systemctl stop trading-bot-interactive

# Start bot
sudo systemctl start trading-bot-interactive

# Check status
sudo systemctl status trading-bot-interactive
```

### Automatic Updates

```bash
# Create update script
nano /opt/trading-bot/update.sh
```

```bash
#!/bin/bash
cd /opt/trading-bot
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart trading-bot-interactive
echo "Bot updated and restarted"
```

### Health Monitoring

```bash
# Create health check script
nano /opt/trading-bot/health_check.sh
```

```bash
#!/bin/bash
if ! systemctl is-active --quiet trading-bot-interactive; then
    echo "Bot is down, restarting..."
    sudo systemctl start trading-bot-interactive
    # Send alert to telegram or email
fi
```

---

## 🛠️ Troubleshooting

### Common Issues

1. **Bot Not Responding**

```bash
# Check service status
sudo systemctl status trading-bot-interactive

# Check logs for errors
sudo journalctl -u trading-bot-interactive -n 50

# Restart service
sudo systemctl restart trading-bot-interactive
```

2. **Memory Issues**

```bash
# Check memory usage
free -h
htop

# Add swap space if needed
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

3. **Network Issues**

```bash
# Test internet connectivity
ping google.com

# Test Telegram API
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe"

# Test OpenAI API
curl -H "Authorization: Bearer ${OPENAI_API_KEY}" https://api.openai.com/v1/models
```

4. **Permission Issues**

```bash
# Fix file permissions
sudo chown -R tradingbot:tradingbot /opt/trading-bot
chmod +x /opt/trading-bot/*.py
```

---

## 🚀 Quick Deploy Script

Create an automated deployment script:

```bash
nano deploy_interactive_bot.sh
```

```bash
#!/bin/bash
set -e

echo "🚀 Interactive Trading Bot Deployment Script"
echo "============================================"

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv git curl

# Create application directory
sudo mkdir -p /opt/trading-bot
sudo chown $USER:$USER /opt/trading-bot
cd /opt/trading-bot

# Setup Python environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install --upgrade pip
pip install yfinance pandas numpy matplotlib python-telegram-bot==20.7 python-dotenv openai asyncio

# Create environment file
cat > .env << EOF
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
OPENAI_API_KEY=your_openai_key_here
EOF

echo "✅ Deployment complete!"
echo "📝 Edit .env file with your credentials"
echo "🚀 Run: python interactive_telegram_bot.py"
```

Make it executable and run:

```bash
chmod +x deploy_interactive_bot.sh
./deploy_interactive_bot.sh
```

---

## 🎯 Production Checklist

-   [ ] VPS/Server provisioned
-   [ ] Dependencies installed
-   [ ] Bot files uploaded
-   [ ] Environment configured
-   [ ] Systemd service created
-   [ ] Service started and enabled
-   [ ] Bot responds to `/start`
-   [ ] Analyze commands work
-   [ ] Watchlist functions work
-   [ ] Logs are accessible
-   [ ] Auto-restart configured
-   [ ] Health monitoring setup
-   [ ] Backup strategy in place

**Ready to deploy? Choose your preferred option and follow the guide!** 🚀
