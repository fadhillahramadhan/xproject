# 🚀 Server Deployment Guide

Complete guide to deploy Murphy's Crypto Trading Bot on various server platforms.

## 🌐 Server Options

### 1. **VPS (Virtual Private Server)** - Recommended

-   **DigitalOcean** - $5-10/month
-   **Linode** - $5-10/month
-   **Vultr** - $2.50-6/month
-   **AWS EC2** - $3-10/month
-   **Google Cloud Compute** - $5-10/month

### 2. **Free Options** (Limited)

-   **Heroku** - Free tier (sleeps after 30min)
-   **Railway** - $5/month
-   **Render** - Free tier available
-   **PythonAnywhere** - Free tier (limited)

### 3. **Dedicated Servers**

-   **Hetzner** - €3-20/month
-   **OVH** - €3-15/month

## 🐧 Ubuntu Server Setup (Recommended)

### Step 1: Create Server

1. **Choose Ubuntu 20.04 or 22.04 LTS**
2. **Minimum specs:** 1GB RAM, 1 CPU, 25GB storage
3. **Recommended:** 2GB RAM, 2 CPU, 50GB storage

### Step 2: Initial Server Setup

```bash
# Connect to your server
ssh root@your_server_ip

# Update system
apt update && apt upgrade -y

# Install essential packages
apt install -y python3 python3-pip python3-venv git nginx certbot python3-certbot-nginx ufw htop nano

# Create a new user (replace 'botuser' with your preferred username)
adduser botuser
usermod -aG sudo botuser

# Setup firewall
ufw allow ssh
ufw allow 80
ufw allow 443
ufw enable

# Switch to new user
su - botuser
```

### Step 3: Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv crypto_bot_env
source crypto_bot_env/bin/activate

# Clone your repository
git clone https://github.com/yourusername/TradingCryptoBot.git
cd TradingCryptoBot

# Install requirements
pip install -r requirements.txt
```

### Step 4: Configuration

```bash
# Copy and edit configuration
cp config.env config_production.env
nano config_production.env
```

**Edit config_production.env:**

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=YOUR_ACTUAL_BOT_TOKEN

# Exchange API Keys (Optional)
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key

# Bot Settings
DEFAULT_TIMEFRAME=4h
DEFAULT_SYMBOLS=BTC/USDT,ETH/USDT,BNB/USDT,ADA/USDT,SOL/USDT
ANALYSIS_INTERVAL=3600
RISK_THRESHOLD=75

# Production settings
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Step 5: Create Systemd Service

```bash
sudo nano /etc/systemd/system/crypto-bot.service
```

**Add this content:**

```ini
[Unit]
Description=Murphy's Crypto Trading Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/TradingCryptoBot
Environment=PATH=/home/botuser/crypto_bot_env/bin
ExecStart=/home/botuser/crypto_bot_env/bin/python telegram_bot.py
EnvironmentFile=/home/botuser/TradingCryptoBot/config_production.env
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Step 6: Start and Enable Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable crypto-bot

# Start the service
sudo systemctl start crypto-bot

# Check status
sudo systemctl status crypto-bot

# View logs
sudo journalctl -u crypto-bot -f
```

## 🐳 Docker Deployment

### Create Dockerfile

```bash
nano Dockerfile
```

**Dockerfile content:**

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Command to run the application
CMD ["python", "telegram_bot.py"]
```

### Create docker-compose.yml

```bash
nano docker-compose.yml
```

**docker-compose.yml content:**

```yaml
version: '3.8'

services:
    crypto-bot:
        build: .
        restart: unless-stopped
        env_file:
            - config_production.env
        volumes:
            - ./logs:/app/logs
        environment:
            - ENVIRONMENT=production
        healthcheck:
            test:
                [
                    'CMD',
                    'python',
                    '-c',
                    "import requests; requests.get('https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe')",
                ]
            interval: 30s
            timeout: 10s
            retries: 3
```

### Deploy with Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Update
git pull
docker-compose build
docker-compose up -d
```

## ☁️ Cloud Platform Deployments

### Heroku Deployment

1. **Create Procfile:**

```bash
echo "worker: python telegram_bot.py" > Procfile
```

2. **Create runtime.txt:**

```bash
echo "python-3.11.6" > runtime.txt
```

3. **Deploy to Heroku:**

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login and create app
heroku login
heroku create your-crypto-bot-name

# Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set BINANCE_API_KEY=your_key
heroku config:set BINANCE_SECRET_KEY=your_secret

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Scale worker
heroku ps:scale worker=1
```

### Railway Deployment

