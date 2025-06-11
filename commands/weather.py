import requests

# Yanlış kelime düzeltme sözlüğü
sehirdogru = {
    "burası": "bursa",
    "ismir": "izmir",
    "istanbıl": "istanbul",
    "ankaraa": "ankara",
    "adanaa": "adana",
    "mersinn": "mersin",
    "vursa": "Bursa"
}

def duzelt_sehir_adi(sehir):
    sehir = sehir.lower()
    return sehirdogru.get(sehir, sehir)

def weather(metin: str) -> str:
    metin = metin.lower()

    if "hava" in metin or "hava durumu" in metin:
        # Metni kelimelerine ayır
        kelimeler = metin.split()

        # Hava durumu ile alakalı kelimeleri çıkar
        filtreli = [k for k in kelimeler if k not in ("hava", "durumu", "nasıl", "?", "var", "bana")]

        sehir = None
        # Filtrelenmiş kelimelerden şehir adını bul
        for kelime in filtreli:
            duzeltilmis = duzelt_sehir_adi(kelime)
            if duzeltilmis:
                sehir = duzeltilmis
                break

        if not sehir:
            sehir = "istanbul"  # default şehir

        api_key = "7f1df4d02ef267fb2359c2305d0634e7"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric&lang=tr"

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                sicaklik = data['main']['temp']
                aciklama = data['weather'][0]['description']
                nem = data['main']['humidity']
                ruzgar = data['wind']['speed']
                return (f"{sehir.title()} şu anda {sicaklik} derece, hava durumu {aciklama}.")

            else:
                mesaj = data.get("message", "Hava durumu bilgisi alınamadı.")
                return f"{sehir.title()} için hava durumu bilgisi alınamadı: {mesaj}"

        except Exception as e:
            return f"Hava durumu bilgisi alınırken hata oluştu: {e}"

    return ""
