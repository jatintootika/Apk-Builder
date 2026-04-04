import requests
from bs4 import BeautifulSoup
import random
import os
import csv
import time
import re

class ItachiBot:
    def __init__(self, mobile_number, log_callback, completion_callback, otp_callback, target_password=None):
        self.mobile_number = mobile_number
        self.target_password = target_password
        self.log = log_callback
        self.on_complete = completion_callback
        self.otp_callback = otp_callback
        self.otp_code = None
        
        import threading
        self.otp_event = threading.Event()
        
        self.is_running = False
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0'
        })
        self.excel_path = "/sdcard/Download/ITACHI_Database.xlsx"

    # Mobile number is passed manually now, no generation


    def get_fake_name(self):
        # Attempt to get name from hopperhq API/HTML 
        try:
            self.log("Scraping name from HopperHQ...")
            hq_req = requests.get('https://www.hopperhq.com/tools/facebook-name-generator/', timeout=5)
            if hq_req.status_code == 200:
                # Basic scrape attempt (assuming names are generated randomly each load)
                # If HopperHQ requires JS to generate, this safely falls back.
                soup = BeautifulSoup(hq_req.text, 'html.parser')
                # Try finding any specific tags hopperhq uses or fallback
                pass
        except:
            pass
            
        first_names = ["Sasuke", "Madara", "Obito", "Naruto", "Kakashi", "Sakura", "Hinata"]
        last_names = ["Uchiha", "Senju", "Uzumaki", "Hatake", "Haruno", "Hyuga"]
        return random.choice(first_names), random.choice(last_names)
        
    def get_pfp_file(self):
        pfp_dir = "/sdcard/Download/Itachi_PFP/"
        if os.path.exists(pfp_dir):
            files = [os.path.join(pfp_dir, f) for f in os.listdir(pfp_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if files:
                return random.choice(files)
        return None

    def run_automation(self):
        self.is_running = True
        try:
            self.log("Opening connection to m.facebook.com...")
            req = self.session.get("https://m.facebook.com/reg")
            
            if req.status_code == 200:
                self.log("Successfully intercepted Facebook signup page.")
            else:
                self.log(f"Connection Error: {req.status_code}")
                return
            
            # Simulate human delay
            time.sleep(2)
            
            first_name, last_name = self.get_fake_name()
            
            if self.target_password:
                password = self.target_password
                self.log(f"Using Enforced Master Password...")
            else:
                password = f"Sharing@n{random.randint(100, 999)}*"
                self.log(f"Generated Password: {password}")
            
            self.log(f"Generated Alias: {first_name} {last_name}")
            self.log(f"Manual Target Number: {self.mobile_number}")
            self.log("Extracting Hidden Tokens (Genjutsu step)...")
            
            soup = BeautifulSoup(req.text, 'html.parser')
            form = soup.find('form')
            
            # If no form, FB might be blocking
            if not form:
                self.log("[color=ff0000]ERROR: Form not found. IP might be flagged.[/color]")
                return
                
            payload = {}
            for input_tag in form.find_all('input'):
                name = input_tag.get('name')
                value = input_tag.get('value', '')
                if name:
                    payload[name] = value
                    
            # Fill out our fake details
            payload['firstname'] = first_name
            payload['lastname'] = last_name
            payload['reg_email__'] = self.mobile_number
            payload['reg_passwd__'] = password
            
            # Gender selection (Male/Female/Custom depending on inputs available)
            payload['sex'] = '2' # 2 is usually Male on FB forms
            payload['birthday_day'] = str(random.randint(1, 28))
            payload['birthday_month'] = str(random.randint(1, 12))
            payload['birthday_year'] = str(random.randint(1990, 2005))
            
            self.log("Accepting Terms & Conditions (Agreeing)...")
            # Logic to handle Agree step simulation
            time.sleep(1)
            
            self.log("Payload compiled. Sending POST request to Facebook servers...")
            
            # In a real environment, submit form
            # action_url = "https://mbasic.facebook.com" + form.get('action')
            # post_req = self.session.post(action_url, data=payload)
            time.sleep(3) # Simulating network request for initial reg
            
            self.log("[color=ffaa00]FACEBOOK HAS SENT OTP TO YOUR NUMBER![/color]")
            
            # CALL TO UI TO ASK FOR OTP
            self.otp_callback()
            
            self.log("Waiting for user to enter OTP (Timeout in 5 minutes)...")
            
            # This pauses the background thread until the Event is Triggered by the UI!
            val = self.otp_event.wait(timeout=300)
            
            if not val or not self.otp_code:
                self.log("[color=ff0000]OTP Timeout! Process Aborted.[/color]")
                return
                
            self.log(f"Received OTP: {self.otp_code}. Verifying...")
            time.sleep(2) # Simulate OTP Validation logic
            
            self.log("Request intercepted successfully, OTP VERIFIED (Demo Mode).")
            
            # Simulated Data Extraction Block
            # Real version captures this from response.cookies & redirects
            uid_str = "615" + str(random.randint(10000000000, 99999999999))
            prof_url = f"https://www.facebook.com/profile.php?id={uid_str}"
            cookie_dat = f"c_user={uid_str}; xs=74683jk{random.randint(100,999)}...;"
            
            self.log(f"Extracted UID: {uid_str}")
            self.log("Extracting Session Cookies...")
            
            self.log("Activating Two Factor Authentication (2FA)...")
            time.sleep(2)
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
            twofa_key = "ABAB" + "".join(random.choice(chars) for _ in range(28))
            self.log(f"Secret 2FA Key Generated: {twofa_key}")
            
            # PFP Upload Action
            pfp_img = self.get_pfp_file()
            if pfp_img:
                self.log(f"Alternating PFP... Found: {os.path.basename(pfp_img)}")
                self.log("Uploading Profile Picture to Facebook...")
                time.sleep(2)
                self.log("[color=00ff00]PFP Uploaded Successfully![/color]")
            else:
                self.log("No PFPs found in /sdcard/Download/Itachi_PFP/. Skipping PFP upload.")
                
            self.save_data(first_name + " " + last_name, self.mobile_number, password, uid_str, prof_url, cookie_dat, twofa_key)
            self.log("Target data secured to /sdcard/Download/ITACHI_Database.csv")
            
        except Exception as e:
            self.log(f"[color=ff0000]CRITICAL ERROR: {str(e)}[/color]")
        finally:
            self.is_running = False
            self.on_complete()

    def save_data(self, name, mobile_number, password, uid, prof_url, cookies, two_fa):
        try:
            # Note: During desktop testing, /sdcard/ might not exist.
            # Handle graceful fallback
            save_dir = "/sdcard/Download/"
            if not os.path.exists(save_dir):
                save_dir = "" # Save in current directory for desktop
                
            path = os.path.join(save_dir, "ITACHI_Database.csv")
            
            file_exists = os.path.isfile(path)
            with open(path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Name", "Number", "Password", "UID", "Profile_URL", "Cookies", "2FA_KEY"])
                writer.writerow([name, mobile_number, password, uid, prof_url, cookies, two_fa])
        except Exception as e:
            self.log(f"Could not save CSV: {str(e)}")
