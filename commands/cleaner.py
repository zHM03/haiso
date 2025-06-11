import os
import shutil
import tempfile

def clean(metin):
    komutlar = ["temizle", "temizlik zamanı", "geçici dosyaları sil"]

    if not any(k in metin.lower() for k in komutlar):
        return None

    mesajlar = []

    # %TEMP% klasörü
    try:
        temp_path = tempfile.gettempdir()
        for root, dirs, files in os.walk(temp_path, topdown=False):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except Exception:
                    pass
            for name in dirs:
                try:
                    shutil.rmtree(os.path.join(root, name), ignore_errors=True)
                except Exception:
                    pass
        mesajlar.append("TEMP klasörü temizlendi.")
    except Exception as e:
        mesajlar.append(f"%TEMP% klasörü temizlenemedi: {e}")

    # Prefetch klasörü
    try:
        prefetch_path = r"C:\Windows\Prefetch"
        for root, dirs, files in os.walk(prefetch_path, topdown=False):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except Exception:
                    pass
        mesajlar.append("Prefetch klasörü temizlendi.")
    except Exception as e:
        mesajlar.append(f"Prefetch klasörü temizlenemedi: {e}")  # Yönetici gerekebilir

    # C:\Windows\Temp klasörü
    try:
        alt_temp = r"C:\Windows\Temp"
        if os.path.exists(alt_temp):
            for root, dirs, files in os.walk(alt_temp, topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except Exception:
                        pass
                for name in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, name), ignore_errors=True)
                    except Exception:
                        pass
            mesajlar.append("Temp klasörü temizlendi.")
    except Exception as e:
        mesajlar.append(f"C:\\Windows\\Temp klasörü temizlenemedi: {e}")

    return "\n".join(mesajlar)
