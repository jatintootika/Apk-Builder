import requests
from bs4 import BeautifulSoup
import random
import os
import csv
import time
import re

class ItachiBot:
    def __init__(self, log_callback, completion_callback):
        self.log = log_callback
        self.on_complete = completion_callback
        self.is_running = False
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Galaxy S23) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36'
        })
        self.excel_path = "/sdcard/Download/ITACHI_Database.xlsx"

    def get_fake_email(self):
        try:
            domain = random.choice(["1secmail.com", "1secmail.org", "1secmail.net"])
            user = f"itachi_{random.randint(10000, 99999)}_{int(time.time())}"
            return f"{user}@{domain}"
        except:
            return f"itachi_{random.randint(1000,9999)}@example.com"

    def get_fake_name(self):
        first_names = ["Sasuke", "Madara", "Obito", "Naruto", "Kakashi", "Sakura", "Hinata"]
        last_names = ["Uchiha", "Senju", "Uzumaki", "Hatake", "Haruno", "Hyuga"]
        return random.choice(first_names), random.choice(last_names)

    def run_automation(self):
        self.is_running = True
        try:
            self.log("Opening connection to mbasic.facebook.com...")
            req = self.session.get("https://mbasic.facebook.com/reg")
            
            if req.status_code == 200:
                self.log("Successfully intercepted Facebook signup page.")
            else:
                self.log(f"Connection Error: {req.status_code}")
                return
            
            # Simulate human delay
            time.sleep(2)
            
            first_name, last_name = self.get_fake_name()
            email = self.get_fake_email()
            password = f"Sharing@n{random.randint(100, 999)}*"
            
            self.log(f"Generated Alias: {first_name} {last_name}")
            self.log(f"Generated Email: {email}")
            self.log(f"Generated Password: {password}")
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
            payload['reg_email__'] = email
            payload['reg_passwd__'] = password
            
            # Gender selection (Male/Female/Custom depending on inputs available)
            payload['sex'] = '2' # 2 is usually Male on FB forms
            payload['birthday_day'] = str(random.randint(1, 28))
            payload['birthday_month'] = str(random.randint(1, 12))
            payload['birthday_year'] = str(random.randint(1990, 2005))
            
            self.log("Payload compiled. Sending POST request to Facebook servers...")
            
            # In a real environment, submit form
            # action_url = "https://mbasic.facebook.com" + form.get('action')
            # post_req = self.session.post(action_url, data=payload)
            time.sleep(3) # Simulating network request
            
            self.log("Request intercepted successfully (Demo/Test Mode).")
            self.save_data(first_name + " " + last_name, email, password)
            self.log("Target data secured to /sdcard/Download/ITACHI_Database.csv")
            
        except Exception as e:
            self.log(f"[color=ff0000]CRITICAL ERROR: {str(e)}[/color]")
        finally:
            self.is_running = False
            self.on_complete()

    def save_data(self, name, email, password):
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
                    writer.writerow(["Name", "Email", "Password"])
                writer.writerow([name, email, password])
        except Exception as e:
            self.log(f"Could not save CSV: {str(e)}")
