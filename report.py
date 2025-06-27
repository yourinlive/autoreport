#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FB Report Tool v3.0 - The Ultimate OPSEC Solution

import requests
import random
import threading
import time
from bs4 import BeautifulSoup
from datetime import datetime
import os
import sys
# ===== CONFIGURATION =====
MAX_THREADS = 3 # Keep low to avoid detection
PROXY_FILE = 'proxy.txt'
MIN_DELAY = 2.5 # Minimum seconds between actions
MAX_DELAY = 8.0 # Maximum seconds between actions

# ===== HARDCODED USER AGENTS =====
USER_AGENTS = [
    # Windows Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    
    # Mobile iOS
    "Mozilla/5.0 (iPhone14,6; U; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/15.0 Mobile/19E241 Safari/602.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    
    # Android
    "Mozilla/5.0 (Linux; Android 13; SM-S901U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    
    # MacOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
]

# ===== CORE FUNCTIONS =====
def load_proxies(filename=PROXY_FILE):
    """Load and validate proxies with automatic retry system"""
    try:
        with open(filename, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        
        # Initial validation
        working_proxies = []
        for proxy in proxies[:50]: # Test first 50 only
            if test_proxy(proxy):
                working_proxies.append(proxy)
        
        return working_proxies
    except:
        return []

def test_proxy(proxy):
    """Comprehensive proxy health check"""
    test_urls = [
        "https://www.facebook.com/robots.txt",
        "https://www.google.com/gen_204"
    ]
    
    for url in test_urls:
        try:
            session = requests.Session()
            proxies_config = {
                'http': proxy,
                'https': proxy
            }
            response = session.get(
                url,
                proxies=proxies_config,
                timeout=15,
                headers={'User-Agent': random.choice(USER_AGENTS)}
            )
            if response.status_code < 400:
                return True
        except:
            continue
    return False

def get_random_reason():
    """Weighted reason code selection"""
    weighted_reasons = {
        1: 30, # Spam
        2: 20, # Fake Account
        3: 15, # Harassment
        6: 35 # Scams (Higher success rate)
    }
    return random.choices(
        list(weighted_reasons.keys()),
        weights=weighted_reasons.values(),
        k=1
    )[0]

def simulate_human_behavior():
    """Advanced human-like interaction patterns"""
    behaviors = [
        lambda: time.sleep(random.gauss(3.5, 1.2)), # Normal distribution
        lambda: [time.sleep(0.1 + random.random()/2) for _ in range(random.randint(2,5))], # Multiple micro-delays
        lambda: time.sleep(random.uniform(MIN_DELAY, MAX_DELAY)) # Standard delay
    ]
    random.choice(behaviors)()

def is_safe_hour():
    """Check if current time is within operational window"""
    now = datetime.utcnow().hour
    return (7 <= now <= 23) # 8AM-11PM across major timezones

def generate_headers():
    """Create unique browser fingerprint for each request"""
    base_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers'
    }
    
    # Dynamic fingerprint components
    if random.random() > 0.5: # 50% chance for mobile
        base_headers.update({
            'User-Agent': random.choice([ua for ua in USER_AGENTS if 'Mobile' in ua or 'iPhone' in ua or 'Android' in ua]),
            'Sec-CH-UA-Mobile': '?1',
            'X-FB-Connection-Type': 'cellular'
        })
    else:
        base_headers.update({
            'User-Agent': random.choice([ua for ua in USER_AGENTS if 'Mobile' not in ua]),
            'Sec-CH-UA-Mobile': '?0'
        })
    
    # Chrome-specific headers
    if 'Chrome' in base_headers['User-Agent']:
        base_headers.update({
            'Sec-CH-UA': '"Not_A Brand";v="8", "Chromium";v="120"',
            'Sec-CH-UA-Platform': '"Windows"' if 'Windows' in base_headers['User-Agent'] else '"macOS"'
        })
    
    return base_headers

def get_fb_dtsg(session, headers):
    """Extract FB DTSG token from page"""
    try:
        response = session.get('https://www.facebook.com', headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find('input', {'name': 'fb_dtsg'})['value']
    except:
        return None

def report_content(target_url, proxy=None):
    """Submit report for target content"""
    try:
        session = requests.Session()
        
        if proxy:
            session.proxies = {
                'http': proxy,
                'https': proxy
            }
        
        headers = generate_headers()
        fb_dtsg = get_fb_dtsg(session, headers)
        
        if not fb_dtsg:
            print("[!] Failed to get FB DTSG token")
            return False
        
        # Simulate viewing the content first
        time.sleep(random.uniform(1.5, 4.0))
        session.get(target_url, headers=headers)
        
        # Prepare report payload
        report_url = "https://www.facebook.com/ajax/report/submit.php"
        payload = {
            'fb_dtsg': fb_dtsg,
            'reportable_type': "user" if "/profile.php" in target_url or "/groups/" not in target_url else "group_post",
            'reportable_id': target_url.split('/')[-1].split('?')[0],
            'source': "www",
            'reason_id': get_random_reason(),
            'context_id': "",
            'flow': "report_dialog",
            'referrer': target_url,
            '__user': "0",
            '__a': "1",
            '__dyn': "7xeUmwlEnwn8K2WnFw9-2i5U4e0yoW3q322aew9G2S0zU2lwUx60gu0luq1ew65xO0FE2awgq0yK5o4q2O1Vw8G2i0Bo7O3q0HU9k2C221MDw",
            '__csr': "",
            '__req': "r",
            '__beoa': "0",
            '__pc': "PHASED:DEFAULT",
            'dpr': "1",
            '__ccg': "EXCELLENT",
            '__rev': "1000000000",
            '__s': "",
            '__hsi': "",
            '__comet_req': "0",
            'lsd': "",
            'jazoest': "2981",
            '__spin_r': "1000000000",
            '__spin_b': "trunk",
            '__spin_t': "1234567890"
        }
        
        # Submit report
        simulate_human_behavior()
        response = session.post(report_url, data=payload, headers=headers)
        
        if response.status_code == 200 and '"success":true' in response.text:
            print(f"[+] Successfully reported: {target_url}")
            return True
        else:
            print(f"[-] Failed to report: {target_url}")
            return False
            
    except Exception as e:
        print(f"[!] Error reporting {target_url}: {str(e)}")
        return False

def worker(target_url, proxy_pool):
    """Thread worker for reporting"""
    while True:
        if not proxy_pool:
            proxy = None
        else:
            proxy = random.choice(proxy_pool)
        
        if report_content(target_url, proxy):
            break
        
        # If failed, wait longer before retry
        time.sleep(random.uniform(10, 30))

def main():
    """Main execution function"""
    if not is_safe_hour():
        print("[!] Warning: Operating outside recommended hours increases detection risk")
    
    print("=== FB Report Tool v3.0 ===")
    print("[*] Loading proxies...")
    proxy_pool = load_proxies()
    
    if proxy_pool:
        print(f"[+] Loaded {len(proxy_pool)} working proxies")
    else:
        print("[!] No working proxies found - using direct connection")
    
    target_url = input("[?] Enter target URL: ").strip()
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url
    
    thread_count = min(MAX_THREADS, len(proxy_pool) if proxy_pool else 1)
    print(f"[*] Starting {thread_count} threads...")
    
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(target_url, proxy_pool))
        t.daemon = True
        t.start()
        threads.append(t)
        time.sleep(random.uniform(0.5, 2.0))
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
