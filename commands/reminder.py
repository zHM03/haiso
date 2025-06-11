import re
import threading
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
import os

# Türkçe yazılı sayılar
sayi_sozluk = {
    "bir": 1, "iki": 2, "üç": 3, "dört": 4, "beş": 5,
    "altı": 6, "yedi": 7, "sekiz": 8, "dokuz": 9, "on": 10,
    "on bir": 11, "on iki": 12, "on üç": 13, "on dört": 14,
    "on beş": 15, "on altı": 16, "on yedi": 17, "on sekiz": 18,
    "on dokuz": 19, "yirmi": 20
}

def sayiyi_coz(sayi_str):
    sayi_str = sayi_str.strip()
    try:
        return int(sayi_str)
    except ValueError:
        return sayi_sozluk.get(sayi_str, None)

def hatirlatici(metin, callback=None):
    desen = r"([\w\sçğıöşü]+)\s*(saniye|dakika|saat)\s+sonra\s+(.+)"
    eslesme = re.search(desen, metin.lower())

    if not eslesme:
        return

    sayi_raw = eslesme.group(1).strip()
    birim = eslesme.group(2)
    mesaj = eslesme.group(3).strip()

    sayi = sayiyi_coz(sayi_raw)
    if sayi is None:
        return f"'{sayi_raw}' ifadesi sayı olarak anlaşılamadı."

    # Süreyi saniyeye çevir
    if birim == "saat":
        sure = sayi * 3600
    elif birim == "dakika":
        sure = sayi * 60
    else:
        sure = sayi

    # Eğer mesaj "hatırlat ..." ile başlıyorsa, "hatırlat"ı çıkar
    if mesaj.lower().startswith("hatırlat"):
        mesaj = mesaj[9:].strip()

    def goster_popup():
        # Ses çal
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ses_dosyasi = os.path.join(base_dir, "assets/ding.mp3")
        sound = SoundLoader.load(ses_dosyasi)
        if sound:
            sound.play()

        # Popup göster
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text=f"Hatırlatma:\n{mesaj}", font_size=18, halign='center'))

        buton_kutu = BoxLayout(size_hint_y=0.3, spacing=10)
        btn_tamam = Button(text="Tamam", background_color=(0, 1, 0, 1))

        popup = Popup(title='Hatırlatıcı', content=layout, size_hint=(0.6, 0.4), auto_dismiss=False)

        def kapat(_):
            popup.dismiss()

        def ertele(_):
            popup.dismiss()
            threading.Timer(60, lambda: Clock.schedule_once(lambda dt: goster_popup())).start()

        btn_tamam.bind(on_release=kapat)
        buton_kutu.add_widget(btn_tamam)
        layout.add_widget(buton_kutu)

        popup.open()

    threading.Timer(sure, lambda: Clock.schedule_once(lambda dt: goster_popup())).start()

    return f"{sayi} {birim} sonra sana “{mesaj}” diyeceğim."
