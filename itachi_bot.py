import requests
from bs4 import BeautifulSoup
import random
import time
import os
import csv

class ItachiBot:
    def __init__(self, log_callback):
        self.log = log_callback
        self.session = requests.Session()
        self.phone = ""
        self.password = ""
        # Random Devices (Samsung, Pixel, Redmi, Vivo)
        self.ua_list = [
            'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 11; vivo V2031) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 10; Redmi Note 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36'
        ]

    def step_1_fill_form(self, phone):
        try:
            self.phone = phone
            # Har request pe naya Agent
            self.session.headers.update({'User-Agent': random.choice(self.ua_list)})
            
            self.log(f"Starting Stealth Reg for {phone}...")
            
            # Step 1: Base Cookies lena zaroori hai
            self.session.get("https://mbasic.facebook.com/", timeout=15)
            time.sleep(2)
            
            # Step 2: Registration Page
            res = self.session.get("https://mbasic.facebook.com/reg/", timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            form = soup.find('form')
            if not form:
                self.log("[color=ff0000]Security Block! Use Airplane Mode Trick.[/color]")
                return False
                
            action = "https://mbasic.facebook.com" + form['action']
            payload = {n.get('name'): n.get('value', '') for n in form.find_all('input') if n.get('name')}
            
            f_name = random.choice(["Arjun", "Kabir", "Aryan", "Sufi", "Zoro", "Rohan"])
            l_name = random.choice(["Uchiha", "Sharma", "Singh", "Khan", "Malhotra", "Verma"])
            self.password = "Itachi@" + str(random.randint(1000, 9999))
            
            payload.update({
                'firstname': f_name, 'lastname': l_name, 'reg_email__': phone,
                'sex': '2', 'birthday_day': str(random.randint(1,28)),
                'birthday_month': str(random.randint(1,12)),
                'birthday_year': str(random.randint(1995, 2004)),
                'reg_passwd__': self.password
            })
            
            self.log("Wait... Simulating Human Behavior...")
            time.sleep(random.uniform(5, 9)) # Zyada delay = Less Block
            
            self.session.post(action, data=payload, timeout=15)
            self.log("[color=ffff00]Request Sent! Enter OTP if received.[/color]")
            return True
        except Exception as e:
            self.log(f"Error: {str(e)[:30]}")
            return False

    def step_2_confirm_otp(self, otp):
        self.save_account(otp)
        self.log("[color=00ff00]Account Data Saved![/color]")

    def save_account(self, otp):
        path = "/sdcard/Download/ITACHI_Accounts.csv"
        exists = os.path.isfile(path)
        try:
            with open(path, 'a', newline='') as f:
                writer = csv.writer(f)
                if not exists: writer.writerow(["Phone", "Pass", "OTP", "Time"])
                writer.writerow([self.phone, self.password, otp, time.ctime()])
        except:
            self.log("Storage Error: Give Permission in Settings!")
