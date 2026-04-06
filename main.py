from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from itachi_bot import ItachiBot
import threading

class ItachiUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=10, **kwargs)
        self.bot = ItachiBot(self.update_log)

        self.add_widget(Label(text="[b]ITACHI ACCOUNT MAKER v2.1[/b]", markup=True, size_hint_y=0.1))

        self.phone_in = TextInput(text="+91", multiline=False, font_size=20)
        self.add_widget(self.phone_in)

        self.btn_reg = Button(text="1. START REGISTRATION", background_color=(0, 0.4, 1, 1), bold=True)
        self.btn_reg.bind(on_press=self.run_step1)
        self.add_widget(self.btn_reg)

        self.otp_in = TextInput(hint_text="Enter 5-digit OTP", multiline=False, font_size=20)
        self.add_widget(self.otp_in)

        self.btn_otp = Button(text="2. CONFIRM & SAVE", background_color=(0, 0.7, 0, 1), bold=True)
        self.btn_otp.bind(on_press=self.run_step2)
        self.add_widget(self.btn_otp)

        self.logs = Label(text="Status: Ready", markup=True, halign="center")
        self.add_widget(self.logs)

    def update_log(self, msg):
        Clock.schedule_once(lambda dt: self._set_log(msg))

    def _set_log(self, msg):
        self.logs.text = msg

    def run_step1(self, instance):
        threading.Thread(target=lambda: self.bot.step_1_fill_form(self.phone_in.text)).start()

    def run_step2(self, instance):
        threading.Thread(target=lambda: self.bot.step_2_confirm_otp(self.otp_in.text)).start()

class ItachiApp(App):
    def build(self): return ItachiUI()

if __name__ == "__main__": ItachiApp().run()
