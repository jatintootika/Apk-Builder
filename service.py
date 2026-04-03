import requests
from bs4 import BeautifulSoup
import random
import os
import re
import pandas as pd
import pyotp
from PIL import Image, ImageDraw, ImageFont
from jnius import autoclass

# Android Classes
Bundle = autoclass('android.os.Bundle')
AccessibilityNodeInfo = autoclass('android.view.accessibility.AccessibilityNodeInfo')

class FBAutomator:
    def __init__(self):
        self.current_name = ""
        self.current_pwd = ""
        self.excel_path = "/sdcard/Download/FB_Database.xlsx"

    def get_live_name(self):
        try:
            url = "https://www.hopperhq.com/tools/facebook-name-generator/"
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.text, 'html.parser')
            names = [t.text.strip() for t in soup.find_all('span', class_='name-suggestion')]
            return random.choice(names) if names else "Aryan_Smart"
        except: return f"User_{random.randint(100,999)}"

    def create_name_pfp(self, name):
        try:
            img = Image.new('RGB', (500, 500), color=(230, 240, 255))
            d = ImageDraw.Draw(img)
            d.text((150, 220), name, fill=(0,0,0))
            path = "/sdcard/Download/fb_pfp.jpg"
            img.save(path)
            return path
        except: return None

    def log_to_excel(self, name, pwd, url, two_fa_key):
        uid = re.search(r'id=(\d+)', url).group(1) if "id=" in url else "N/A"
        data = {"Name": [name], "Pass": [pwd], "UID": [uid], "2FA": [two_fa_key]}
        df = pd.DataFrame(data)
        if os.path.exists(self.excel_path):
            pd.concat([pd.read_excel(self.excel_path), df]).to_excel(self.excel_path, index=False)
        else: df.to_excel(self.excel_path, index=False)

bot = FBAutomator()

def onAccessibilityEvent(event):
    root = event.getSource()
    if root:
        scan_nodes(root)
        root.recycle()

def scan_nodes(node):
    if not node: return
    # Fill Name & Pass Logic
    if "EditText" in str(node.getClassName()):
        hint = str(node.getHintText()).lower() if node.getHintText() else ""
        if "name" in hint or "first" in hint:
            if not bot.current_name: 
                bot.current_name = bot.get_live_name()
                bot.create_name_pfp(bot.current_name)
            fill(node, bot.current_name)
        elif "password" in hint:
            bot.current_pwd = f"Pass@{random.randint(1000,9999)}"
            fill(node, bot.current_pwd)
    
    for i in range(node.getChildCount()):
        child = node.getChild(i)
        scan_nodes(child)
        if child: child.recycle()

def fill(node, text):
    b = Bundle()
    b.putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, text)
    node.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT, b)