1. **Connect GitHub repository**
2. **Add environment variables**
3. **Deploy automatically**

### AWS EC2 Deployment

```bash
# Connect to EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Follow Ubuntu setup steps above
# Configure security groups for ports 80, 443, 22
```

## 🔒 Security Best Practices

### 1. SSH Security

```bash
# Generate SSH key pair on your local machine
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Copy public key to server
ssh-copy-id botuser@your_server_ip

# Disable password authentication
sudo nano /etc/ssh/sshd_config
```

**Edit SSH config:**

```
PasswordAuthentication no
PermitRootLogin no
Port 2222  # Change default port
```

```bash
# Restart SSH
sudo systemctl restart ssh
```

### 2. Environment Variables Security

```bash
# Secure config file
chmod 600 config_production.env
```

### 3. Firewall Configuration

```bash
# Allow only necessary ports
sudo ufw deny incoming
sudo ufw allow outgoing
sudo ufw allow 2222  # SSH (if you changed port)
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
```

## 📊 Monitoring and Logs

### 1. Log Management

```bash
# Create logging configuration
nano logging_config.py
```

**logging_config.py:**

```python
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    # Create logs directory
    os.makedirs('logs', exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler('logs/bot.log', maxBytes=10*1024*1024, backupCount=5),
            logging.StreamHandler()
        ]
    )
```

### 2. System Monitoring

```bash
# Install monitoring tools
sudo apt install -y htop iotop nethogs

# Check system resources
htop

# Monitor bot logs
tail -f logs/bot.log

# Check service status
systemctl status crypto-bot
```

### 3. Setup Alerts (Optional)

```bash
# Install fail2ban for security
sudo apt install fail2ban

# Configure logwatch for log monitoring
sudo apt install logwatch
```

## 🔄 Auto Updates and Maintenance

### Create Update Script

```bash
nano update_bot.sh
```

**update_bot.sh:**

```bash
#!/bin/bash
cd /home/botuser/TradingCryptoBot

# Pull latest changes
git pull origin main

# Activate virtual environment
source /home/botuser/crypto_bot_env/bin/activate

# Update dependencies
pip install -r requirements.txt

# Restart service
sudo systemctl restart crypto-bot

echo "Bot updated and restarted successfully!"
```

```bash
# Make executable
chmod +x update_bot.sh

# Create cron job for automatic updates (optional)
crontab -e
```

**Add to crontab (updates daily at 3 AM):**

```
0 3 * * * /home/botuser/TradingCryptoBot/update_bot.sh
```

## 🚨 Troubleshooting

### Common Issues

1. **Bot not starting:**

```bash
# Check service status
sudo systemctl status crypto-bot

# View detailed logs
sudo journalctl -u crypto-bot -f

# Check Python errors
python telegram_bot.py
```

2. **Permission errors:**

```bash
# Fix ownership
sudo chown -R botuser:botuser /home/botuser/TradingCryptoBot

# Fix permissions
chmod +x telegram_bot.py
```

3. **Memory issues:**

```bash
# Check memory usage
free -h

# Monitor processes
htop

# Restart service
sudo systemctl restart crypto-bot
```

4. **API connectivity issues:**

```bash
# Test internet connectivity
ping google.com

# Test API endpoints
curl -X GET "https://api.binance.com/api/v3/ping"
```

## 📱 Domain and SSL (Optional)

### 1. Point Domain to Server

-   Update DNS A record to point to your server IP

### 2. Setup SSL Certificate

```bash
# Install SSL certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

## 💰 Cost Optimization

### Free/Cheap Options:

1. **Oracle Cloud** - Always Free tier (1-4 ARM cores, 6-24GB RAM)
2. **Google Cloud** - $300 credit for new users
3. **AWS Free Tier** - 12 months free
4. **Azure** - $200 credit for new users

### Resource Usage:

-   **CPU**: 10-20% average
-   **RAM**: 200-500MB
-   **Storage**: 1-5GB
-   **Bandwidth**: 1-10GB/month

## 🎯 Production Checklist

-   [ ] Server secured (SSH keys, firewall, non-root user)
-   [ ] Bot token configured
-   [ ] Service running and enabled
-   [ ] Logs properly configured
-   [ ] Monitoring setup
-   [ ] Backup strategy in place
-   [ ] Update mechanism configured
-   [ ] Domain and SSL (if needed)
-   [ ] Performance monitoring active

---

**Your Murphy's Crypto Trading Bot is now running 24/7 on your server!** 🚀

For support, check the logs first, then create an issue with error details.
