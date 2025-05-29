#!/bin/bash

# Indonesian Trading Bot - Server Deployment Script
# Run this script on your Ubuntu/Debian server

echo "🇮🇩 Indonesian Trading Bot - Server Deployment"
echo "=============================================="

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3.9+ and pip
echo "🐍 Installing Python and dependencies..."
sudo apt install -y python3 python3-pip python3-venv git curl wget

# Install system dependencies for matplotlib and other packages
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y pkg-config libfreetype6-dev libpng-dev

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /opt/trading-bot
sudo chown $USER:$USER /opt/trading-bot
cd /opt/trading-bot

# Clone repository (replace with your actual repo URL)
echo "📥 Cloning repository..."
# git clone https://github.com/yourusername/indonesian-trading-bot.git .
# For now, we'll create the directory structure
mkdir -p logs backups

# Create Python virtual environment
echo "🔧 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip

# Create requirements.txt if not exists
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

pip install -r requirements.txt

# Create systemd service file
echo "⚙️ Creating systemd service..."
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
ExecStart=/opt/trading-bot/venv/bin/python /opt/trading-bot/trading_bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create log rotation configuration
echo "📝 Setting up log rotation..."
sudo tee /etc/logrotate.d/trading-bot > /dev/null << EOF
/opt/trading-bot/trading_bot.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 $USER $USER
}
EOF

# Create backup script
echo "💾 Creating backup script..."
cat > backup.sh << 'EOF'
#!/bin/bash
# Backup script for trading bot

BACKUP_DIR="/opt/trading-bot/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="trading_bot_backup_$DATE.tar.gz"

# Create backup
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    --exclude="venv" \
    --exclude="backups" \
    --exclude="__pycache__" \
    --exclude="*.pyc" \
    /opt/trading-bot/

# Keep only last 7 backups
cd "$BACKUP_DIR"
ls -t trading_bot_backup_*.tar.gz | tail -n +8 | xargs -r rm

echo "Backup created: $BACKUP_FILE"
EOF

chmod +x backup.sh

# Create monitoring script
echo "📊 Creating monitoring script..."
cat > monitor.sh << 'EOF'
#!/bin/bash
# Monitoring script for trading bot

SERVICE_NAME="trading-bot"
LOG_FILE="/opt/trading-bot/trading_bot.log"

# Check if service is running
if systemctl is-active --quiet $SERVICE_NAME; then
    echo "✅ Trading Bot is running"
else
    echo "❌ Trading Bot is not running"
    echo "🔄 Attempting to restart..."
    sudo systemctl restart $SERVICE_NAME
    sleep 5
    if systemctl is-active --quiet $SERVICE_NAME; then
        echo "✅ Trading Bot restarted successfully"
    else
        echo "❌ Failed to restart Trading Bot"
        echo "📋 Service status:"
        sudo systemctl status $SERVICE_NAME
    fi
fi

# Show recent logs
echo ""
echo "📝 Recent logs (last 10 lines):"
tail -n 10 $LOG_FILE

# Show system resources
echo ""
echo "💻 System resources:"
echo "Memory usage: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo "Disk usage: $(df -h /opt/trading-bot | awk 'NR==2 {print $3 "/" $2 " (" $5 ")"}')"
echo "CPU load: $(uptime | awk -F'load average:' '{print $2}')"
EOF

chmod +x monitor.sh

# Create update script
echo "🔄 Creating update script..."
cat > update.sh << 'EOF'
#!/bin/bash
# Update script for trading bot

echo "🔄 Updating Trading Bot..."

# Stop the service
sudo systemctl stop trading-bot

# Backup current version
./backup.sh

# Activate virtual environment
source venv/bin/activate

# Update Python packages
pip install --upgrade -r requirements.txt

# Pull latest code (uncomment when using git)
# git pull origin main

# Restart the service
sudo systemctl start trading-bot

# Check status
sleep 5
if systemctl is-active --quiet trading-bot; then
    echo "✅ Trading Bot updated and restarted successfully"
else
    echo "❌ Update failed, check logs"
    sudo systemctl status trading-bot
fi
EOF

chmod +x update.sh

# Create environment file template
echo "📝 Creating environment file template..."
cat > .env.example << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
EOF

echo ""
echo "✅ Server deployment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Copy your bot files to /opt/trading-bot/"
echo "2. Create .env file with your credentials:"
echo "   cp .env.example .env"
echo "   nano .env"
echo "3. Enable and start the service:"
echo "   sudo systemctl enable trading-bot"
echo "   sudo systemctl start trading-bot"
echo "4. Check status:"
echo "   sudo systemctl status trading-bot"
echo "   ./monitor.sh"
echo ""
echo "🔧 Useful commands:"
echo "   ./monitor.sh     - Check bot status and logs"
echo "   ./backup.sh      - Create backup"
echo "   ./update.sh      - Update bot"
echo "   sudo systemctl restart trading-bot  - Restart service"
echo "   sudo journalctl -u trading-bot -f   - View live logs" 