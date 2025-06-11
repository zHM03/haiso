import subprocess
import os

dosya_yolu = r"D:/Projeler/haiso"
git_path = r"D:/Program Files/Git/cmd/git.exe"
repo_link = "https://github.com/zHM03/haiso.git"

# Kullanıcı bilgilerini ayarla (bir kere yeter, global yapıyor)
subprocess.run([git_path, "config", "--global", "user.name", "Adınız Soyadınız"])
subprocess.run([git_path, "config", "--global", "user.email", "email@example.com"])

# Repo işlemleri
subprocess.run([git_path, "init"], cwd=dosya_yolu)

result = subprocess.run([git_path, "remote"], cwd=dosya_yolu, capture_output=True, text=True)
remotes = result.stdout.split()

if "origin" in remotes:
    subprocess.run([git_path, "remote", "set-url", "origin", repo_link], cwd=dosya_yolu)
else:
    subprocess.run([git_path, "remote", "add", "origin", repo_link], cwd=dosya_yolu)

subprocess.run([git_path, "add", "."], cwd=dosya_yolu)

# Commit yapmadan önce dosya olup olmadığını kontrol edebilirsin (opsiyonel)

commit_result = subprocess.run([git_path, "commit", "-m", "Yükleme"], cwd=dosya_yolu, capture_output=True, text=True)
print(commit_result.stdout)
print(commit_result.stderr)

# Branch adını değiştir
subprocess.run([git_path, "branch", "-M", "main"], cwd=dosya_yolu)

# Push
push_result = subprocess.run([git_path, "push", "-u", "origin", "main"], cwd=dosya_yolu, capture_output=True, text=True)
print(push_result.stdout)
print(push_result.stderr)
