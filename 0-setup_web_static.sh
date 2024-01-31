#!/usr/bin/env bash
# A Bash script that sets up your web servers for the deployment of web_static

# Create folders
sudo mkdir -p /data/web_static/{shared,releases/test}
echo "Index html content" | sudo tee /data/web_static/releases/test/index.html > /dev/null
sudo chown -R ubuntu:ubuntu /data/

# Create a symbolic link
sudo ln -sfn /data/web_static/releases/test/ /data/web_static/current

# Update NGINX configuration
nginx_config="/etc/nginx/sites-available/default"
echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html;

    location /redirect_me {
        return 301 https://upschool.com/register;
    }

    error_page 404 /404.html;
    location = /404.html {
        internal;
    }

    location / {
        add_header X-Served-By \$hostname;
        try_files \$uri \$uri/ =404;
    }

    location /hbnb_static/ {
        alias /data/web_static/current/;
    }
}" | sudo tee $nginx_config

# Test Configuration
sudo nginx -t

# Restart NGINX
sudo service nginx restart
