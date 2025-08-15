# Deployment Guide

This guide covers both free deployment options and VPS deployment for the JobHelp application.

## Free Deployment Options

### Frontend Deployment (Vercel)
1. Sign up for a free account at [Vercel](https://vercel.com)
2. Connect your GitHub repository
3. Configure the project:
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`
4. Add environment variables:
   ```
   NEXT_PUBLIC_API_URL=your_backend_url
   ```

### Backend Deployment (Railway)
1. Sign up for a free account at [Railway](https://railway.app)
2. Connect your GitHub repository
3. Create a new project and select the Python template
4. Configure the deployment:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables as needed

## VPS Deployment

### Prerequisites
1. A VPS instance (DigitalOcean, Linode, AWS EC2, etc.)
2. Domain name (optional but recommended)
3. SSH access to the server

### Initial Server Setup
1. SSH into your server:
   ```bash
   ssh root@your_server_ip
   ```

2. Create a non-root user:
   ```bash
   adduser jobhelp
   usermod -aG sudo jobhelp
   ```

3. Setup SSH keys:
   ```bash
   mkdir -p /home/jobhelp/.ssh
   cp ~/.ssh/authorized_keys /home/jobhelp/.ssh/
   chown -R jobhelp:jobhelp /home/jobhelp/.ssh
   ```

### GitHub Actions Setup
1. Add the following secrets to your GitHub repository:
   - `SSH_PRIVATE_KEY`: Your SSH private key
   - `SERVER_IP`: Your VPS IP address
   - `SERVER_USER`: Your server username (e.g., jobhelp)

### Manual Deployment
1. Clone the repository on your VPS:
   ```bash
   git clone https://github.com/yourusername/jobhelp.git
   ```

2. Make the deployment script executable:
   ```bash
   chmod +x deploy/deploy.sh
   ```

3. Run the deployment script:
   ```bash
   ./deploy/deploy.sh
   ```

### SSL Setup (Optional but Recommended)
1. Install Certbot:
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   ```

2. Obtain SSL certificate:
   ```bash
   sudo certbot --nginx -d your_domain.com
   ```

## Monitoring and Maintenance

### View Logs
- Backend logs:
  ```bash
  sudo journalctl -u jobhelp-backend
  ```
- Frontend logs:
  ```bash
  sudo journalctl -u jobhelp-frontend
  ```
- Nginx logs:
  ```bash
  sudo tail -f /var/log/nginx/access.log
  sudo tail -f /var/log/nginx/error.log
  ```

### Common Commands
- Restart services:
  ```bash
  sudo systemctl restart jobhelp-backend
  sudo systemctl restart jobhelp-frontend
  sudo systemctl restart nginx
  ```
- Check service status:
  ```bash
  sudo systemctl status jobhelp-backend
  sudo systemctl status jobhelp-frontend
  ```

## Troubleshooting

### Common Issues
1. **502 Bad Gateway**
   - Check if backend service is running
   - Verify Nginx configuration
   - Check application logs

2. **Frontend Not Loading**
   - Verify Next.js build was successful
   - Check frontend service status
   - Review frontend logs

3. **API Connection Issues**
   - Verify CORS settings
   - Check API URL configuration
   - Ensure backend service is running

### Security Considerations
1. Enable UFW firewall:
   ```bash
   sudo ufw allow 22
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw enable
   ```

2. Regular updates:
   ```bash
   sudo apt-get update
   sudo apt-get upgrade
   ```

3. Monitor system resources:
   ```bash
   htop
   df -h
   ```
