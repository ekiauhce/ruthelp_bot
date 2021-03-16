# How to deploy on ubuntu server 20.04 

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

## Bot as systemd service

Create file `/etc/systemd/system/ruthelp.service`:
```
[Unit]
Description=Service of telegram bot @ruthelp_bot
Wants=network.target
After=network.target

[Service]
Environment="TG_API_TOKEN=YOUR:TOKEN"

# Change to actual path in your system 
WorkingDirectory=/home/ekiauhce/code/python/ruthelp_bot/src/

# Pull updates from github repo
ExecStartPre=/usr/bin/git pull

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
sudo systemctl daemon-reload
sudo systemctl enable ruthelp
sudo systectml start ruthelp
```
Bot will start on every reboot and automatically restart when crash

## View logs
```
less -N +G /var/log/ruthelp.log
```
