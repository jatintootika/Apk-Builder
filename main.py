import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import mainthread
from kivy.utils import get_color_from_hex

# Import the new bot logic
from itachi_bot import ItachiBot

class ItachiConsoleApp(App):
    def build(self):
        # Apply Itachi Theme Window Color (Dark Grey/Black)
        Window.clearcolor = get_color_from_hex('#111111')
        
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Logo Image
        if os.path.exists('itachi_logo.png'):
            self.logo = Image(source='itachi_logo.png', size_hint=(1, 0.4), allow_stretch=True, keep_ratio=True)
            self.layout.add_widget(self.logo)
        
        # Title Label
        self.title_label = Label(
            text="[b][color=ff0000]ITACHI FB TOOL[/color][/b]", 
            markup=True, 
            font_size='24sp',
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.title_label)
        
        # Console Area
        self.scroll = ScrollView(size_hint=(1, 0.5))
        self.console_label = Label(
            text="[color=ff0000]> Waiting for command...[/color]",
            markup=True,
            valign='top',
            halign='left',
            size_hint_y=None
        )
        self.console_label.bind(width=lambda *x: self.console_label.setter('text_size')(self.console_label, (self.console_label.width, None)))
        self.console_label.bind(texture_size=self.console_label.setter('size'))
        self.scroll.add_widget(self.console_label)
        self.layout.add_widget(self.scroll)
        
        # Action Buttons
        button_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        self.start_btn = Button(
            text="Genjutsu Start (Run Bot)", 
            background_color=get_color_from_hex('#8b0000'), 
            color=(1, 1, 1, 1),
            bold=True
        )
        self.start_btn.bind(on_press=self.start_bot)
        button_layout.add_widget(self.start_btn)
        
        self.layout.add_widget(button_layout)
        
        # Bot instance
        self.bot = None
        
        return self.layout

    @mainthread
    def log_to_console(self, msg):
        current_text = self.console_label.text
        # Add new log line with red/grey theme
        self.console_label.text = current_text + f"\n[color=a8a8a8]> {msg}[/color]"
        
        # Auto scroll to bottom
        self.scroll.scroll_y = 0

    def start_bot(self, instance):
        if self.bot and self.bot.is_running:
            self.log_to_console("[color=ff0000]Bot is already running![/color]")
            return
            
        self.start_btn.disabled = True
        self.log_to_console("[color=ff0000]>>> INITIATING TSUKUYOMI FLOW...[/color]")
        
        self.bot = ItachiBot(log_callback=self.log_to_console, completion_callback=self.bot_finished)
        
        # Start bot in background thread so UI doesn't freeze
        threading.Thread(target=self.bot.run_automation, daemon=True).start()

    @mainthread
    def bot_finished(self):
        self.start_btn.disabled = False
        self.log_to_console("[color=00ff00]>>> CYCLE COMPLETE![/color]")

if __name__ == '__main__':
    ItachiConsoleApp().run()