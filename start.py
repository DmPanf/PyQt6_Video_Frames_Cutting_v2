https://github.com/DmPanf/PyQt6_Video_Frames_Cutting_v2

import os
import subprocess

REPO_URL = "https://github.com/ваш_логин/имя_репозитория.git"
PROJECT_DIR = "имя_каталога_проекта"
VENV_NAME = "venv"

# Клонирование репозитория
subprocess.run(["git", "clone", REPO_URL, PROJECT_DIR])

# Переходим в каталог проекта
os.chdir(PROJECT_DIR)

# Создаем виртуальное окружение
subprocess.run(["python", "-m", "venv", VENV_NAME])

# Устанавливаем необходимые библиотеки
pip_path = os.path.join(VENV_NAME, "bin", "pip")
subprocess.run([pip_path, "install", "PyQt6", "opencv-python"])

# Запускаем main.py с использованием виртуального окружения
python_path = os.path.join(VENV_NAME, "bin", "python")
subprocess.run([python_path, "main.py"])
