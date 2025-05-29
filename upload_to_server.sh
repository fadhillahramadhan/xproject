#!/bin/bash

# Upload Bot Files to Server Script
# Run this from your local machine to upload files to server

echo "📤 Upload Trading Bot to Server"
echo "==============================="

# Check if server details are provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <server_ip> <username> [ssh_key_path]"
    echo ""
    echo "Examples:"
    echo "  $0 192.168.1.100 tradingbot"
    echo "  $0 your-server.com tradingbot ~/.ssh/id_rsa"
    echo ""
    exit 1
fi

SERVER_IP=$1
USERNAME=$2
SSH_KEY=${3:-""}

# Build SSH command
if [ -n "$SSH_KEY" ]; then
    SSH_CMD="ssh -i $SSH_KEY"
    SCP_CMD="scp -i $SSH_KEY"
else
    SSH_CMD="ssh"
    SCP_CMD="scp"
fi

echo "🎯 Target: $USERNAME@$SERVER_IP"
echo "📁 Uploading to: /opt/trading-bot/"

# Test connection
echo "🔍 Testing connection..."
if ! $SSH_CMD $USERNAME@$SERVER_IP "echo 'Connection successful'"; then
    echo "❌ Cannot connect to server"
    echo "   Check your server IP, username, and SSH key"
    exit 1
fi

# List of files to upload
FILES_TO_UPLOAD=(
    "trading_bot.py"
    "config.py"
    "run_production.py"
    "test_single_stock.py"
    "test_enhanced_chatgpt.py"
    "requirements.txt"
    ".env"
)

# Optional files
OPTIONAL_FILES=(
    "watchlist_manager.py"
    "README.md"
    "DEPLOYMENT_GUIDE.md"
)

echo ""
echo "📦 Uploading core files..."

# Upload core files
for file in "${FILES_TO_UPLOAD[@]}"; do
    if [ -f "$file" ]; then
        echo "📤 Uploading $file..."
        $SCP_CMD "$file" $USERNAME@$SERVER_IP:/opt/trading-bot/
    else
        if [ "$file" = ".env" ]; then
            echo "⚠️  $file not found - you'll need to create it on the server"
        else
            echo "❌ $file not found - this file is required!"
        fi
    fi
done

echo ""
echo "📦 Uploading optional files..."

# Upload optional files
for file in "${OPTIONAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "📤 Uploading $file..."
        $SCP_CMD "$file" $USERNAME@$SERVER_IP:/opt/trading-bot/
    else
        echo "⚠️  $file not found - skipping"
    fi
done

echo ""
echo "🔧 Setting up environment on server..."

# Create .env file if it doesn't exist
$SSH_CMD $USERNAME@$SERVER_IP << 'EOF'
cd /opt/trading-bot

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env template..."
    cat > .env << 'ENVEOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
ENVEOF
    echo "⚠️  Please edit .env file with your actual credentials"
fi

# Set permissions
chmod 600 .env 2>/dev/null || true
chmod +x *.sh 2>/dev/null || true

echo "✅ Files uploaded successfully!"
EOF

echo ""
echo "✅ Upload complete!"
echo ""
echo "📋 Next steps on server:"
echo "1. SSH to your server:"
echo "   $SSH_CMD $USERNAME@$SERVER_IP"
echo ""
echo "2. Configure environment:"
echo "   cd /opt/trading-bot"
echo "   nano .env"
echo "   # Add your actual Telegram and OpenAI credentials"
echo ""
echo "3. Test the bot:"
echo "   source venv/bin/activate"
echo "   python run_production.py test"
echo ""
echo "4. Start the service:"
echo "   sudo systemctl enable trading-bot"
echo "   sudo systemctl start trading-bot"
echo ""
echo "5. Monitor:"
echo "   ./monitor.sh"
echo "   sudo journalctl -u trading-bot -f"
echo ""
echo "🔑 Don't forget to configure your .env file with real credentials!" 