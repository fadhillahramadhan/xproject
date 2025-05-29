#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Interactive Trading Bot Deployment Script${NC}"
echo "============================================"
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}❌ This script should not be run as root${NC}"
   echo "Please run as a regular user with sudo privileges"
   exit 1
fi

# Update system
echo -e "${YELLOW}📦 Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo -e "${YELLOW}🔧 Installing dependencies...${NC}"
sudo apt install -y python3 python3-pip python3-venv git curl wget
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y pkg-config libfreetype6-dev libpng-dev
sudo apt install -y htop nano screen tmux

# Check if user wants to create service user
read -p "Create dedicated 'tradingbot' user? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo adduser --disabled-password --gecos "" tradingbot || true
    sudo usermod -aG sudo tradingbot
    echo -e "${GREEN}✅ Created tradingbot user${NC}"
    BOT_USER="tradingbot"
    BOT_HOME="/home/tradingbot"
else
    BOT_USER=$(whoami)
    BOT_HOME=$HOME
fi

# Create application directory
APP_DIR="/opt/trading-bot"
echo -e "${YELLOW}📁 Creating application directory...${NC}"
sudo mkdir -p $APP_DIR
sudo chown $BOT_USER:$BOT_USER $APP_DIR

# Copy current directory files to app directory
echo -e "${YELLOW}📋 Copying application files...${NC}"
if [ "$PWD" != "$APP_DIR" ]; then
    sudo cp -r * $APP_DIR/ 2>/dev/null || true
    sudo chown -R $BOT_USER:$BOT_USER $APP_DIR
fi

cd $APP_DIR

# Setup Python environment
echo -e "${YELLOW}🐍 Setting up Python virtual environment...${NC}"
sudo -u $BOT_USER python3 -m venv venv
sudo -u $BOT_USER bash -c "source venv/bin/activate && pip install --upgrade pip"

# Install Python packages
echo -e "${YELLOW}📦 Installing Python packages...${NC}"
sudo -u $BOT_USER bash -c "source venv/bin/activate && pip install yfinance pandas numpy matplotlib python-dotenv openai asyncio telegram python-telegram-bot==20.7"

# Create requirements.txt if it doesn't exist
if [ ! -f requirements.txt ]; then
    echo -e "${YELLOW}📝 Creating requirements.txt...${NC}"
    cat > requirements.txt << EOF
yfinance==0.2.28
pandas==2.1.4
numpy==1.24.3
matplotlib==3.7.2
python-dotenv==1.0.0
openai==1.3.7
python-telegram-bot==20.7
asyncio-mqtt==0.16.1
EOF
    sudo chown $BOT_USER:$BOT_USER requirements.txt
fi

# Install from requirements.txt
sudo -u $BOT_USER bash -c "source venv/bin/activate && pip install -r requirements.txt"

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}🔐 Creating environment file...${NC}"
    cat > .env << EOF
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Trading Configuration
ENABLE_CHATGPT_CONFIRMATION=True
ENABLE_CHATGPT_VISION=True
CHATGPT_MODEL=gpt-4o-mini
RSI_OVERBOUGHT_THRESHOLD=80
STOP_LOSS_PERCENTAGE=0.15
TAKE_PROFIT_PERCENTAGE=0.25
EOF
    sudo chown $BOT_USER:$BOT_USER .env
    echo -e "${RED}⚠️  Please edit .env file with your actual credentials!${NC}"
fi

# Create systemd service
echo -e "${YELLOW}⚙️  Creating systemd service...${NC}"
sudo tee /etc/systemd/system/trading-bot-interactive.service > /dev/null << EOF
[Unit]
Description=Interactive Telegram Trading Bot
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$BOT_USER
Group=$BOT_USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/interactive_telegram_bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
TimeoutStopSec=30
KillMode=process

[Install]
WantedBy=multi-user.target
EOF

# Create log directory
sudo mkdir -p /var/log/trading-bot
sudo chown $BOT_USER:$BOT_USER /var/log/trading-bot

