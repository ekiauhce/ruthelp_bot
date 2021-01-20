# @ruthelp_bot completely guide to setup on Ubuntu server 20.04 

## Install python and venv

```
sudo apt update && sudo apt install python3.8 python3-venv
```

## Install from github

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

## Make main.py and init_db.py executable
```
chmod u+x src/main.py
chmod u+x src/init_db.py
```
## Before launch

```
```
