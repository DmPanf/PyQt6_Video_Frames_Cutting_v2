import os
import subprocess

def create_startup_script(project_path, venv_path):
    startup_script_content = f"""
@echo off
call {os.path.join(venv_path, 'Scripts', 'activate.bat')}
python main.py
pause
"""
    startup_script_path = os.path.join(project_path, "start_project.bat")
    with open(startup_script_path, 'w') as file:
        file.write(startup_script_content)
    print(f"Startup script created at {startup_script_path}")


def generate_project_dir(base_name="Project"):
    count = 1
    while True:
        project_dir = f"{base_name}{count:03}"
        if not os.path.exists(project_dir):
            return project_dir
        count += 1

REPO_URL = "https://github.com/DmPanf/PyQt6_Video_Frames_Cutting_v2.git"
PROJECT_DIR = generate_project_dir()
VENV_NAME = "venv"

# Определение базового пути
BASE_PATH = os.getcwd()
PROJECT_PATH = os.path.join(BASE_PATH, PROJECT_DIR)
VENV_PATH = os.path.join(PROJECT_PATH, VENV_NAME)
PIP_PATH = os.path.join(VENV_PATH, "Scripts", "pip.exe")
PYTHON_PATH = os.path.join(VENV_PATH, "Scripts", "python.exe")
REQ_PATH = os.path.join(PROJECT_PATH, "requirements.txt")

# Клонирование репозитория
subprocess.run(["git", "clone", REPO_URL, PROJECT_DIR])

# Переходим в каталог проекта
os.chdir(PROJECT_DIR)

# Создаем виртуальное окружение
subprocess.run(["python", "-m", "venv", VENV_NAME])

# Устанавливаем необходимые библиотеки, если файл requirements.txt существует
if os.path.exists(REQ_PATH):
    subprocess.run([PIP_PATH, "install", "-r", REQ_PATH])
else:
    print("File 'requirements.txt' not found!")

# Создаем стартовый скрипт для удобного запуска проекта
create_startup_script(PROJECT_PATH, VENV_PATH)

# Первичный запуск main.py с использованием виртуального окружения
subprocess.run([PYTHON_PATH, "main.py"])

print(f'\n⚙️ Проект загружен в папку {PROJECT_DIR}, библиотеки установлены,\nдля последующего запуска можно использовать "tart_project.bat"!')
