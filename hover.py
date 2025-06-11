from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.factory import Factory


class HoverBehavior:
    hovered = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            return
        self.hovered = inside
        if inside:
            self.on_enter()
        else:
            self.on_leave()

    def on_enter(self):
        pass

    def on_leave(self):
        pass


class HoverButton(HoverBehavior, Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anim = None
        self.normal_size = None
        self.normal_pos = None

    def on_enter(self):
        if self.anim:
            self.anim.cancel(self)

        self.normal_size = self.size[:]
        self.normal_pos = self.pos[:]

        new_w = self.width * 1.1
        new_h = self.height * 1.1
        new_x = self.center_x - new_w / 2
        new_y = self.center_y - new_h / 2

        self.anim = Animation(size=(new_w, new_h), pos=(new_x, new_y), duration=0.2)
        self.anim.start(self)

    def on_leave(self):
        if self.anim:
            self.anim.cancel(self)

        if self.normal_size and self.normal_pos:
            self.anim = Animation(size=self.normal_size, pos=self.normal_pos, duration=0.2)
            self.anim.start(self)


# Factory kaydı, böylece KV dosyasında <HoverButton> olarak kullanabilirsin
Factory.register('HoverButton', cls=HoverButton)
