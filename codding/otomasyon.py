import json
import subprocess
import webbrowser
import time

def otomasyon(metin: str) -> str:
    metin = metin.lower()

    if "yazılım" in metin:
        vs_code_path = r"D:\Program Files\Microsoft VS Code\Code.exe"
        workspace_file = r"D:\myworkspace.code-workspace"
        klasorler = [
            r"D:\Dersler",
            r"D:\Ödevler",
            r"D:\Projeler"
        ]
        workspace_data = {
            "folders": [{"path": klasor} for klasor in klasorler],
            "settings": {}
        }

        with open(workspace_file, "w", encoding="utf-8") as f:
            json.dump(workspace_data, f, indent=4, ensure_ascii=False)

        subprocess.Popen([vs_code_path, workspace_file])
        time.sleep(2)
        webbrowser.open("https://www.youtube.com/watch?v=GRxofEmo3HA")
        time.sleep(1)
        webbrowser.open("https://chat.openai.com/")
        time.sleep(1)
        webbrowser.open("https://github.com/")

        return "Workspace ile VS Code ve diğer uygulamalar açıldı."
    else:
        return ""
