import subprocess
import os

dosya_yolu = r"D:/Projeler/haiso"
git_path = r"D:/Program Files/Git/cmd/git.exe"
repo_link = "https://github.com/zHM03/haiso.git"

# Kullanıcı bilgilerini ayarla (bir kere yeter, global yapıyor)
subprocess.run([git_path, "config", "--global", "user.name", "Adınız Soyadınız"])
subprocess.run([git_path, "config", "--global", "user.email", "email@example.com"])

# Git repo başlat
subprocess.run([git_path, "init"], cwd=dosya_yolu)

# Remote kontrol et, varsa URL güncelle yoksa ekle
result = subprocess.run([git_path, "remote"], cwd=dosya_yolu, capture_output=True, text=True)
remotes = result.stdout.split()

if "origin" in remotes:
    subprocess.run([git_path, "remote", "set-url", "origin", repo_link], cwd=dosya_yolu)
else:
    subprocess.run([git_path, "remote", "add", "origin", repo_link], cwd=dosya_yolu)

# Tüm dosyaları git'e ekle
subprocess.run([git_path, "add", "."], cwd=dosya_yolu)

# Değişiklik var mı kontrol et
status_result = subprocess.run([git_path, "status", "--porcelain"], cwd=dosya_yolu, capture_output=True, text=True)

if status_result.stdout.strip() == "":
    print("Commit yapılacak değişiklik yok.")
else:
    # Commit işlemi
    commit_result = subprocess.run([git_path, "commit", "-m", "Yükleme"], cwd=dosya_yolu, capture_output=True, text=True)
    print(commit_result.stdout)
    print(commit_result.stderr)

    # Branch adı main olarak ayarla
    subprocess.run([git_path, "branch", "-M", "main"], cwd=dosya_yolu)

    # Push işlemi
    push_result = subprocess.run([git_path, "push", "-u", "origin", "main"], cwd=dosya_yolu, capture_output=True, text=True)
    print(push_result.stdout)
    print(push_result.stderr)
