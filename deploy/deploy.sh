#!/bin/bash

# Exit on error
set -e

# Load environment variables
source .env

# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages if not present
sudo apt-get install -y python3-pip python3-venv nginx

# Create project directory if it doesn't exist
sudo mkdir -p /var/www/jobhelp
sudo chown -R $USER:$USER /var/www/jobhelp

# Setup Python virtual environment
cd /var/www/jobhelp/backend
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install gunicorn

# Download NLTK data
python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"

# Install Node.js and npm if not present
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Setup frontend
cd /var/www/jobhelp/frontend
npm install
npm run build

# Setup systemd service for backend
sudo tee /etc/systemd/system/jobhelp-backend.service << EOF
[Unit]
Description=JobHelp Backend
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=/var/www/jobhelp/backend
Environment="PATH=/var/www/jobhelp/backend/venv/bin"
ExecStart=/var/www/jobhelp/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
EOF

# Setup systemd service for frontend
sudo tee /etc/systemd/system/jobhelp-frontend.service << EOF
[Unit]
Description=JobHelp Frontend
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=/var/www/jobhelp/frontend
Environment="PATH=/usr/bin"
ExecStart=/usr/bin/npm start

[Install]
WantedBy=multi-user.target
EOF

# Setup Nginx configuration
sudo tee /etc/nginx/sites-available/jobhelp << EOF
server {
    listen 80;
    server_name your_domain.com;  # Replace with your domain

    # Frontend
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Enable the Nginx configuration
sudo ln -sf /etc/nginx/sites-available/jobhelp /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Start and enable services
sudo systemctl daemon-reload
sudo systemctl enable jobhelp-backend
sudo systemctl enable jobhelp-frontend
sudo systemctl start jobhelp-backend
sudo systemctl start jobhelp-frontend
sudo systemctl restart nginx

echo "Deployment completed successfully!"
