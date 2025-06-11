# film_modulu.py
import webbrowser

def film(metin: str) -> str:
    metin = metin.lower().strip()

    if "film bakalım" in metin or "izleyelim" in metin:
        url = "https://www.imdb.com/chart/moviemeter/"
        webbrowser.open(url)
        return "Popüler ve yeni çıkan filmler gösteriliyor."
    
    return None
