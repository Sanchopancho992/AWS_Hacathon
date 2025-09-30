#!/bin/bash

# EC2 Deployment Script for Smart Tourism AI Backend
# Run this on your EC2 instance (Ubuntu 20.04/22.04)

echo "🚀 Setting up Smart Tourism AI Backend on EC2..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.9+ and pip
sudo apt install python3.9 python3.9-venv python3-pip -y

# Install Node.js (for PM2)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 globally
sudo npm install -g pm2

# Install Nginx
sudo apt install nginx -y

# Clone repository (replace with your repo URL)
cd /home/ubuntu
git clone https://github.com/yourusername/smart-tourism-ai.git
cd smart-tourism-ai

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Create environment file (you'll need to edit this with your keys)
cp .env.example .env
echo "⚠️  Please edit /home/ubuntu/smart-tourism-ai/backend/.env with your API keys"

# Create PM2 ecosystem file
cat > ecosystem.config.js << 'EOL'
module.exports = {
  apps: [{
    name: 'tourism-ai-backend',
    script: '/home/ubuntu/smart-tourism-ai/venv/bin/python',
    args: '/home/ubuntu/smart-tourism-ai/backend/main.py',
    cwd: '/home/ubuntu/smart-tourism-ai/backend',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production',
      PORT: 8000
    }
  }]
};
EOL

# Configure Nginx
sudo tee /etc/nginx/sites-available/tourism-ai << 'EOL'
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain or EC2 public IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
EOL

# Enable the site
sudo ln -s /etc/nginx/sites-available/tourism-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Start the application with PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup

echo "✅ Deployment complete!"
echo "📝 Next steps:"
echo "1. Edit /home/ubuntu/smart-tourism-ai/backend/.env with your API keys"
echo "2. Restart the app: pm2 restart tourism-ai-backend"
echo "3. Configure your domain in /etc/nginx/sites-available/tourism-ai"
echo "4. Get SSL certificate: sudo certbot --nginx"
echo "5. Open port 80 and 443 in EC2 security group"
