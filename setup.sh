echo "Creating env directory..." &&
    python3 -m venv env &&
    echo "env directory has created" &&
    . env/bin/activate &&
    echo "Upgrading pip..." &&
    python -m pip install --upgrade pip &&
    echo "pip has upgraded" &&
    echo "Installing requirements..." &&
    pip install -r requirements.txt &&
    echo "requirements has installed" &&
    deactivate &&
    echo "Environment has setup successfully!" &&
    echo "Creating SSL certificate..." &&
    openssl req -newkey rsa:2048 -sha256 -nodes -keyout private.key -x509 -days 3650 -out cert.pem &&
    echo "SSL certificate has created successfully!"
