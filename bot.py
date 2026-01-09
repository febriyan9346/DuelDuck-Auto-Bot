import os
import time
import random
import requests
import base64
import json
import pytz
from datetime import datetime
from colorama import Fore, Style, init
from solders.keypair import Keypair
from solders.pubkey import Pubkey
import nacl.signing
import nacl.encoding

os.system('clear' if os.name == 'posix' else 'cls')

import warnings
warnings.filterwarnings('ignore')

import sys
if not sys.warnoptions:
    import os
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)

class DuelDuckAutoBot:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://duelduck.com',
            'referer': 'https://duelduck.com/',
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
        }
        self.session.headers.update(self.headers)
        self.base_url_captcha = "https://api.2captcha.com"

    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')
    
    def print_banner(self):
        banner = f"""
{Fore.CYAN}DUELDUCK AUTO BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)
    
    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    
    def random_delay(self):
        delay = random.randint(2, 5)
        self.log(f"Delay {delay} seconds...", "INFO")
        time.sleep(delay)

    def load_file(self, filename):
        try:
            with open(filename, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []
    
    def show_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)
    
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)

    def solve_captcha(self, api_key, website_url, website_key):
        payload = {
            "clientKey": api_key,
            "task": {
                "type": "TurnstileTaskProxyless",
                "websiteURL": website_url,
                "websiteKey": website_key
            }
        }
        
        self.log("Solving Captcha...", "INFO")
        try:
            response = requests.post(f"{self.base_url_captcha}/createTask", json=payload)
            result = response.json()
            
            if result.get("errorId") != 0:
                self.log(f"Captcha Error: {result.get('errorDescription')}", "ERROR")
                return None
            
            task_id = result.get("taskId")
            
            for _ in range(60):
                time.sleep(3)
                res = requests.post(f"{self.base_url_captcha}/getTaskResult", json={"clientKey": api_key, "taskId": task_id}).json()
                if res.get("status") == "ready":
                    self.log("Captcha Solved", "SUCCESS")
                    return res.get("solution", {}).get("token")
            
            self.log("Captcha Timeout", "ERROR")
            return None
        except Exception as e:
            self.log(f"Captcha Exception: {e}", "ERROR")
            return None

    def sign_message(self, keypair, message):
        secret_key_bytes = bytes(keypair)[:32]
        signing_key = nacl.signing.SigningKey(secret_key_bytes)
        signed = signing_key.sign(message.encode())
        return base64.b64encode(signed.signature).decode()

    def login(self, private_key, captcha_token):
        try:
            keypair = Keypair.from_base58_string(private_key)
            address = str(keypair.pubkey())
            secret = self.sign_message(keypair, address)
            
            payload = {
                "address": address,
                "chain_type": 0,
                "name": "Phantom",
                "secret": secret
            }
            
            headers = self.session.headers.copy()
            if captcha_token:
                headers['cf-turnstile-response'] = captcha_token
            
            response = self.session.post('https://api.duelduck.com/auth/sign-in-wallet', json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                token = data['jwt_info']['access_token']
                self.session.headers['authorization'] = f"Bearer {token}"
                return data
            elif response.status_code == 429:
                self.log("Login Rate Limited. Waiting 10s...", "WARNING")
                time.sleep(10)
                return None
            else:
                self.log(f"Login Failed: {response.status_code}", "ERROR")
                return None
        except Exception as e:
            self.log(f"Login Error: {e}", "ERROR")
            return None

    def get_duels(self, page_num=1):
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
        params = {
            "opts.pagination.page_size": "50",
            "opts.pagination.page_num": str(page_num),
            "opts.order.order_by": "created_at",
            "opts.order.order_type": "desc",
            "opts.filters[0].column": "status",
            "opts.filters[0].operator": "=",
            "opts.filters[0].value": "4",
            "opts.filters[0].where_or": "false",
            "opts.filters[1].column": "p.user_id",
            "opts.filters[1].operator": "is",
            "opts.filters[1].value": "null",
            "opts.filters[1].where_or": "false",
            "opts.filters[2].column": "deadline",
            "opts.filters[2].operator": ">",
            "opts.filters[2].value": current_time,
            "opts.filters[2].where_or": "false",
            "opts.filters[3].column": "subtopic",
            "opts.filters[3].operator": "not",
            "opts.filters[3].value": "DegenGames",
            "opts.filters[3].where_or": "false"
        }
        try:
            response = self.session.get('https://api.duelduck.com/duel/all-with-joined', params=params)
            if response.status_code == 200:
                data = response.json()
                filtered = []
                for d in data:
                    if d.get('status') == 4 and d.get('joined') == False:
                        filtered.append(d)
                return filtered
            return []
        except:
            return []

    def join_duel(self, duel_data):
        duel_id = duel_data.get('id')
        yes_count = duel_data.get('yes_count', 0)
        no_count = duel_data.get('no_count', 0)
        
        if yes_count > no_count:
            answer = 1
            reason = f"Following Majority (Yes: {yes_count} vs No: {no_count})"
        elif no_count > yes_count:
            answer = 0
            reason = f"Following Majority (No: {no_count} vs Yes: {yes_count})"
        else:
            answer = random.choice([0, 1])
            reason = "Random (Equal votes)"

        answer_str = "Yes" if answer == 1 else "No"
        
        max_retries = 1
        for attempt in range(max_retries):
            try:
                response = self.session.post('https://api.duelduck.com/duel/join', json={"answer": answer, "duel_id": duel_id})
                
                if response.status_code == 200:
                    self.log(f"Join Success! | Answer: {answer_str} | {reason}", "SUCCESS")
                    return True
                elif response.status_code == 429:
                    self.log(f"Waiting 10s...", "WARNING")
                    time.sleep(10)
                    return False
                elif response.status_code == 400:
                    return False
                else:
                    return False
            except Exception as e:
                return False
        return False

    def update_wallet(self, wallet_id):
        try:
            response = self.session.put('https://api.duelduck.com/wallets/active', json={"wallet_id": wallet_id})
            if response.status_code == 200:
                data = response.json().get('user', {})
                print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Username: {data.get('username')}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Email: {data.get('email')}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Balance: {data.get('balance')}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Streak: {data.get('daily_reward_streak')}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}XP: {data.get('current_xp')}{Style.RESET_ALL}")
        except:
            pass

    def run(self):
        self.print_banner()
        choice = self.show_menu()
        
        accounts = self.load_file('accounts.txt')
        proxies = self.load_file('proxy.txt')
        api_keys = self.load_file('2captcha.txt')
        
        if not api_keys:
            self.log("2captcha.txt missing", "ERROR")
            return

        use_proxy = True if choice == '1' else False
        if use_proxy:
            self.log(f"Loaded {len(proxies)} proxies", "INFO")
        else:
            self.log("Running without proxy", "INFO")
            
        self.log(f"Loaded {len(accounts)} accounts", "INFO")
        
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        cycle = 1
        while True:
            self.log(f"Cycle #{cycle} Started", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            
            for i, pk in enumerate(accounts):
                self.log(f"Account #{i+1}/{len(accounts)}", "INFO")
                
                if use_proxy and proxies:
                    proxy = proxies[i % len(proxies)]
                    self.session.proxies = {'http': proxy, 'https': proxy}
                    self.log(f"Proxy: {proxy}", "INFO")
                else:
                    self.session.proxies = {}
                    self.log("Proxy: No Proxy", "INFO")

                try:
                    keypair = Keypair.from_base58_string(pk)
                    address = str(keypair.pubkey())
                    censored_wallet = f"{address[:5]}***{address[-5:]}"
                    self.log(f"Wallet: {censored_wallet}", "INFO")
                except:
                    self.log("Invalid Private Key", "ERROR")
                    continue

                captcha_token = self.solve_captcha(api_keys[0], "https://duelduck.com", "0x4AAAAAACI3oP1RfS_PoAfL")
                if not captcha_token:
                    continue

                login_data = self.login(pk, captcha_token)
                if login_data:
                    self.log("Login Successful", "SUCCESS")
                    wallet_id = login_data['user']['active_wallet_id']
                    
                    all_duels = []
                    for page in range(1, 4):
                        duels = self.get_duels(page)
                        if duels:
                            all_duels.extend(duels)
                            time.sleep(2)
                    
                    if all_duels:
                        self.log(f"Total found {len(all_duels)} available duels", "INFO")
                        joined = 0
                        for duel_data in all_duels:
                            if joined >= 10:
                                break
                            if self.join_duel(duel_data):
                                joined += 1
                                delay = random.randint(8, 15)
                                self.log(f"Delay {delay} seconds...", "INFO")
                                time.sleep(delay)
                        
                        self.log(f"Successfully joined {joined} duels", "SUCCESS")
                    else:
                        self.log("No new duels available", "WARNING")
                    
                    self.update_wallet(wallet_id)
                
                if i < len(accounts) - 1:
                    print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                    time.sleep(3)
            
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle} Complete", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle += 1
            self.countdown(86400)

if __name__ == "__main__":
    bot = DuelDuckAutoBot()
    bot.run()
