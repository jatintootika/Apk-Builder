import os
import threading
import sys
import traceback
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import mainthread
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        try:
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
            
            # Application Logo
            if os.path.exists('itachi_logo.png'):
                self.logo = Image(source='itachi_logo.png', size_hint=(1, 0.4), allow_stretch=True, keep_ratio=True)
                self.layout.add_widget(self.logo)
            
            self.title_label = Label(
                text="[b][color=ff0000]ITACHI FB TOOL[/color][/b]", 
                markup=True, 
                font_size='24sp',
                size_hint=(1, 0.1)
            )
            self.layout.add_widget(self.title_label)
            
            # Setup Console
            self.scroll = ScrollView(size_hint=(1, 0.5))
            self.console_label = Label(
                text="[color=ff0000]> System Ready...[/color]",
                markup=True,
                valign='top',
                halign='left',
                size_hint_y=None
            )
            self.console_label.bind(width=lambda *x: self.console_label.setter('text_size')(self.console_label, (self.console_label.width, None)))
            self.console_label.bind(texture_size=self.console_label.setter('size'))
            self.scroll.add_widget(self.console_label)
            self.layout.add_widget(self.scroll)
            
            # Manual Number Input
            self.number_input = TextInput(
                hint_text='Dial Number Manually (eg. 9876543210)',
                multiline=False,
                input_type='number',
                size_hint=(1, 0.1),
                background_color=(0.1, 0.1, 0.1, 1),
                foreground_color=(1, 1, 1, 1)
            )
            self.layout.add_widget(self.number_input)
            
            # OTP Input area (Hidden at start)
            self.otp_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
            self.otp_input = TextInput(
                hint_text='Wait for OTP, then enter here...',
                multiline=False,
                input_type='number',
                size_hint=(0.7, 1),
                background_color=(0.1, 0.1, 0.1, 1),
                foreground_color=(1, 1, 1, 1),
                disabled=True
            )
            self.submit_otp_btn = Button(
                text="Verify (Jutsu)",
                background_color=get_color_from_hex('#228b22'),
                color=(1, 1, 1, 1),
                bold=True,
                size_hint=(0.3, 1),
                disabled=True
            )
            self.submit_otp_btn.bind(on_press=self.submit_otp)
            
            self.otp_layout.add_widget(self.otp_input)
            self.otp_layout.add_widget(self.submit_otp_btn)
            self.layout.add_widget(self.otp_layout)
            
            button_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
            
            # Add Human Mode Button
            self.human_btn = Button(
                text="👤 HUMAN MODE", 
                background_color=get_color_from_hex('#224488'), 
                color=(1, 1, 1, 1),
                bold=True
            )
            self.human_btn.bind(on_press=self.open_human_mode)
            button_layout.add_widget(self.human_btn)
            
            self.start_btn = Button(
                text="🦇 GENJUTSU", 
                background_color=get_color_from_hex('#8b0000'), 
                color=(1, 1, 1, 1),
                bold=True
            )
            self.start_btn.bind(on_press=self.start_bot)
            button_layout.add_widget(self.start_btn)
            
            # Sexy Sliding Setting navigation
            self.settings_btn = Button(
                text="⚙️ SETTINGS",
                background_color=get_color_from_hex('#555555'),
                color=(1,1,1,1),
                bold=True
            )
            self.settings_btn.bind(on_press=self.go_to_settings)
            button_layout.add_widget(self.settings_btn)
            
            self.layout.add_widget(button_layout)
            self.bot = None
            
            # Auto-create PFP directory for the user
            try:
                os.makedirs("/sdcard/Download/Itachi_PFP/", exist_ok=True)
            except:
                pass
                
            self.add_widget(self.layout)
        except Exception as e:
            err = Label(text=f"CRASH ON LOAD: {str(e)}\n\n{traceback.format_exc()}")
            self.add_widget(err)

    def go_to_settings(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'settings'

    @mainthread
    def log_to_console(self, msg):
        self.console_label.text += f"\n[color=a8a8a8]> {msg}[/color]"
        self.scroll.scroll_y = 0

    @mainthread
    def ask_for_otp(self):
        self.otp_input.disabled = False
        self.submit_otp_btn.disabled = False
        self.log_to_console("[color=ffff00]>>> WAITING FOR YOU... Type OTP above and Click Verify![/color]")

    def open_human_mode(self, instance):
        import webbrowser
        self.log_to_console("[color=00ff00]Human Mode Activated -> Opening Chrome![/color]")
        webbrowser.open('https://m.facebook.com/reg')

    def submit_otp(self, instance):
        o_val = self.otp_input.text.strip()
        if not o_val:
            self.log_to_console("[color=ff0000]ERROR: OTP is blank![/color]")
            return
            
        self.submit_otp_btn.disabled = True
        self.otp_input.disabled = True
        
        if self.bot:
            self.bot.otp_code = o_val
            self.bot.otp_event.set()

    def start_bot(self, instance):
        if self.bot and getattr(self.bot, 'is_running', False):
            self.log_to_console("[color=ff0000]Bot is already running![/color]")
            return
            
        self.start_btn.disabled = True
        
        mobile_number = self.number_input.text.strip()
        if not mobile_number:
            self.start_btn.disabled = False
            self.log_to_console("[color=ff0000]ERROR: Mobile Number is Empty![/color]")
            return
            
        self.log_to_console("[color=ff0000]>>> INITIATING TSUKUYOMI FLOW...[/color]")
        
        try:
            from itachi_bot import ItachiBot
            self.bot = ItachiBot(
                mobile_number=mobile_number, 
                log_callback=self.log_to_console, 
                completion_callback=self.bot_finished,
                otp_callback=self.ask_for_otp,
                target_password=self.manager.master_password # Passed from ScreenManager state
            )
            # Make sure old texts are wiped
            self.otp_input.text = "" 
            threading.Thread(target=self.bot.run_automation, daemon=True).start()
        except Exception as e:
            err_msg = traceback.format_exc()
            self.log_to_console(f"[color=ff0000]LOAD ERROR: {str(e)}[/color]")
            self.log_to_console(f"[color=ff0000]TRACE: {err_msg}[/color]")
            self.start_btn.disabled = False

    @mainthread
    def bot_finished(self):
        self.start_btn.disabled = False
        self.log_to_console("[color=00ff00]>>> CYCLE COMPLETE![/color]")


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title_label = Label(
            text="[b][color=aaaaaa]⚙️ CONFIGURATOR[/color][/b]", 
            markup=True, font_size='24sp', size_hint=(1, 0.1)
        )
        layout.add_widget(title_label)
        
        # Master Password Config
        layout.add_widget(Label(text="[b]Enforce Master Password[/b]", markup=True, size_hint=(1, 0.05)))
        self.pw_input = TextInput(
            hint_text='Type Target Password (eg. Naruto@123)',
            multiline=False, size_hint=(1, 0.1),
            background_color=(0.1, 0.1, 0.1, 1), foreground_color=(1, 1, 1, 1)
        )
        layout.add_widget(self.pw_input)
        
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        set_pw_btn = Button(text="Lock Password", background_color=get_color_from_hex('#228b22'), bold=True)
        set_pw_btn.bind(on_press=self.set_password)
        btn_layout.add_widget(set_pw_btn)
        
        reset_pw_btn = Button(text="Reset (Random)", background_color=get_color_from_hex('#8b0000'), bold=True)
        reset_pw_btn.bind(on_press=self.reset_password)
        btn_layout.add_widget(reset_pw_btn)
        
        layout.add_widget(btn_layout)
        
        self.status_label = Label(text="Current: [color=00ffff]Random Generation[/color]", markup=True, size_hint=(1, 0.05))
        layout.add_widget(self.status_label)
        
        # Profile Picture Area
        pfp_label = Label(text="[b]PFP Folder Location (Auto Created):[/b]\n[color=00ff00]/sdcard/Download/Itachi_PFP/[/color]", markup=True, size_hint=(1, 0.1), halign='center')
        layout.add_widget(pfp_label)
        
        # View Excel Database Button
        view_db_btn = Button(text="📊 VIEW EXCEL (CSV) DATABASE", background_color=get_color_from_hex('#224488'), bold=True, size_hint=(1, 0.1))
        view_db_btn.bind(on_press=self.view_database)
        layout.add_widget(view_db_btn)
        
        # Spacer
        layout.add_widget(Label(size_hint=(1, 0.1)))
        
        # Back Button
        back_btn = Button(text="⬅ BACK TO TERMINAL", size_hint=(1, 0.1), background_color=get_color_from_hex('#555555'))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)

    def set_password(self, instance):
        input_pw = self.pw_input.text.strip()
        if input_pw:
            self.manager.master_password = input_pw
            self.status_label.text = f"Current: [color=00ff00]Locked ({input_pw})[/color]"
            
    def reset_password(self, instance):
        self.manager.master_password = None
        self.pw_input.text = ""
        self.status_label.text = "Current: [color=00ffff]Random Generation[/color]"

    def view_database(self, instance):
        path = "/sdcard/Download/ITACHI_Database.csv"
        if not os.path.exists(path):
            path = "ITACHI_Database.csv" # Desktop Fallback
            
        file_content = "File not found or empty."
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
            except Exception as e:
                file_content = f"Error reading file: {e}"
                
        # Show in a scrollable popup
        scroll = ScrollView(size_hint=(1, 1))
        lbl = Label(text=file_content, size_hint_y=None, markup=True, halign='left', valign='top')
        lbl.bind(width=lambda *x: lbl.setter('text_size')(lbl, (lbl.width, None)))
        lbl.bind(texture_size=lbl.setter('size'))
        scroll.add_widget(lbl)
        
        popup = Popup(title="ITACHI Excel (CSV) View", content=scroll, size_hint=(0.9, 0.9))
        popup.open()

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main'

class ItachiConsoleApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#111111')
        
        # Setup Slide Manager
        sm = ScreenManager(transition=SlideTransition())
        sm.master_password = None # Global state for the bot
        
        # Add our sexy pages
        main_screen = MainScreen(name='main')
        settings_screen = SettingsScreen(name='settings')
        
        sm.add_widget(main_screen)
        sm.add_widget(settings_screen)
        
        return sm

if __name__ == '__main__':
    try:
        ItachiConsoleApp().run()
    except Exception as e:
        pass