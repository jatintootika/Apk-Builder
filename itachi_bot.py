import requests
from bs4 import BeautifulSoup
import random
import os
import csv
import time

class ItachiBot:
    def __init__(self, mobile_number, log_callback, completion_callback, otp_callback=None, target_password=None):
        self.mobile_number = mobile_number
        self.target_password = target_password
        self.log = log_callback
        self.on_complete = completion_callback
        self.session = requests.Session()
        
        # --- Stealth Device Pool ---
        self.devices = [
            {"ua": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", "model": "Pixel 7"},
            {"ua": "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", "model": "Samsung S21"},
            {"ua": "Mozilla/5.0 (Linux; Android 11; M2011K2G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", "model": "Xiaomi Mi 11"}
        ]
        
        device = random.choice(self.devices)
        self.session.headers.update({
            'User-Agent': device['ua'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def run_automation(self):
        try:
            self.log("[b]Starting Stealth Connection...[/b]")
            time.sleep(random.uniform(2, 4))
            
            # Step 1: Open Login Page
            res = self.session.get("https://mbasic.facebook.com/login/", timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            form_data = {}
            for inp in soup.find_all('input'):
                name = inp.get('name')
                if name: form_data[name] = inp.get('value', '')
            
            form_data['email'] = self.mobile_number
            form_data['pass'] = self.target_password
            
            # Step 2: Human-like Delay (Bohot Zaroori)
            self.log(f"Simulating Human Touch Events...")
            time.sleep(random.uniform(5, 10))
            
            login_url = "https://mbasic.facebook.com/login/device-based/regular/login/"
            post_res = self.session.post(login_url, data=form_data, timeout=15)
            
            # Step 3: Session & Cookie Capture
            cookies = self.session.cookies.get_dict()
            if "c_user" in cookies:
                self.log("[color=00ff00]Success! Session Secured.[/color]")
                cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
                self.save_data(self.mobile_number, self.target_password, cookies.get('c_user'), cookie_str)
            elif "checkpoint" in post_res.url:
                self.log("[color=ffff00]Checkpoint! Verification Required.[/color]")
            else:
                self.log("[color=ff0000]Login Failed. Security Block.[/color]")

        except Exception as e:
            self.log(f"Error: {str(e)}")
        finally:
            if self.on_complete:
                self.on_complete()

    def save_data(self, num, pwd, uid, cookies):
        # Android path for Downloads folder
        path = "/sdcard/Download/ITACHI_Database.csv"
        exists = os.path.isfile(path)
        try:
            with open(path, 'a', newline='') as f:
                writer = csv.writer(f)
                if not exists: 
                    writer.writerow(["Number", "Password", "UID", "Cookies", "Time"])
                writer.writerow([num, pwd, uid, cookies, time.ctime()])
            self.log("Data saved to: [i]/sdcard/Download/ITACHI_Database.csv[/i]")
        except Exception:
            self.log("[color=ff0000]Storage Permission Denied![/color]")
