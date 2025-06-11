import threading
import time

def _geri_sayim(mesaj, sure, callback):
    for i in range(sure, -1, -1):  # 4,3,2,1,0 gibi sayar
        if callback:
            callback(f"{mesaj} {i}")
        time.sleep(1)

def _nefes_egzersizi_thread(callback):
    adimlar = [
        ("Derin nefes al", 4),
        ("Nefesini tut", 7),
        ("Yavaşça nefes ver", 8),
        ("Tekrar derin nefes al", 4)
    ]

    for mesaj, sure in adimlar:
        _geri_sayim(mesaj, sure, callback)

    if callback:
        callback("Nefes egzersizi tamamlandı.")

def breath(metin: str, callback=None) -> str:
    metin = metin.lower()
    if "nefes egzersizi" in metin or "nefes" in metin:
        threading.Thread(target=_nefes_egzersizi_thread, args=(callback,), daemon=True).start()
        return "Nefes egzersizi başladı..."
    return ""
