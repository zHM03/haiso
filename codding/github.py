import subprocess
import os

dosya_yolu = r"D:/Projeler/haiso"
git_path = r"D:/Program Files/Git/cmd/git.exe"
repo_link = "https://github.com/zHM03/haiso.git"

def calistir_git(args, cwd=dosya_yolu):
    """Git komutlarını çalıştır, çıktıyı döndür"""
    result = subprocess.run([git_path] + args, cwd=cwd, capture_output=True, text=True)
    return result

# Kullanıcı bilgilerini ayarla (bir kere yeter, global yapıyor)
calistir_git(["config", "--global", "user.name", "Adınız Soyadınız"])
calistir_git(["config", "--global", "user.email", "email@example.com"])

# Repo işlemleri
calistir_git(["init"])
remotes = calistir_git(["remote"]).stdout.split()

if "origin" in remotes:
    calistir_git(["remote", "set-url", "origin", repo_link])
else:
    calistir_git(["remote", "add", "origin", repo_link])

calistir_git(["add", "."])

commit = calistir_git(["commit", "-m", "Yükleme"])
print(commit.stdout)
print(commit.stderr)

calistir_git(["branch", "-M", "main"])

push = calistir_git(["push", "-u", "origin", "main"])
print(push.stdout)
print(push.stderr)

if "Large files detected" in push.stderr or "GH001" in push.stderr:
    print("Büyük dosya hatası tespit edildi. Git LFS kurulumu ve takibi başlatılıyor...")

    # Git LFS kurulumu (bir kere yeter)
    subprocess.run([git_path, "lfs", "install"], cwd=dosya_yolu)

    # Büyük dosyaları takip et (örnek: .exe dosyaları)
    subprocess.run([git_path, "lfs", "track", "*.exe"], cwd=dosya_yolu)

    # .gitattributes dosyasını git'e ekle
    subprocess.run([git_path, "add", ".gitattributes"], cwd=dosya_yolu)

    # Commit yap
    subprocess.run([git_path, "commit", "-m", "Add Git LFS tracking for large files"], cwd=dosya_yolu)

    # Tekrar push yap
    push = subprocess.run([git_path, "push", "-u", "origin", "main"], cwd=dosya_yolu, capture_output=True, text=True)
    print(push.stdout)
    print(push.stderr)
