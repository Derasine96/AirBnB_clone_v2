#!/usr/bin/env bash
# A Bash script that sets up your web servers for the deployment of web_static

# Check if Nginx is installed
if ! command -v nginx &> /dev/null
then
    sudo apt-get update
    sudo apt-get install nginx -y
fi

# Create folders
sudo mkdir -p /data/web_static/{shared,releases/test}
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Give ownership to /data
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
}" | sudo tee $nginx_config > /dev/null

# Restart NGINX
sudo service nginx restart

exit 0
