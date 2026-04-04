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
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.behaviors import ButtonBehavior

# --- SEXY AESTHETIC CLASSES --- #
class RoundedButton(ButtonBehavior, Label):
    def __init__(self, bg_color_hex='#1e3a8a', **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.base_color = get_color_from_hex(bg_color_hex)
        self.color = (1, 1, 1, 1) # Text color
        self.bold = True
        
        with self.canvas.before:
            self.bg_color_prop = Color(rgba=self.base_color)
            # Add a sexy 15px radius for smooth curves (Apple/Premium style)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
            
        self.bind(pos=self.update_rect, size=self.update_rect)
        
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
    def on_press(self):
        # Click effect
        self.bg_color_prop.rgba = (self.base_color[0]*0.7, self.base_color[1]*0.7, self.base_color[2]*0.7, 1)
        
    def on_release(self):
        # Restore color
        self.bg_color_prop.rgba = self.base_color


class RoundedInputWrapper(BoxLayout):
    def __init__(self, hint='', cc=False, **kwargs):
        super(RoundedInputWrapper, self).__init__(**kwargs)
        self.padding = [2, 2, 2, 2] # Border thickness
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#334155')) # Border Color
            self.rect1 = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        with self.canvas:
            Color(rgba=get_color_from_hex('#1e293b')) # Internal Dark Box
            self.rect2 = RoundedRectangle(pos=(self.x+2, self.y+2), size=(self.width-4, self.height-4), radius=[9])
            
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Real text input goes inside transparently
        self.input_field = TextInput(
            hint_text=hint,
            multiline=False,
            background_color=(0,0,0,0), # Total transparent
            foreground_color=get_color_from_hex('#ffffff'),
            cursor_color=get_color_from_hex('#f43f5e'),
            halign='center' if cc else 'left',
            padding_y=[12, 0] # Centers text vertically roughly
        )
        if not cc:
            self.input_field.input_type = 'number'
        self.add_widget(self.input_field)

    def update_rect(self, *args):
        self.rect1.pos = self.pos
        self.rect1.size = self.size
        self.rect2.pos = (self.x+2, self.y+2)
        self.rect2.size = (self.width-4, self.height-4)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        try:
            self.layout = BoxLayout(orientation='vertical', padding=[30, 40, 30, 20], spacing=25)
            
            # Premium Cyberpunk Title
            self.title_label = Label(
                text="[b][color=f43f5e][size=34sp]ITACHI[/size][/color][/b] [size=22sp][color=cbd5e1]PRO[/color][/size]\n[color=64748b][size=12sp]A U T O M A T I O N   E N G I N E[/size][/color]", 
                markup=True, 
                halign='center',
                size_hint=(1, 0.15)
            )
            self.layout.add_widget(self.title_label)
            
            # Pure Black Cyber Console Box
            console_wrapper = BoxLayout(padding=[2,2,2,2], size_hint=(1, 0.45))
            with console_wrapper.canvas.before:
                Color(rgba=get_color_from_hex('#1e293b')) # Subtle Slate border
                self.cw_rect1 = RoundedRectangle(pos=console_wrapper.pos, size=console_wrapper.size, radius=[12])
            with console_wrapper.canvas:
                Color(rgba=get_color_from_hex('#000000')) # Pure Jet Black console
                self.cw_rect2 = RoundedRectangle(pos=(console_wrapper.x+1, console_wrapper.y+1), size=(console_wrapper.width-2, console_wrapper.height-2), radius=[11])
            console_wrapper.bind(pos=lambda obj,pos: self.update_console_bg(obj), size=lambda obj,size: self.update_console_bg(obj))
                
            self.scroll = ScrollView()
            self.console_label = Label(
                text="[color=10b981]> System Boot Sequence Initiated...[/color]\n[color=10b981]> Waiting for Target Protocol...[/color]",
                markup=True,
                valign='top',
                halign='left',
                size_hint_y=None,
                padding=(15, 15)
            )
            self.console_label.bind(width=lambda *x: self.console_label.setter('text_size')(self.console_label, (self.console_label.width, None)))
            self.console_label.bind(texture_size=self.console_label.setter('size'))
            
            self.scroll.add_widget(self.console_label)
            console_wrapper.add_widget(self.scroll)
            self.layout.add_widget(console_wrapper)
            
            # Sleek Dual Number Layout
            self.phone_layout = BoxLayout(size_hint=(1, 0.1), spacing=15)
            
            self.country_wrapper = RoundedInputWrapper(hint='+91', cc=True)
            self.country_wrapper.size_hint = (0.3, 1)
            self.country_wrapper.input_field.text = '+91'
            
            self.number_wrapper = RoundedInputWrapper(hint='Dial Target Mobile...')
            self.number_wrapper.size_hint = (0.7, 1)
            
            self.phone_layout.add_widget(self.country_wrapper)
            self.phone_layout.add_widget(self.number_wrapper)
            self.layout.add_widget(self.phone_layout)
            
            # OTP Verify Flow (Hidden)
            self.otp_layout = BoxLayout(size_hint=(1, 0.1), spacing=15)
            self.otp_wrapper = RoundedInputWrapper(hint='Enter Secure OTP')
            self.otp_wrapper.size_hint = (0.6, 1)
            self.otp_wrapper.input_field.disabled = True
            
            self.submit_otp_btn = RoundedButton(bg_color_hex='#0f766e', text="VERIFY CODE")
            self.submit_otp_btn.size_hint = (0.4, 1)
            self.submit_otp_btn.disabled = True
            self.submit_otp_btn.bind(on_press=self.submit_otp)
            
            self.otp_layout.add_widget(self.otp_wrapper)
            self.otp_layout.add_widget(self.submit_otp_btn)
            self.layout.add_widget(self.otp_layout)
            
            # Bottom Action Menu (Modern Spacing)
            button_layout = BoxLayout(size_hint=(1, 0.12), spacing=15)
            
            self.human_btn = RoundedButton(bg_color_hex='#334155', text="👤 BROWSER")
            self.human_btn.bind(on_press=self.open_human_mode)
            button_layout.add_widget(self.human_btn)
            
            self.start_btn = RoundedButton(bg_color_hex='#dc2626', text="🦇 GENJUTSU") # Cyber Red
            self.start_btn.bind(on_press=self.start_bot)
            button_layout.add_widget(self.start_btn)
            
            self.settings_btn = RoundedButton(bg_color_hex='#0f172a', text="⚙️ CONFIG")
            self.settings_btn.bind(on_press=self.go_to_settings)
            button_layout.add_widget(self.settings_btn)
            
            self.layout.add_widget(button_layout)
            self.bot = None
            
            try:
                os.makedirs("/sdcard/Download/Itachi_PFP/", exist_ok=True)
            except:
                pass
                
            self.add_widget(self.layout)
            
        except Exception as e:
            err_msg = f"CRASH ON LOAD: {str(e)}\n\n{traceback.format_exc()}"
            print("CRASH TRACE:", err_msg)
            err = Label(text=err_msg)
            self.add_widget(err)

    def update_console_bg(self, obj):
        self.cw_rect1.pos = obj.pos
        self.cw_rect1.size = obj.size
        self.cw_rect2.pos = (obj.x+1, obj.y+1)
        self.cw_rect2.size = (obj.width-2, obj.height-2)

    def go_to_settings(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'settings'

    @mainthread
    def log_to_console(self, msg):
        self.console_label.text += f"\n[color=94a3b8]> {msg}[/color]"
        self.scroll.scroll_y = 0

    @mainthread
    def ask_for_otp(self):
        self.otp_wrapper.input_field.disabled = False
        self.submit_otp_btn.disabled = False
        self.log_to_console("[color=eab308][!] WAITING FOR ACTION: Type intercepted OTP above.[/color]")

    def open_human_mode(self, instance):
        import webbrowser
        self.log_to_console("[color=10b981]> Manual Bridge Created -> Web Link Opened![/color]")
        webbrowser.open('https://m.facebook.com/reg')

    def submit_otp(self, instance):
        o_val = self.otp_wrapper.input_field.text.strip()
        if not o_val:
            self.log_to_console("[color=f43f5e][X] ERROR: OTP Code Missing![/color]")
            return
            
        self.submit_otp_btn.disabled = True
        self.otp_wrapper.input_field.disabled = True
        
        if self.bot:
            self.bot.otp_code = o_val
            self.bot.otp_event.set()

    def start_bot(self, instance):
        if self.bot and getattr(self.bot, 'is_running', False):
            self.log_to_console("[color=f43f5e][X] Override: Engine is already engaged![/color]")
            return
            
        self.start_btn.disabled = True
        
        c_code = self.country_wrapper.input_field.text.strip()
        m_num = self.number_wrapper.input_field.text.strip()
        mobile_number = c_code + m_num
        
        if not m_num:
            self.start_btn.disabled = False
            self.log_to_console("[color=f43f5e][X] ERROR: No Target Phone Specified.[/color]")
            return
            
        self.log_to_console("[color=f43f5e]>>> INITIATING SILENT TSUKUYOMI PROTOCOL...[/color]")
        
        try:
            from itachi_bot import ItachiBot
            self.bot = ItachiBot(
                mobile_number=mobile_number, 
                log_callback=self.log_to_console, 
                completion_callback=self.bot_finished,
                otp_callback=self.ask_for_otp,
                target_password=self.manager.master_password # Passed from ScreenManager state
            )
            self.otp_wrapper.input_field.text = "" 
            threading.Thread(target=self.bot.run_automation, daemon=True).start()
        except Exception as e:
            err_msg = traceback.format_exc()
            self.log_to_console(f"[color=f43f5e]LOAD ERROR: {str(e)}[/color]")
            self.log_to_console(f"[color=f43f5e]TRACE: {err_msg}[/color]")
            self.start_btn.disabled = False

    @mainthread
    def bot_finished(self):
        self.start_btn.disabled = False
        self.log_to_console("[color=4ade80]>>> EXTRACTION COMPLETE & DATABASE WRITTEN![/color]")


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[30, 40, 30, 20], spacing=25)
        
        # Title
        title_label = Label(
            text="[b][color=94a3b8]⚙️ CONFIGURATOR INTERFACE[/color][/b]", 
            markup=True, font_size='20sp', size_hint=(1, 0.1)
        )
        layout.add_widget(title_label)
        
        # Master Password Config
        layout.add_widget(Label(text="[b][color=e2e8f0]Force Global Target Password[/color][/b]", markup=True, size_hint=(1, 0.05)))
        self.pw_wrapper = RoundedInputWrapper(hint='e.g. Naruto@123')
        self.pw_wrapper.size_hint = (1, 0.1)
        layout.add_widget(self.pw_wrapper)
        
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=15)
        
        set_pw_btn = RoundedButton(bg_color_hex='#0f766e', text="LOCK ENGINE")
        set_pw_btn.bind(on_press=self.set_password)
        btn_layout.add_widget(set_pw_btn)
        
        reset_pw_btn = RoundedButton(bg_color_hex='#991b1b', text="RESET RANDOM")
        reset_pw_btn.bind(on_press=self.reset_password)
        btn_layout.add_widget(reset_pw_btn)
        
        layout.add_widget(btn_layout)
        
        self.status_label = Label(text="State: [color=38bdf8]Random Generation Algorithm Active[/color]", markup=True, size_hint=(1, 0.05))
        layout.add_widget(self.status_label)
        
        # Profile Picture Area
        pfp_label = Label(text="[color=94a3b8]Directory Target (Image Uploads):[/color]\n[color=4ade80]/sdcard/Download/Itachi_PFP/[/color]", markup=True, size_hint=(1, 0.1), halign='center')
        layout.add_widget(pfp_label)
        
        # View Excel Database Button
        view_db_btn = RoundedButton(bg_color_hex='#334155', text="📊 OPEN CSV REPOSITORY")
        view_db_btn.size_hint = (1, 0.1)
        view_db_btn.bind(on_press=self.view_database)
        layout.add_widget(view_db_btn)
        
        # Spacer
        layout.add_widget(Label(size_hint=(1, 0.1)))
        
        # Back Button
        back_btn = RoundedButton(bg_color_hex='#0f172a', text="⬅ RETURN TO COMMAND LINE")
        back_btn.size_hint = (1, 0.1)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)

    def set_password(self, instance):
        input_pw = self.pw_wrapper.input_field.text.strip()
        if input_pw:
            self.manager.master_password = input_pw
            self.status_label.text = f"State: [color=10b981]Locked Global [{input_pw}][/color]"
            
    def reset_password(self, instance):
        self.manager.master_password = None
        self.pw_wrapper.input_field.text = ""
        self.status_label.text = "State: [color=38bdf8]Random Generation Algorithm Active[/color]"

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
                
        scroll = ScrollView(size_hint=(1, 1))
        lbl = Label(text=file_content, size_hint_y=None, markup=True, halign='left', valign='top')
        lbl.bind(width=lambda *x: lbl.setter('text_size')(lbl, (lbl.width, None)))
        lbl.bind(texture_size=lbl.setter('size'))
        scroll.add_widget(lbl)
        
        popup = Popup(title="ITACHI CSV DATA TARGET", content=scroll, size_hint=(0.9, 0.9))
        popup.open()

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main'

class ItachiConsoleApp(App):
    def build(self):
        # Ultra Premium Night Mode Background
        Window.clearcolor = get_color_from_hex('#0b0f19') 
        # Fix Keyboard Hiding Inputs
        Window.softinput_mode = "below_target"
        
        sm = ScreenManager(transition=SlideTransition())
        sm.master_password = None
        
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