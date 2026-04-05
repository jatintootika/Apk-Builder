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
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'
        })

    def step_1_fill_form(self, phone):
        try:
            self.phone = phone
            self.log(f"Starting for {phone}...")
            res = self.session.get("https://mbasic.facebook.com/reg/", timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            form = soup.find('form')
            if not form:
                self.log("[color=ff0000]FB Blocked this Request.[/color]")
                return
                
            action = "https://mbasic.facebook.com" + form['action']
            payload = {n.get('name'): n.get('value', '') for n in form.find_all('input') if n.get('name')}
            
            self.password = "Itachi@" + str(random.randint(1000, 9999))
            payload.update({
                'firstname': 'User', 'lastname': str(random.randint(10,99)),
                'reg_email__': phone, 'sex': '2',
                'birthday_day': '10', 'birthday_month': '5', 'birthday_year': '1998',
                'reg_passwd__': self.password
            })
            
            self.session.post(action, data=payload, timeout=15)
            self.log("[color=ffff00]Step 1 Done! Check SMS for OTP.[/color]")
        except Exception as e:
            self.log(f"Error: {str(e)[:50]}")

    def step_2_confirm_otp(self, otp):
        try:
            # Sirf data save karne ki koshish karega
            self.save_account(otp)
        except Exception as e:
            self.log(f"Save Error: {str(e)}")

    def save_account(self, otp):
        # Crash se bachne ke liye path check
        path = "/sdcard/Download/ITACHI_Accounts.csv"
        try:
            file_exists = os.path.isfile(path)
            with open(path, 'a', newline='') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Phone", "Pass", "OTP", "Date"])
                writer.writerow([self.phone, self.password, otp, time.ctime()])
            self.log("[color=00ff00]Saved in Downloads![/color]")
        except Exception as e:
            self.log("[color=ff0000]Permission Denied! Enable Storage in Settings.[/color]")
