# ui.py ile entegre edilecek örnek kivy popup ve yükleme fonksiyonu

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import mainthread

import subprocess
import os
import threading

class GitPushPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "GitHub'a Yükle"

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.repo_input = TextInput(hint_text="GitHub Repo URL'si", multiline=False, size_hint_y=None, height=40)
        self.path_input = TextInput(hint_text="Yüklemek istediğiniz dosya klasörü", multiline=False, size_hint_y=None, height=40)

        self.status_label = Label(text="", size_hint_y=None, height=40)

        self.submit_btn = Button(text="Yükle", size_hint_y=None, height=40)
        self.submit_btn.bind(on_press=self.start_upload)

        layout.add_widget(self.repo_input)
        layout.add_widget(self.path_input)
        layout.add_widget(self.submit_btn)
        layout.add_widget(self.status_label)

        self.content = layout
        self.size_hint = (0.8, 0.5)

    def start_upload(self, instance):
        repo = self.repo_input.text.strip()
        path = self.path_input.text.strip()

        if not repo or not path:
            self.status_label.text = "[color=ff3333]Lütfen tüm alanları doldurun![/color]"
            return

        if not os.path.exists(path):
            self.status_label.text = "[color=ff3333]Belirtilen klasör bulunamadı![/color]"
            return

        self.status_label.text = "Yükleniyor..."
        self.submit_btn.disabled = True

        # Git yükleme işlemini başka thread'de yap (UI donmasın diye)
        threading.Thread(target=self.git_push, args=(repo, path), daemon=True).start()

    def git_push(self, repo, path):
        git_path = r"D:/Program Files/Git/cmd/git.exe"  # Git exe yolu

        try:
            # Git ayarları
            subprocess.run([git_path, "config", "--global", "user.name", "Adınız Soyadınız"], capture_output=True)
            subprocess.run([git_path, "config", "--global", "user.email", "email@example.com"], capture_output=True)

            # Repo işlemleri
            subprocess.run([git_path, "init"], cwd=path, capture_output=True)
            result = subprocess.run([git_path, "remote"], cwd=path, capture_output=True, text=True)
            remotes = result.stdout.split()

            if "origin" in remotes:
                subprocess.run([git_path, "remote", "set-url", "origin", repo], cwd=path, capture_output=True)
            else:
                subprocess.run([git_path, "remote", "add", "origin", repo], cwd=path, capture_output=True)

            subprocess.run([git_path, "add", "."], cwd=path, capture_output=True)
            commit_result = subprocess.run([git_path, "commit", "-m", "Otomatik yükleme"], cwd=path, capture_output=True, text=True)
            subprocess.run([git_path, "branch", "-M", "main"], cwd=path, capture_output=True)
            push_result = subprocess.run([git_path, "push", "-u", "origin", "main"], cwd=path, capture_output=True, text=True)

            # Push sonucu çıktılarını ana threadde UI'ya bildir
            self.update_status(f"Commit: {commit_result.stdout}\nPush: {push_result.stdout}")

        except Exception as e:
            self.update_status(f"[color=ff3333]Hata oluştu: {str(e)}[/color]")

        self.enable_button()

    @mainthread
    def update_status(self, message):
        self.status_label.text = message

    @mainthread
    def enable_button(self):
        self.submit_btn.disabled = False


# Eğer doğrudan çalıştırmak istersen
class TestApp(App):
    def build(self):
        popup = GitPushPopup()
        popup.open()
        return BoxLayout()  # boş root


if __name__ == "__main__":
    TestApp().run()
