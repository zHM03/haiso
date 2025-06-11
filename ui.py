from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock

import threading
import sounddevice as sd
import numpy as np
import wave
import os
import subprocess
import noisereduce as nr
from datetime import datetime
from faster_whisper import WhisperModel

# Komutlar
from commands.clock import saat
from commands.calculator import hesapla
from commands.notepad import note
from commands.weather import weather
from commands.breath import breath
from commands.cleaner import clean
from commands.reminder import hatirlatici
from commands.shutdown import kapat
from commands.film import film
from commands.search import search
from codding.otomasyon import otomasyon
from codding.github import github_komut

class AsistanEkrani(BoxLayout):
    kullanici_metni = StringProperty("")
    cevap = StringProperty()
    dalga_acik = BooleanProperty(False)
    kayit_suresi = 5  # saniye

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.device = "cpu"
        self.model = None
        self.stream = None
        self.recording = []
        self.fs = 16000
        self.lock = threading.Lock()
        self.yukleniyor_event = None
        self.yukleniyor_durum = 0

        # Saat bazlı selamlama
        saat_ = datetime.now().hour
        if saat_ < 6:
            selam = "İyi geceler Hiso!"
        elif saat_ < 12:
            selam = "Günaydın Hiso!"
        elif saat_ < 18:
            selam = "İyi günler Hiso!"
        else:
            selam = "İyi akşamlar Hiso!"

        self.kullanici_metni = selam

    def modeli_yukle(self):
        if self.model is None:
            self.model = WhisperModel(
                "small",
                device=self.device,
                compute_type="int8"  # daha iyi doğruluk
            )

    def baslat_ses_dalgasi_ve_kayit(self):
        if self.dalga_acik:
            self.ses_kaydi_bitir()
            return

        self.kullanici_metni = "Dinliyorum"
        self.cevap = ""
        self.dalga_acik = True
        self.recording = []

        self.ids.wave.start_animation()
        self.stream = sd.InputStream(
            channels=1,
            samplerate=self.fs,
            callback=self.audio_callback
        )
        self.stream.start()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Ses cihazı durumu: {status}")
        rms = np.sqrt(np.mean(indata**2))
        rms_norm = min(rms * 10, 1.0)
        Clock.schedule_once(lambda dt: setattr(self.ids.wave, "rms_level", float(rms_norm)))
        with self.lock:
            self.recording.append(indata.copy())

    def baslat_yukleniyor_animasyonu(self):
        self.yukleniyor_durum = 0
        if self.yukleniyor_event is None:
            self.yukleniyor_event = Clock.schedule_interval(self.guncelle_yukleniyor_animasyonu, 0.5)

    def durdur_yukleniyor_animasyonu(self):
        if self.yukleniyor_event:
            self.yukleniyor_event.cancel()
            self.yukleniyor_event = None
            Clock.schedule_once(lambda dt: setattr(self, 'kullanici_metni', self.kullanici_metni))

    def guncelle_yukleniyor_animasyonu(self, dt):
        noktalar = "." * ((self.yukleniyor_durum % 3) + 1)
        self.kullanici_metni = f"Çözümleme yapılıyor{noktalar}"
        self.yukleniyor_durum += 1

    def ses_kaydi_bitir(self):
        Clock.schedule_once(lambda dt: setattr(self, 'kullanici_metni', "Çözümleme yapılıyor..."))
        Clock.schedule_once(lambda dt: self.ids.wave.stop_animation())
        self.baslat_yukleniyor_animasyonu()

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        self.dalga_acik = False

        with self.lock:
            audio_np = np.concatenate(self.recording, axis=0).flatten()

        # Gürültü azaltma
        audio_clean = nr.reduce_noise(y=audio_np, sr=self.fs)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        wav_path = os.path.join(base_dir, "kayit.wav")

        # WAV yaz
        audio_data = (audio_clean * 32767).astype(np.int16)
        with wave.open(wav_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.fs)
            wf.writeframes(audio_data.tobytes())

        # Arka planda çözümleme başlat
        threading.Thread(target=self.sesi_coz, args=(wav_path,), daemon=True).start()

    def sesi_coz(self, wav_path):
        try:
            self.modeli_yukle()

            segments, _ = self.model.transcribe(
                wav_path,
                language="tr",
                initial_prompt="Merhaba, ben bir sesli asistanım. Saat, hesap makinesi, hava durumu gibi konularda yardımcı olurum.",
                beam_size=3,
                vad_filter=True
            )
            metin = "".join([segment.text for segment in segments]).strip()
        except Exception as e:
            metin = f"Ses çözümlemede hata: {e}"

        Clock.schedule_once(lambda dt: self.guncelle_cevap(metin))

    def guncelle_cevap(self, metin):
        self.durdur_yukleniyor_animasyonu()
        if not metin.strip():
            metin = ""

        cevap = ""

        def nefes_callback(adim_metni):
            Clock.schedule_once(lambda dt: setattr(self, 'cevap', adim_metni))

        for fonksiyon in [saat, hesapla, note, weather,otomasyon, github_komut, search, clean, hatirlatici, kapat, film]:
            cevap = fonksiyon(metin)
            if cevap:
                break

        if not cevap:
            cevap = breath(metin, callback=nefes_callback)

        if not cevap:
            cevap = "Anlamadım"

        self.kullanici_metni = metin
        self.cevap = cevap
