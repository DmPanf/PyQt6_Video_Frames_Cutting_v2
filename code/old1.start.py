# https://github.com/DmPanf/PyQt6_Video_Frames_Cutting_v2
# Ver.1.33 [08-2023]
import os
import subprocess

REPO_URL = "https://github.com/DmPanf/PyQt6_Video_Frames_Cutting_v2.git"
PROJECT_DIR = "Video_CUT"
VENV_NAME = "venv"

# Клонирование репозитория
subprocess.run(["git", "clone", REPO_URL, PROJECT_DIR])

# Переходим в каталог проекта
os.chdir(PROJECT_DIR)

# Создаем виртуальное окружение
subprocess.run(["python", "-m", "venv", VENV_NAME])

# Устанавливаем необходимые библиотеки
pip_path = os.path.join(VENV_NAME, "bin", "pip")
subprocess.run([pip_path, "install", "-r", "requirements.txt"])

# Запускаем main.py с использованием виртуального окружения
python_path = os.path.join(VENV_NAME, "bin", "python")
subprocess.run([python_path, "main.py"])
