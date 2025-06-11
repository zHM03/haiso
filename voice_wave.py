from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty
from kivy.clock import Clock
import math

class VoiceWave(Widget):
    points = ListProperty([])
    rms_level = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._anim_event = None
        self._time = 0
        self._current_genlik = 0  # Şu anki genlik değeri, animasyonda yumuşatma için

    def start_animation(self):
        self.opacity = 1
        self._time = 0
        self._current_genlik = 0
        self._anim_event = Clock.schedule_interval(self.update_wave, 1 / 30.)

    def stop_animation(self):
        if self._anim_event:
            self._anim_event.cancel()
            self._anim_event = None
        self.opacity = 0
        self.points = []
        self.rms_level = 0
        self._current_genlik = 0

    def update_wave(self, dt):
        self._time += dt * 5

        width = self.width / 2
        start_x = (self.width - width) / 2
        height = self.height / 2
        points = []

        min_genlik = 5
        max_genlik = 60

        epsilon = 1e-4
        rms = max(self.rms_level, epsilon)
        rms = min(rms, 1)

        threshold = 0.1
        if rms < threshold:
            scaled_rms = 0
        else:
            scaled_rms = (rms - threshold) / (1 - threshold)

        genlik_ratio = math.log10(1 + 9 * scaled_rms)
        target_genlik = min_genlik + (max_genlik - min_genlik) * (genlik_ratio ** 2)

        # Yumuşatma katsayısı (0 < alpha < 1), küçük olursa daha yavaş değişir
        alpha = 0.2  
        self._current_genlik += alpha * (target_genlik - self._current_genlik)

        for x in range(0, int(width), 10):
            y = height + math.sin(self._time + x * 0.05) * self._current_genlik
            points.extend([self.x + start_x + x, self.y + y])

        self.points = points
