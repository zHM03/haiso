def note(metin: str) -> str:
    metin = metin.strip()
    kelimeler = metin.split()

    # "not" kelimesi ile başlamıyorsa işlemi yapma
    if len(kelimeler) < 3 or kelimeler[0].lower() != "not":
        return None

    dosya_adi = kelimeler[1].lower() + ".txt"  # ikinci kelime dosya adı
    yazi = " ".join(kelimeler[1:])             # 2. kelimeden itibaren hepsi

    try:
        with open(dosya_adi, "a", encoding="utf-8") as dosya:
            dosya.write(yazi + "\n")
        return "Notunuzu kaydettim."
    except Exception as e:
        return f"Not kaydedilirken hata oluştu: {e}"