# Create update script
echo -e "${YELLOW}🔄 Creating update script...${NC}"
cat > update.sh << 'EOF'
#!/bin/bash
echo "🔄 Updating Trading Bot..."
cd /opt/trading-bot
git pull origin main 2>/dev/null || echo "Not a git repository, skipping git pull"
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart trading-bot-interactive
echo "✅ Bot updated and restarted"
EOF
chmod +x update.sh
sudo chown $BOT_USER:$BOT_USER update.sh

# Create health check script
echo -e "${YELLOW}🏥 Creating health check script...${NC}"
cat > health_check.sh << 'EOF'
#!/bin/bash
SERVICE_NAME="trading-bot-interactive"

if ! systemctl is-active --quiet $SERVICE_NAME; then
    echo "$(date): Bot is down, restarting..."
    sudo systemctl start $SERVICE_NAME
    
    # Optional: Send alert to Telegram
    # curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
    #     -d chat_id="$TELEGRAM_CHAT_ID" \
    #     -d text="🚨 Trading Bot was down and has been restarted at $(date)"
else
    echo "$(date): Bot is running normally"
fi
EOF
chmod +x health_check.sh
sudo chown $BOT_USER:$BOT_USER health_check.sh

# Setup log rotation
echo -e "${YELLOW}📜 Setting up log rotation...${NC}"
sudo tee /etc/logrotate.d/trading-bot > /dev/null << EOF
/var/log/trading-bot/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 $BOT_USER $BOT_USER
}
EOF

# Reload systemd and enable service
echo -e "${YELLOW}🔧 Configuring systemd service...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable trading-bot-interactive

# Create start script for easy management
cat > start_bot.sh << 'EOF'
#!/bin/bash
sudo systemctl start trading-bot-interactive
echo "✅ Interactive Trading Bot started"
sudo systemctl status trading-bot-interactive --no-pager -l
EOF
chmod +x start_bot.sh

# Create stop script
cat > stop_bot.sh << 'EOF'
#!/bin/bash
sudo systemctl stop trading-bot-interactive
echo "🛑 Interactive Trading Bot stopped"
EOF
chmod +x stop_bot.sh

# Create status script
cat > status_bot.sh << 'EOF'
#!/bin/bash
echo "📊 Interactive Trading Bot Status:"
sudo systemctl status trading-bot-interactive --no-pager -l
echo ""
echo "📜 Recent logs:"
sudo journalctl -u trading-bot-interactive -n 10 --no-pager
EOF
chmod +x status_bot.sh

# Create logs script
cat > logs_bot.sh << 'EOF'
#!/bin/bash
echo "📜 Following bot logs (Ctrl+C to exit):"
sudo journalctl -u trading-bot-interactive -f
EOF
chmod +x logs_bot.sh

# Set proper ownership
sudo chown $BOT_USER:$BOT_USER *.sh

echo ""
echo -e "${GREEN}🎉 Interactive Trading Bot Deployment Complete!${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Edit the .env file with your credentials:"
echo "   nano $APP_DIR/.env"
echo ""
echo "2. Start the bot:"
echo "   ./start_bot.sh"
echo ""
echo -e "${BLUE}📊 Management Commands:${NC}"
echo "• Start bot:    ./start_bot.sh"
echo "• Stop bot:     ./stop_bot.sh" 
echo "• Bot status:   ./status_bot.sh"
echo "• View logs:    ./logs_bot.sh"
echo "• Update bot:   ./update.sh"
echo "• Health check: ./health_check.sh"
echo ""
echo -e "${BLUE}🔧 Manual Commands:${NC}"
echo "• Service status: sudo systemctl status trading-bot-interactive"
echo "• View logs:      sudo journalctl -u trading-bot-interactive -f"
echo "• Restart:        sudo systemctl restart trading-bot-interactive"
echo ""
echo -e "${YELLOW}⚠️  Important:${NC}"
echo "• Edit .env with your Telegram Bot Token, Chat ID, and OpenAI API Key"
echo "• Test with /start command in Telegram after starting"
echo "• Check logs if bot doesn't respond"
echo ""
echo -e "${GREEN}🚀 Ready to deploy!${NC}" 