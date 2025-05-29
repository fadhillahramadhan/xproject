#!/bin/bash

# Quick Deploy Script for Indonesian Trading Bot
# Run this on your server for immediate deployment

set -e  # Exit on any error

echo "🚀 Indonesian Trading Bot - Quick Deploy"
echo "========================================"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run this script as root"
    echo "   Create a regular user first:"
    echo "   adduser tradingbot"
    echo "   usermod -aG sudo tradingbot"
    echo "   su - tradingbot"
    exit 1
fi

# Update system
echo "📦 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo "🐍 Installing dependencies..."
sudo apt install -y python3 python3-pip python3-venv git curl wget nano htop

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p /opt/trading-bot
sudo chown $USER:$USER /opt/trading-bot
cd /opt/trading-bot

# Create Python virtual environment
echo "🔧 Creating Python environment..."
python3 -m venv venv
source venv/bin/activate

# Create requirements.txt
echo "📦 Creating requirements file..."
cat > requirements.txt << 'EOF'
yfinance==0.2.28
pandas==2.1.4
numpy==1.24.3
matplotlib==3.7.2
python-telegram-bot==20.7
python-dotenv==1.0.0
openai==1.3.8
schedule==1.2.0
asyncio
aiohttp==3.9.1
requests==2.31.0
Pillow==10.1.0
EOF

# Install Python packages
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Create directories
mkdir -p logs backups

# Create environment template
echo "📝 Creating environment template..."
cat > .env.example << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
EOF

# Create systemd service
echo "⚙️ Creating system service..."
sudo tee /etc/systemd/system/trading-bot.service > /dev/null << EOF
[Unit]
Description=Indonesian Trading Bot
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/trading-bot
Environment=PATH=/opt/trading-bot/venv/bin
ExecStart=/opt/trading-bot/venv/bin/python /opt/trading-bot/run_production.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create monitoring script
echo "📊 Creating monitoring script..."
cat > monitor.sh << 'EOF'
#!/bin/bash
echo "🤖 Trading Bot Status Check"
echo "=========================="

if systemctl is-active --quiet trading-bot; then
    echo "✅ Status: Running"
else
    echo "❌ Status: Stopped"
fi

echo ""
echo "📝 Recent logs:"
sudo journalctl -u trading-bot -n 5 --no-pager

echo ""
echo "💻 System resources:"
echo "Memory: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo "Disk: $(df -h /opt/trading-bot | awk 'NR==2 {print $3 "/" $2 " (" $5 ")"}')"
EOF

chmod +x monitor.sh

# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backups/trading_bot_backup_$DATE.tar.gz"

tar -czf "$BACKUP_FILE" \
    --exclude="venv" \
    --exclude="backups" \
    --exclude="__pycache__" \
    --exclude="*.pyc" \
    .

echo "Backup created: $BACKUP_FILE"
EOF

chmod +x backup.sh

# Reload systemd
sudo systemctl daemon-reload

echo ""
echo "✅ Quick deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Copy your bot files to /opt/trading-bot/"
echo "   - trading_bot.py"
echo "   - config.py" 
echo "   - run_production.py"
echo "   - test_single_stock.py"
echo "   - (all your bot files)"
echo ""
echo "2. Create .env file with your credentials:"
echo "   cp .env.example .env"
echo "   nano .env"
echo ""
echo "3. Test the bot:"
echo "   cd /opt/trading-bot"
echo "   source venv/bin/activate"
echo "   python run_production.py test"
echo ""
echo "4. Start the service:"
echo "   sudo systemctl enable trading-bot"
echo "   sudo systemctl start trading-bot"
echo ""
echo "5. Monitor the bot:"
echo "   ./monitor.sh"
echo "   sudo journalctl -u trading-bot -f"
echo ""
echo "🔧 Useful commands:"
echo "   ./monitor.sh                    - Check status"
echo "   ./backup.sh                     - Create backup"
echo "   sudo systemctl restart trading-bot  - Restart"
echo "   sudo journalctl -u trading-bot -f   - View logs"
echo ""
echo "📁 Bot files should be placed in: /opt/trading-bot/"
echo "🔑 Don't forget to configure your .env file!" 