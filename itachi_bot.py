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
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        })

    def step_1_fill_form(self, phone):
        try:
            self.phone = phone
            self.log(f"Opening FB Reg for {phone}...")
            res = self.session.get("https://mbasic.facebook.com/reg/")
            soup = BeautifulSoup(res.text, 'html.parser')
            
            form = soup.find('form')
            if not form:
                self.log("[color=ff0000]Security Block! Change Internet/IP.[/color]")
                return False
                
            action = "https://mbasic.facebook.com" + form['action']
            
            # Random Identity Logic
            f_name = random.choice(["Arjun", "Zoro", "Kabir", "Itachi", "Sufi", "Aryan", "Vikram"])
            l_name = random.choice(["Uchiha", "Sharma", "Singh", "Khan", "Malhotra", "Verma"])
            self.password = "Itachi@" + str(random.randint(1000, 9999))
            
            payload = {n.get('name'): n.get('value', '') for n in form.find_all('input') if n.get('name')}
            payload.update({
                'firstname': f_name,
                'lastname': l_name,
                'reg_email__': phone,
                'sex': '2', # Male
                'birthday_day': str(random.randint(1, 28)),
                'birthday_month': str(random.randint(1, 12)),
                'birthday_year': str(random.randint(1992, 2004)),
                'reg_passwd__': self.password
            })
            
            self.log(f"Filling: {f_name} {l_name}...")
            time.sleep(random.uniform(2, 4)) # Simulation delay
            
            self.session.post(action, data=payload)
            self.log("[color=ffff00]Step 1 Done! Check your phone for OTP.[/color]")
            return True
        except Exception as e:
            self.log(f"Error: {str(e)}")
            return False

    def step_2_confirm_otp(self, otp):
        try:
            self.log(f"Submitting OTP: {otp}...")
            # Yahan hum data save kar rahe hain kyunki OTP aap manually daal rahe ho
            self.save_account(otp)
            self.log("[color=00ff00]Account Created & Details Saved![/color]")
        except Exception as e:
            self.log(f"OTP Error: {str(e)}")

    def save_account(self, otp):
        path = "/sdcard/Download/ITACHI_Accounts.csv"
        exists = os.path.isfile(path)
        try:
            with open(path, 'a', newline='') as f:
                writer = csv.writer(f)
                if not exists: 
                    writer.writerow(["Number", "Password", "OTP", "Time"])
                writer.writerow([self.phone, self.password, otp, time.ctime()])
            self.log(f"Saved to: Downloads/ITACHI_Accounts.csv")
        except:
            self.log("Storage Error: Give Permission in App Settings!")
