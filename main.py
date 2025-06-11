import os
import logging
from kivy.config import Config

from kivy.app import App
from kivy.lang import Builder

from hover import HoverButton  # hover_button_module, sınıfın olduğu dosya adı
from ui import AsistanEkrani

Builder.load_file("ui.kv")

class AsistanApp(App):
    def build(self):
        return AsistanEkrani()

if __name__ == "__main__":
    AsistanApp().run()
