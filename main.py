from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from itachi_bot import ItachiBot
import threading

class ItachiInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        
        # Log Display Window
        self.log_display = Label(
            text="[b]ITACHI FB TOOL v1.0[/b]\nReady for Build...",
            markup=True,
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.log_display.bind(texture_size=self.log_display.setter('size'))
        
        scroll = ScrollView(size_hint=(1, 0.8))
        scroll.add_widget(self.log_display)
        self.add_widget(scroll)
        
        # Start Button
        self.btn = Button(text="START AUTOMATION", size_hint=(1, 0.2), background_color=(0, 1, 0, 1))
        self.btn.bind(on_press=self.start_process)
        self.add_widget(self.btn)

    def update_log(self, message):
        Clock.schedule_once(lambda dt: self._append_text(message))

    def _append_text(self, message):
        self.log_display.text += f"\n> {message}"

    def start_process(self, instance):
        self.btn.disabled = True
        self.update_log("Thread Started...")
        # TEST CREDENTIALS (Build se pehle badal lena)
        bot = ItachiBot("YOUR_NUMBER", self.update_log, self.finish_task, None, "YOUR_PASS")
        threading.Thread(target=bot.run_automation).start()

    def finish_task(self):
        self.btn.disabled = False
        self.update_log("Process Finished.")

class ItachiApp(App):
    def build(self):
        return ItachiInterface()

if __name__ == "__main__":
    ItachiApp().run()
