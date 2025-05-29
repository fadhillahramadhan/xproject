#!/bin/bash

# Murphy's Crypto Trading Bot - Server Setup Script
# Run this script on a fresh Ubuntu 20.04/22.04 server

set -e  # Exit on any error

echo "🚀 Setting up Murphy's Crypto Trading Bot Server..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}Please run this script as a non-root user with sudo privileges${NC}"
    exit 1
fi

# Update system
echo -e "${YELLOW}Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y

# Install essential packages
echo -e "${YELLOW}Installing essential packages...${NC}"
sudo apt install -y python3 python3-pip python3-venv git nginx certbot python3-certbot-nginx ufw htop nano curl wget

# Setup firewall
echo -e "${YELLOW}Configuring firewall...${NC}"
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# Create virtual environment
echo -e "${YELLOW}Setting up Python virtual environment...${NC}"
python3 -m venv crypto_bot_env
source crypto_bot_env/bin/activate

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Create production config
echo -e "${YELLOW}Setting up configuration...${NC}"
if [ ! -f config_production.env ]; then
    cp config.env config_production.env
    echo -e "${GREEN}Created config_production.env - Please edit this file with your actual tokens${NC}"
fi

# Create systemd service
echo -e "${YELLOW}Creating systemd service...${NC}"
sudo tee /etc/systemd/system/crypto-bot.service > /dev/null <<EOF
[Unit]
Description=Murphy's Crypto Trading Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PWD
Environment=PATH=$PWD/crypto_bot_env/bin
ExecStart=$PWD/crypto_bot_env/bin/python telegram_bot.py
EnvironmentFile=$PWD/config_production.env
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create logs directory
mkdir -p logs

# Set proper permissions
chmod 600 config_production.env
chmod +x telegram_bot.py

# Reload systemd and enable service
echo -e "${YELLOW}Enabling service...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable crypto-bot

# Create update script
echo -e "${YELLOW}Creating update script...${NC}"
tee update_bot.sh > /dev/null <<EOF
#!/bin/bash
cd $PWD

echo "Stopping bot..."
sudo systemctl stop crypto-bot

echo "Pulling latest changes..."
git pull origin main

echo "Activating virtual environment..."
source crypto_bot_env/bin/activate

echo "Updating dependencies..."
pip install -r requirements.txt

echo "Starting bot..."
sudo systemctl start crypto-bot

echo "Bot updated and restarted successfully!"
sudo systemctl status crypto-bot
EOF

chmod +x update_bot.sh

# Setup log rotation
echo -e "${YELLOW}Setting up log rotation...${NC}"
sudo tee /etc/logrotate.d/crypto-bot > /dev/null <<EOF
$PWD/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 644 $USER $USER
    postrotate
        sudo systemctl reload crypto-bot
    endscript
}
EOF

echo -e "${GREEN}✅ Server setup completed!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Edit config_production.env with your Telegram bot token:"
echo "   nano config_production.env"
echo ""
echo "2. Start the bot:"
echo "   sudo systemctl start crypto-bot"
echo ""
echo "3. Check bot status:"
echo "   sudo systemctl status crypto-bot"
echo ""
echo "4. View logs:"
echo "   sudo journalctl -u crypto-bot -f"
echo ""
echo "5. Update bot (when needed):"
echo "   ./update_bot.sh"
echo ""
echo -e "${GREEN}🎉 Your Murphy's Crypto Trading Bot is ready!${NC}" 