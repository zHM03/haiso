import re

def hesapla(metin: str) -> str:
    metin = metin.lower()

    # İşaret kelimelerini sembollere dönüştür
    cevir = {
        "artı": "+",
        "eksi": "-",
        "çarpı": "*",
        "çarpi": "*",   # yazım hatası ihtimali için
        "çarp": "*",
        "bölü": "/",
        "bolu": "/",
        "böl": "/",
        "x": "*",       # burada x harfi de çarpma sembolü olarak ekleniyor
    }

    for kelime, sembol in cevir.items():
        metin = metin.replace(kelime, sembol)

    # Ayrıca büyük X varsa onu da küçük harfe çevirme öncesi veya sonra değiştir
    metin = metin.replace("X", "*")

    pattern = r'(\d+)\s*([\+\-\*/])\s*(\d+)'
    match = re.search(pattern, metin)

    if match:
        sayi1, islem, sayi2 = match.groups()
        sayi1 = float(sayi1)
        sayi2 = float(sayi2)

        try:
            if islem == '+':
                sonuc = sayi1 + sayi2
            elif islem == '-':
                sonuc = sayi1 - sayi2
            elif islem == '*':
                sonuc = sayi1 * sayi2
            elif islem == '/':
                if sayi2 == 0:
                    return "Bir sayı sıfıra bölünemez."
                sonuc = sayi1 / sayi2
            else:
                return None

            if sonuc.is_integer():
                sonuc = int(sonuc)

            return f"{sayi1} {islem} {sayi2} işleminin sonucu {sonuc}."
        except Exception as e:
            return f"Hesaplama sırasında hata oluştu: {e}"

    return None
