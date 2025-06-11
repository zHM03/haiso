import platform
import subprocess
import tkinter as tk
from tkinter import messagebox

def reset(callback=None):
    if platform.system() != "Windows":
        if callback:
            callback("Bu işlem sadece Windows işletim sisteminde desteklenir.")
        return

    # Tkinter penceresi oluştur ve onay al
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle

    answer = messagebox.askyesno("Bilgi", "Bilgisayar yeniden başlatılsın mı?")
    root.destroy()

    if answer:
        try:
            subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
            if callback:
                callback("Bilgisayar yeniden başlatılıyor...")
        except Exception as e:
            if callback:
                callback(f"Yeniden başlatılamadı: {e}")
    else:
        if callback:
            callback("Yeniden başlatma iptal edildi.")

def komut_isle(metin, callback=None):
    metin = metin.lower()
    if "yeniden başlat" in metin:
        reset(callback)
    else:
        if callback:
            callback("Anlaşılan komut desteklenmiyor.")
