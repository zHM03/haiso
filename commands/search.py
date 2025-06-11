import webbrowser

def search(metin: str) -> str:
    metin = metin.lower().strip()
    
    # Metin "araştırma yap" ile başlıyorsa devamını ara
    if metin.startswith("araştırma yap"):
        # "araştırma yap" ifadesini kaldır, kalan arama terimi olsun
        arama_terimi = metin[len("araştırma yap"):].strip()
        
        if not arama_terimi:
            return "Lütfen aramak istediğiniz konuyu yazın."
        
        url = f"https://www.google.com/search?q={arama_terimi.replace(' ', '+')}"
        webbrowser.open(url)
        
        return f"Google'da '{arama_terimi}' aranıyor..."
    
    return None
