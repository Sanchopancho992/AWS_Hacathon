# 🚀 Deployment Guide - Smart Tourism AI

## Quick Deploy Options

### Option 1: AWS EC2 Free Tier (Recommended)
**Cost**: Free for 1 year
**Difficulty**: Medium

### Option 2: Docker Containers
**Cost**: Varies by provider
**Difficulty**: Easy

### Option 3: Vercel + Railway
**Cost**: Free tier available
**Difficulty**: Easy

---

## 🛡️ Option 1: AWS EC2 Free Tier Deployment

### Step 1: Launch EC2 Instance

1. **Go to AWS Console** → EC2 → Launch Instance
2. **Choose AMI**: Ubuntu Server 22.04 LTS
3. **Instance Type**: t2.micro (free tier)
4. **Key Pair**: Create new or use existing
5. **Security Group**: Allow HTTP (80), HTTPS (443), SSH (22)
6. **Storage**: 30GB gp2 (free tier)

### Step 2: Connect to Instance

```bash
# Replace with your key and instance IP
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### Step 3: Run Deployment Script

```bash
# Download and run the deployment script
wget https://raw.githubusercontent.com/yourusername/smart-tourism-ai/main/deploy-ec2.sh
chmod +x deploy-ec2.sh
sudo ./deploy-ec2.sh
```

### Step 4: Configure Environment

```bash
# Edit environment variables
sudo nano /home/ubuntu/smart-tourism-ai/backend/.env

# Add your API keys:
GOOGLE_API_KEY=AIzaSyC9LxA1u1a2SPP8n4U67mvMqH81N9OZF28
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=awshacathon
PINECONE_HOST=your_pinecone_host
```

### Step 5: Start the Application

```bash
cd /home/ubuntu/smart-tourism-ai
pm2 restart tourism-ai-backend
```

### Step 6: Configure Domain (Optional)

```bash
# Update nginx config with your domain
sudo nano /etc/nginx/sites-available/tourism-ai

# Install SSL certificate
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx
```

---

## 🐳 Option 2: Docker Deployment

### Prerequisites
- Docker and Docker Compose installed
- Server with public IP

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/smart-tourism-ai.git
cd smart-tourism-ai
```

### Step 2: Configure Environment

```bash
# Copy and edit environment file
cp backend/.env.example backend/.env
nano backend/.env
```

### Step 3: Deploy with Docker

```bash
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f
```

### Step 4: Configure Reverse Proxy

```nginx
# /etc/nginx/sites-available/tourism-ai
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## ☁️ Option 3: Vercel + Railway

### Backend on Railway

1. **Connect GitHub**: Link your repository to Railway
2. **Environment Variables**: Add all required env vars
3. **Deploy**: Railway auto-deploys from main branch

### Frontend on Vercel

1. **Connect GitHub**: Link repository to Vercel
2. **Build Settings**:
   - Framework: Create React App
   - Root Directory: frontend
   - Build Command: `npm run build`
3. **Environment Variables**: Add backend URL

---

## 🔧 Environment Variables Reference

### Required Variables

```env
# Google Gemini (Required)
GOOGLE_API_KEY=AIzaSyC9LxA1u1a2SPP8n4U67mvMqH81N9OZF28

# Pinecone (Required)
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=awshacathon
PINECONE_HOST=https://awshacathon-plk6ggn.svc.aped-4627-b74a.pinecone.io

# AWS (Optional - for translation features)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
```

### Frontend Environment

```env
# frontend/.env.production
REACT_APP_API_URL=https://your-backend-domain.com
```

---

## 🎯 Production Checklist

### Security
- [ ] Use HTTPS (SSL certificate)
- [ ] Configure CORS properly
- [ ] Hide .env files from version control
- [ ] Use environment variables for all secrets
- [ ] Configure firewall rules

### Performance
- [ ] Enable gzip compression
- [ ] Configure caching headers
- [ ] Use CDN for static assets
- [ ] Monitor resource usage
- [ ] Set up health checks

### Monitoring
- [ ] Set up error logging
- [ ] Configure uptime monitoring
- [ ] Monitor API usage
- [ ] Set up alerts for failures

---

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check logs
pm2 logs tourism-ai-backend

# Check environment variables
pm2 show tourism-ai-backend
```

**Frontend build fails:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

**API errors:**
- Check if API keys are valid
- Verify Pinecone index exists
- Check network connectivity

### Health Check Endpoints

- Backend: `http://your-domain/health`
- Frontend: Should return React app

---

## 📱 Mobile Deployment (PWA)

The app is automatically a PWA! Users can:

1. **Visit the website** on mobile
2. **Add to Home Screen** (iOS/Android)
3. **Use offline** (cached content)

---

## 💰 Cost Estimation

### AWS EC2 (Free Tier)
- **EC2 t2.micro**: Free for 12 months
- **Storage**: 30GB free
- **Data Transfer**: 1GB/month free
- **Total**: $0 for first year

### After Free Tier
- **EC2 t3.micro**: ~$8.50/month
- **Storage**: ~$3/month
- **Data Transfer**: ~$5/month (50GB)
- **Total**: ~$16.50/month

### API Costs
- **Google Gemini**: Very low cost (pay per use)
- **Pinecone**: Free tier available
- **Total API costs**: <$5/month for moderate usage

---

## 🚀 Go Live Steps

1. **Choose deployment option** (EC2 recommended)
2. **Set up infrastructure** (server, domain)
3. **Configure environment** (API keys, secrets)
4. **Deploy application** (using provided scripts)
5. **Test thoroughly** (all features working)
6. **Monitor and maintain** (logs, uptime)

---

**Need help?** Open an issue in the GitHub repository!
