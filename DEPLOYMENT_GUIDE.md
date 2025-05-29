# 🚀 Server Deployment Guide - Indonesian Trading Bot

Complete guide to deploy your enhanced Indonesian trading bot on a server with ChatGPT Vision analysis.

## 📋 Table of Contents

1. [Server Requirements](#server-requirements)
2. [VPS Setup](#vps-setup)
3. [Quick Deployment](#quick-deployment)
4. [Manual Deployment](#manual-deployment)
5. [Configuration](#configuration)
6. [Testing](#testing)
7. [Production Management](#production-management)
8. [Monitoring & Maintenance](#monitoring--maintenance)
9. [Troubleshooting](#troubleshooting)
10. [Alternative Deployment Options](#alternative-deployment-options)

## 🖥️ Server Requirements

### Minimum Requirements

-   **OS**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
-   **RAM**: 1GB (2GB recommended)
-   **Storage**: 10GB (20GB recommended)
-   **CPU**: 1 vCPU (2 vCPU recommended)
-   **Network**: Stable internet connection

### Recommended VPS Providers

-   **DigitalOcean**: $5-10/month droplets
-   **Linode**: $5-10/month instances
-   **Vultr**: $5-10/month servers
-   **AWS EC2**: t3.micro (free tier eligible)
-   **Google Cloud**: e2-micro (free tier eligible)

## 🌐 VPS Setup

### 1. Create VPS Instance

**DigitalOcean Example:**

```bash
# Create droplet with Ubuntu 22.04
# Choose $5/month basic droplet
# Add SSH key for secure access
```

**AWS EC2 Example:**

```bash
# Launch t3.micro instance
# Choose Ubuntu 22.04 LTS AMI
# Configure security group (SSH, HTTP)
# Download key pair
```

### 2. Initial Server Setup

```bash
# Connect to your server
ssh root@your_server_ip

# Update system
apt update && apt upgrade -y

# Create non-root user (recommended)
adduser tradingbot
usermod -aG sudo tradingbot

# Switch to new user
su - tradingbot
```

## ⚡ Quick Deployment

### Option 1: Automated Script

```bash
# Download and run deployment script
wget https://raw.githubusercontent.com/yourusername/trading-bot/main/deploy_server.sh
chmod +x deploy_server.sh
./deploy_server.sh
```

### Option 2: One-Line Install

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/trading-bot/main/deploy_server.sh | bash
```

## 🔧 Manual Deployment

### Step 1: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv git curl wget
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y pkg-config libfreetype6-dev libpng-dev

# Install additional tools
sudo apt install -y htop nano screen tmux
```

### Step 2: Create Application Directory

```bash
# Create directory
sudo mkdir -p /opt/trading-bot
sudo chown $USER:$USER /opt/trading-bot
cd /opt/trading-bot

# Create subdirectories
mkdir -p logs backups
```

### Step 3: Upload Bot Files

**Option A: Git Clone (Recommended)**

```bash
# Clone your repository
git clone https://github.com/yourusername/indonesian-trading-bot.git .
```

**Option B: Manual Upload**

```bash
# Upload files using SCP
scp -r /local/path/to/trading-bot/* user@server:/opt/trading-bot/
```

**Option C: Direct File Transfer**

```bash
# Create files directly on server
nano trading_bot.py
# Copy and paste your code
```

### Step 4: Setup Python Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Configure Environment

```bash
# Create environment file
cp .env.example .env
nano .env

# Add your credentials:
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 6: Create System Service

```bash
# Create systemd service file
sudo nano /etc/systemd/system/trading-bot.service
```

Add this content:

```ini
[Unit]
Description=Indonesian Trading Bot
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=tradingbot
WorkingDirectory=/opt/trading-bot
Environment=PATH=/opt/trading-bot/venv/bin
ExecStart=/opt/trading-bot/venv/bin/python /opt/trading-bot/run_production.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Step 7: Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable trading-bot

# Start the service
sudo systemctl start trading-bot

# Check status
sudo systemctl status trading-bot
```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Required - Telegram Configuration
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# Required - OpenAI Configuration
OPENAI_API_KEY=sk-proj-abcdefghijklmnopqrstuvwxyz

# Optional - Advanced Settings
ENABLE_CHATGPT_CONFIRMATION=True
ENABLE_CHATGPT_VISION=True
CHATGPT_CONFIDENCE_THRESHOLD=0.7
ENABLE_WATCHLIST=True
```

### Bot Configuration (config.py)

```python
# Customize these settings as needed
INDONESIAN_STOCKS = [
    'BBCA.JK', 'BBRI.JK', 'BMRI.JK', 'TLKM.JK',
    'ASII.JK', 'UNVR.JK', 'ICBP.JK', 'GGRM.JK'
]

WATCHLIST_STOCKS = [
    'BBCA.JK', 'BBRI.JK', 'BMRI.JK', 'TLKM.JK'
]

# ChatGPT Vision Settings
ENABLE_CHATGPT_VISION = True
CHATGPT_VISION_MODEL = "gpt-4o"
CHART_IMAGE_QUALITY = "high"
```

## 🧪 Testing

### Test Bot Deployment

```bash
# Test the bot
cd /opt/trading-bot
source venv/bin/activate
python run_production.py test

# Expected output:
# ✅ Test successful: BBCA.JK analysis completed
# 🚀 Bot is ready for production!
```

### Test Individual Components

```bash
# Test single stock analysis
python test_enhanced_chatgpt.py BBCA.JK

# Test watchlist functionality
python watchlist_manager.py info

# Test Telegram connectivity
python -c "
import asyncio
from trading_bot import IndonesianStockBot
async def test():
    bot = IndonesianStockBot()
    await bot.send_telegram_message('🧪 Test message from server!')
asyncio.run(test())
"
```

## 🏭 Production Management

### Service Management Commands

```bash
# Start the bot
sudo systemctl start trading-bot

# Stop the bot
sudo systemctl stop trading-bot

# Restart the bot
sudo systemctl restart trading-bot

# Check status
sudo systemctl status trading-bot

# Enable auto-start on boot
sudo systemctl enable trading-bot

# Disable auto-start
sudo systemctl disable trading-bot
```

### View Logs

```bash
# View live logs
sudo journalctl -u trading-bot -f

# View recent logs
sudo journalctl -u trading-bot -n 50

# View logs from specific time
sudo journalctl -u trading-bot --since "2024-01-01 00:00:00"

# View error logs only
sudo journalctl -u trading-bot -p err

# View bot's own log files
tail -f /opt/trading-bot/logs/trading_bot.log
tail -f /opt/trading-bot/logs/trading_bot_errors.log
```

### Management Scripts

```bash
# Monitor bot status and resources
cd /opt/trading-bot
./monitor.sh

# Create backup
./backup.sh

# Update bot
./update.sh
```

## 📊 Monitoring & Maintenance

### Daily Monitoring

```bash
# Check bot status
./monitor.sh

# Expected output:
# ✅ Trading Bot is running
# 📝 Recent logs (last 10 lines):
# 💻 System resources:
# Memory usage: 245M/1.0G
# Disk usage: 2.1G/25G (9%)
# CPU load: 0.15, 0.12, 0.08
```

### Weekly Maintenance

```bash
# Create backup
./backup.sh

# Update system packages
sudo apt update && sudo apt upgrade -y

# Clean up old logs
sudo journalctl --vacuum-time=30d

# Check disk space
df -h
```

### Monthly Tasks

```bash
# Update Python packages
source venv/bin/activate
pip list --outdated
pip install --upgrade package_name

# Review and clean old backups
ls -la backups/
# Keep only recent backups

# Review bot performance logs
grep "analysis completed" logs/trading_bot.log | tail -30
```

## 🔍 Monitoring Setup

### Setup Log Rotation

```bash
# Create logrotate configuration
sudo nano /etc/logrotate.d/trading-bot
```

Add:

```
/opt/trading-bot/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 tradingbot tradingbot
}
```

### Setup Monitoring Alerts

```bash
# Create monitoring script
nano /opt/trading-bot/health_check.sh
```

Add:

```bash
#!/bin/bash
# Health check script

if ! systemctl is-active --quiet trading-bot; then
    echo "Trading bot is down!" | mail -s "Trading Bot Alert" your@email.com
    # Or send to Telegram
    curl -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
         -d chat_id="$CHAT_ID" \
         -d text="🚨 Trading Bot is down on server!"
fi
```

### Setup Cron Jobs

```bash
# Edit crontab
crontab -e

# Add monitoring jobs
# Check every 5 minutes
*/5 * * * * /opt/trading-bot/health_check.sh

# Daily backup at 2 AM
0 2 * * * /opt/trading-bot/backup.sh

# Weekly system update (Sunday 3 AM)
0 3 * * 0 sudo apt update && sudo apt upgrade -y
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Bot Not Starting

```bash
# Check service status
sudo systemctl status trading-bot

# Check logs for errors
sudo journalctl -u trading-bot -n 50

# Common fixes:
# - Check .env file exists and has correct values
# - Verify Python virtual environment
# - Check file permissions
```

#### 2. Telegram Messages Not Sending

```bash
# Test Telegram connectivity
curl -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
     -d chat_id="$CHAT_ID" \
     -d text="Test message"

# Common fixes:
# - Verify bot token and chat ID
# - Check internet connectivity
# - Ensure bot is added to chat
```

#### 3. OpenAI API Errors

```bash
# Test OpenAI API
curl -X POST "https://api.openai.com/v1/chat/completions" \
     -H "Authorization: Bearer $OPENAI_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"test"}]}'

# Common fixes:
# - Verify API key is correct
# - Check OpenAI account has credits
# - Verify API key permissions
```

#### 4. Memory Issues

```bash
# Check memory usage
free -h
top -p $(pgrep -f trading-bot)

# Solutions:
# - Upgrade server RAM
# - Optimize Python memory usage
# - Restart bot daily via cron
```

#### 5. Disk Space Issues

```bash
# Check disk usage
df -h
du -sh /opt/trading-bot/*

# Clean up:
# - Remove old log files
# - Clean old backups
# - Clear Python cache: find . -name "__pycache__" -exec rm -rf {} +
```

### Debug Mode

```bash
# Enable debug logging
nano /opt/trading-bot/config.py

# Change logging level
import logging
logging.basicConfig(level=logging.DEBUG)

# Restart service
sudo systemctl restart trading-bot
```

### Recovery Procedures

#### Service Recovery

```bash
# If service fails to start
sudo systemctl reset-failed trading-bot
sudo systemctl start trading-bot

# If persistent issues
sudo systemctl stop trading-bot
cd /opt/trading-bot
source venv/bin/activate
python run_production.py test
```

#### Data Recovery

```bash
# Restore from backup
cd /opt/trading-bot/backups
tar -xzf trading_bot_backup_YYYYMMDD_HHMMSS.tar.gz
# Copy files as needed
```

## 🔄 Alternative Deployment Options

### 1. Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "run_production.py"]
```

```bash
# Build and run
docker build -t trading-bot .
docker run -d --name trading-bot --env-file .env trading-bot
```

### 2. Cloud Platform Deployment

#### Heroku

```bash
# Install Heroku CLI
# Create Procfile: worker: python run_production.py
heroku create your-trading-bot
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

#### Railway

```bash
# Connect GitHub repository
# Set environment variables in dashboard
# Deploy automatically on push
```

#### Google Cloud Run

```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT_ID/trading-bot

# Deploy
gcloud run deploy --image gcr.io/PROJECT_ID/trading-bot --platform managed
```

### 3. Raspberry Pi Deployment

```bash
# Install on Raspberry Pi OS
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git

# Follow manual deployment steps
# Consider using screen or tmux for persistence
screen -S trading-bot
python run_production.py
# Ctrl+A, D to detach
```

## 📈 Performance Optimization

### Server Optimization

```bash
# Optimize Python performance
export PYTHONOPTIMIZE=1

# Use faster JSON library
pip install ujson

# Enable swap if needed
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Bot Optimization

```python
# In config.py - reduce analysis frequency for testing
# Increase delays between API calls
# Use lighter ChatGPT models for cost optimization
CHATGPT_MODEL = "gpt-4o-mini"  # More cost-effective
```

## 🔐 Security Best Practices

### Server Security

```bash
# Update system regularly
sudo apt update && sudo apt upgrade -y

# Configure firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443

# Disable root login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
sudo systemctl restart ssh

# Use SSH keys instead of passwords
ssh-copy-id user@server
```

### Application Security

```bash
# Secure environment file
chmod 600 .env

# Use non-root user for service
# Regularly rotate API keys
# Monitor logs for suspicious activity
```

## 📞 Support & Maintenance

### Getting Help

1. **Check logs first**: `sudo journalctl -u trading-bot -n 50`
2. **Test components individually**: Use test scripts
3. **Check server resources**: `./monitor.sh`
4. **Review configuration**: Verify .env and config.py
5. **Restart service**: `sudo systemctl restart trading-bot`

### Maintenance Schedule

-   **Daily**: Check bot status and logs
-   **Weekly**: Create backup, review performance
-   **Monthly**: Update packages, clean logs
-   **Quarterly**: Review and optimize configuration

---

## 🎉 Congratulations!

Your Indonesian Trading Bot with ChatGPT Vision analysis is now running on a server!

### Next Steps:

1. Monitor the first few days of operation
2. Adjust configuration based on performance
3. Set up additional monitoring and alerts
4. Consider scaling if needed

### Remember:

-   Always test changes in a development environment first
-   Keep backups of your configuration and data
-   Monitor API usage and costs
-   This is for educational purposes - always DYOR!

**Happy Trading! 📈🇮🇩**
