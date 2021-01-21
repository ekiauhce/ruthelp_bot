# Completely guide to set up bot on Ubuntu server 20.04 

## Install python and venv

```
sudo apt update && sudo apt install python3.8 python3-venv
```

## Clone repo

```
git clone https://github.com/ekiauce/ruthelp_bot
cd ruthelp_bot/
```

## Setup environment

```
python3 -m venv env
. env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Create SSL certificate

```
mkdir ssl
openssl req -newkey rsa:2048 -sha256 -nodes -keyout ssl/private.key -x509 -days 3650 -out ssl/cert.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=your-domain-or-ip.com"
```

## Before launch

Create file `/etc/system/systemd/ruthelp.service`:
```
[Unit]
Description=Service of telegram bot @ruthelp_bot
Wants=network.target
After=network.target

[Service]
Environment="TG_API_TOKEN=YOUR:TOKEN"
Environment="HOST_IP=123.123.123.123"

WorkingDirectory=/home/ekiauhce/code/python/ruthelp_bot/src/

ExecStartPre=/home/ekiauhce/code/python/ruthelp_bot/env/bin/python init_db.py
ExecStart=/home/ekiauhce/code/python/ruthelp_bot/env/bin/python main.py

Restart=always
RestartSec=10

StandardOutput=append:/var/log/ruthelp.log
StandardError=inherit

[Install]
WantedBy=multi-user.target

```

## Enable and start service

```
sudo systemctl enable ruthelp
sudo systectml start ruthelp
```
Bot will start on every reboot and automatically restart when crash

## View logs
```
less -N +G /var/log/ruthelp.log
```