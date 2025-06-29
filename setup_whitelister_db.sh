#!/bin/bash

set -e

# --- Configuration ---
DB_NAME="postgres"
DB_USER="postgres"
DB_PASSWORD="your_password_here"
DB_PORT="5432"
DB_HOST="localhost"
ETH_RPC_URL="https://rpc.flashbots.net"

# --- Update and install PostgreSQL ---
echo "[*] Installing PostgreSQL..."
sudo apt update
sudo apt install -y postgresql postgresql-contrib

# --- Ensure PostgreSQL is started ---
echo "[*] Enabling and starting PostgreSQL service..."
sudo systemctl enable postgresql
sudo systemctl start postgresql

# --- Set PostgreSQL user password ---
echo "[*] Setting PostgreSQL user password..."
sudo -u postgres psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"

# --- Create DB if it doesn't exist ---
echo "[*] Creating database $DB_NAME if not exists..."
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"

# --- Show success ---
echo "[✓] PostgreSQL setup complete"

# --- Write environment variables to .env ---
echo "[*] Writing environment variables to .env"
cat <<EOF > .env
WHITELISTER_DB_ENGINE=django.db.backends.postgresql
WHITELISTER_DB_NAME=$DB_NAME
WHITELISTER_DB_USER=$DB_USER
WHITELISTER_DB_PASSWORD=$DB_PASSWORD
WHITELISTER_DB_HOST=$DB_HOST
WHITELISTER_DB_PORT=$DB_PORT
ETH_RPC_URL=$ETH_RPC_URL
EOF

echo "[✓] .env file created"

# --- Optional: Install Python dependencies ---
# echo "[*] Installing Python requirements..."
# pip install -r requirements.txt

echo "[✅] Whitelister DB environment is ready."