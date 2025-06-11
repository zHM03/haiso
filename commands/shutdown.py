import re
import threading
import platform
import os
from kivy.clock import Clock

def kapat(metin):
    # "kapat 5 dakika" veya "kapat 5 saat" şeklinde beklenen format
    desen = r"kapat\s+(\d+)\s*(saniye|dakika|saat)"
    eslesme = re.search(desen, metin.lower())

    if not eslesme:
        return None

    sayi = int(eslesme.group(1))
    birim = eslesme.group(2)

    # Saniyeye çevir
    if birim == "saniye":
        sure = sayi
    elif birim == "dakika":
        sure = sayi * 60
    elif birim == "saat":
        sure = sayi * 3600
    else:
        return None

    def kapat_islemi():
        sistem = platform.system()
        if sistem == "Windows":
            os.system("shutdown /s /t 0")
        elif sistem == "Linux" or sistem == "Darwin":  # MacOS için Darwin
            os.system("shutdown -h now")
        else:
            pass  # Desteklenmeyen sistemler

    # Timer ile süre sonunda kapatma işlemi başlatılır
    threading.Timer(sure, kapat_islemi).start()

    return f"{sayi} {birim} sonra bilgisayar kapatılacak."
