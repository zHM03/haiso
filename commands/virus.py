import subprocess

def virus(metin: str) -> str:
    metin = metin.lower()
    
    if "tarama yap" in metin or "virüs tara" in metin or "antivirüs taraması" in metin:
        try:
            # Windows Defender tarama komutu (tam tarama)
            # MpCmdRun.exe'nin yolu:
            defender_path = r"C:\Program Files\Windows Defender\MpCmdRun.exe"
            
            # Tam tarama komutu:
            komut = [defender_path, "-Scan", "-ScanType", "2"]  
            # ScanType 2: Full scan, 1 ise hızlı tarama
            
            # Komutu çalıştır, çıktı yakalanabilir
            sonuc = subprocess.run(komut, capture_output=True, text=True, check=True)
            
            # Komut başarıyla çalıştıysa çıktı döner
            return "Virüs taraması başlatıldı.\nÇıktı:\n" + sonuc.stdout
        
        except FileNotFoundError:
            return "Windows Defender bulunamadı. Lütfen Windows Defender'ın kurulu ve çalışır olduğundan emin olun."
        except subprocess.CalledProcessError as e:
            return f"Virüs taraması başarısız oldu:\n{e.stderr}"
        except Exception as ex:
            return f"Beklenmedik bir hata oluştu: {ex}"
    
    return None
