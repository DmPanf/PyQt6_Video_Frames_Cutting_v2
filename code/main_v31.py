import sys  # Импортируем модуль sys для получения аргументов командной строки
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QGridLayout, 
                             QLabel, QSlider, QLineEdit, QPushButton, QFileDialog)
from PyQt6.QtCore import Qt, QTimer, QSize  # Импортируем модуль QtCore
from PyQt6.QtGui import QPixmap, QGuiApplication, QImage  # Импортируем модуль для работы с изображениями 
import cv2  # Импортируем модуль cv2 для работы с видео
import os   # Импортируем модуль os для работы с файлами 
import configparser  # Импортируем модуль configparser для работы с конфигурацией 


def read_config():  # Функция чтения конфигурации
    config = configparser.ConfigParser()  # Создаем объект конфигурации
    if not os.path.exists('config.ini'):  # Проверяем, существует ли файл config.ini
        raise FileNotFoundError("config.ini not found!")  # Если нет, выдаем ошибку
    config.read('config.ini')  # Читаем файл
    image_path = config.get('CONFIG', 'basic_image_path', fallback="./images/00.jpg")  # Загружаем изображение 
    frames_dir = config.get('CONFIG', 'default_frames_dir', fallback="./OUTPUT/")  # Загружаем папку
    temp_name = config.get('CONFIG', 'temp_name', fallback="temp")  # Загружаем имя файла временного кадра 
    frames_number = config.get('CONFIG', 'frames_number', fallback="5")  # Загружаем количество изображений для пропуска
    win_title = config.get('CONFIG', 'win_title', fallback="Video")  # Загружаем заголовок окна 
    return image_path, frames_dir, temp_name, frames_number, win_title  # Возвращаем конфигурацию


class VideoApp(QWidget):  # Класс виджета VideoApp
    def __init__(self):
        super().__init__()  # Инициализация виджета и отображения изображения в виджете 

        self.video_path = None  # Путь к видео 
        self.cap = None  # Создаем объект для работы с видео
        self.timer = QTimer(self)  # Создаем таймер 
        self.timer.timeout.connect(self.play_video)  # Подписываемся на событие таймера self.timer 

        # Загрузка конфигурации и установка начального изображения
        self.image_path, self.frames_dir, self.temp_name, self.frames_number, self.win_title = read_config()  # Загрузка конфигурации 
        self.init_ui()  # Функция инициализации виджета и отображения изображения в виджете


    def init_ui(self):  # Функция инициализации виджета и отображения изображения в виджете 
        # Создаем QLabel для отображения изображения
        self.image_label = QLabel(self)  # Создаём виджет QLabel для отображения изображения 
        pixmap = QPixmap(self.image_path)  # Преобразуем путь к изображению в QPixmap 
        self.image_label.setPixmap(pixmap.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio))  # 640x480 - примерные размеры

        # Создаем макет, который будет центрировать image_label относительно его родительского виджета или окна
        layout = QVBoxLayout(self)  # Установите этот макет для вашего главного виджета или окна
        # layout.setContentsMargins(0, 0, 0, 0) # внутренние отступы = 0
        # layout.addWidget(self.image_label) # Вместо одной строки описываем все детально))
        layout.addStretch(1)  # Добавляем пустое пространство сверху
        frame_widget = QWidget()  # Создаём виджет для QGridLayout
        frame_layout = QGridLayout()  # Создаём QGridLayout и центрируем виджет Изображения в родительском макете
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(QWidget(), 0, 0, 1, 1)  # Пустое пространство в верхней части
        frame_layout.addWidget(QWidget(), 1, 0)  # Пустое пространство слева
        frame_layout.addWidget(self.image_label, 1, 1)  # Центрирование виджета
        frame_layout.addWidget(QWidget(), 1, 2)  # Пустое пространство справа
        frame_layout.addWidget(QWidget(), 2, 0, 1, 1)  # Пустое пространство в нижней части
        frame_widget.setLayout(frame_layout)  # Применяем QGridLayout к виджету
        layout.addWidget(frame_widget)  # Добавляем виджет с QGridLayout в основной макет
        layout.addStretch(1)  # Добавляем пустое пространство снизу
        # addWidget(widget, row, column, rowSpan=1, columnSpan=1)
        # row - номер строки, в которой должен размещаться виджет
        # column - номер столбца, в котором должен размещаться виджет
        # rowSpan (необязательно) - сколько строк виджет должен занимать в сетке. По умолчанию это 1
        # columnSpan (необязательно) - сколько столбцов виджет должен занимать в сетке. По умолчанию это 1


        # Video Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)  # Создаем слайдер виджета QSlider 
        self.slider.valueChanged.connect(self.slider_moved) # обработчик событий для события valueChanged слайдера  
        layout.addWidget(self.slider)  # Добавляем слайдер в макет
        # Connect the slider valueChanged signal to the set_video_position function
        self.slider.valueChanged.connect(self.set_video_position)  # Связываем слайдер с функцией set_video_position
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 3px; /* размер трека */
                background: #c9c9c9; /* цвет фона трека */
                margin: 0px;
            }
            QSlider::handle:horizontal {
                background: #505050; /* цвет ползунка */
                border: 2px solid #0c0c0c; /* рамка вокруг ползунка */
                width: 25px; /* размер ползунка */
                margin: -7px 0; /* размер ползунка по отношению к треку */
                border-radius: 7px; /* закругленные углы ползунка */
            }
            QSlider {
                border: 2px solid #0c0c0c; /* рамка вокруг всего слайдера */
                padding: 3px;
            }
        """)


        # Info Panel
        info_layout = QHBoxLayout()  # Основной макет для информации в горизонтальном режиме
        self.start_label = QLineEdit("1")  # Начальное значение 
        self.current_frame_label = QLabel(" 0")  # Начальное значение
        self.end_label = QLineEdit("30")  # Конечное значение 
        self.skip_frames = QLineEdit(self.frames_number)  # Количество кадров
        self.name_label = QLabel("Template:")  # Название изображения 
        self.output_name = QLineEdit(self.temp_name)  # Имя файла 

        # Устанавливаем стили для QLineEdit:
        font_style = "background-color: darkgray; font-size: 18px; color: darkblue; font-weight: bold;"
        self.start_label.setFixedWidth(65)  # Устанавливаем ширину значений LineEdit
        self.start_label.setStyleSheet(font_style)  # Устанавливаем цвет шрифта значений LineEdit
        self.current_frame_label.setFixedWidth(65)  # 
        self.current_frame_label.setStyleSheet("font-size: 18px; font-weight: bold;")  # 
        self.end_label.setFixedWidth(65)
        self.end_label.setStyleSheet(font_style)
        # self.skip_frames.setStyleSheet("background-color: lightgray; width: 35px; font-size: 16px; color: darkgreen;")
        self.skip_frames.setFixedWidth(35)
        self.skip_frames.setStyleSheet(font_style)
        # self.name_label.setFixedWidth(80)
        self.name_label.setStyleSheet("font-size: 16px;")
        # self.output_name.setStyleSheet("background-color: lightgray; width: 200px; font-size: 16px; color: darkgreen;")
        self.output_name.setStyleSheet(font_style)

        info_layout.addWidget(self.start_label)
        info_layout.addWidget(self.current_frame_label)   # 
        info_layout.addWidget(self.end_label)             # Добавляем QLineEdit
        info_layout.addWidget(self.skip_frames)           # Строки "Начальное", "Текущее", "Конечное" добавляются в макет
        info_layout.addWidget(self.name_label)            # Добавляем QLineEdit
        info_layout.addWidget(self.output_name)           # Lейблы "Начальное", "Текущее", "Конечное" добавляются в макет 
        layout.addLayout(info_layout)                     # Добавляем макет в основной макет

        # Button Panel
        btn_layout = QHBoxLayout()  # Создаем макет для кнопок в горизонтальном режиме
        self.load_btn = QPushButton("VIDEO LOAD")
        self.play_btn = QPushButton("PLAY/STOP")
        self.cut_btn = QPushButton("CUT and SAVE")
        self.return_btn = QPushButton("RESET")

        buttons = [self.load_btn, self.play_btn, self.cut_btn, self.return_btn]  # Список кнопок
        for button in buttons:  # Поочередно добавляем кнопки в макет
            button.setFixedHeight(42)  # Устанавливаем высоту
            button.setStyleSheet("""
                QPushButton {
                    background-color: #15a049;
                    color: white;
                    border-radius: 12px;
                    font-size: 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0e6f33;
                }
            """)

        self.load_btn.clicked.connect(self.load_video)       # кнопка "Load Video"
        self.play_btn.clicked.connect(self.toggle_play)      # кнопка "Play/Stop"
        #self.cut_btn.clicked.connect(self.cut_frames)
        self.cut_btn.clicked.connect(self.confirm_action)    # будет представлено диалоговое окно с подтверждением
        self.return_btn.clicked.connect(self.return_values)  # возвращение в начальное состояние

        btn_layout.addWidget(self.load_btn)    # Button "Load Video"
        btn_layout.addWidget(self.play_btn)    # Button "Play/Stop"
        btn_layout.addWidget(self.cut_btn)     # Button "Cut and Save"
        btn_layout.addWidget(self.return_btn)  # Button "Reset"
        layout.addLayout(btn_layout)           # Добавляем кнопки в макет

        # Info Widget 
        self.info_widget = self.create_info_widget()  # Создаем виджет с информацией
        self.info_widget.setStyleSheet("background-color: #c0c0c0; color: darkblue;")  # Цвет фона - серый
        layout.addWidget(self.info_widget)  # Добавляем виджет с информацией в основной макет
        layout.addSpacing(10) # отступ между виджетами
        self.setLayout(layout) # Применяем QGridLayout к виджету

        self.setWindowTitle(self.win_title)  # Устанавливаем заголовок
        self.update_image()  # обновляем изображение
        #self.center()
        self.show()  # показываем виджет


    def center(self):  # центрируем виджет
        screen = QGuiApplication.screens()[0]  # получаем экран
        #screen_geometry = screen.availableGeometry()  # получаем доступную геометрию экрана 
        screen_geometry = screen.geometry()  # получаем геометрию экрана
        window_geometry = self.frameGeometry()  # получаем геометрию виджета
        window_geometry.moveCenter(screen_geometry.center())  # центрируем виджет
        window_geometry.moveTop(window_geometry.top() - 170)  # отступ от верха
        self.move(window_geometry.topLeft())  # перемещаем виджет


    def resizeEvent(self, event):  # обработчик события resize
        super().resizeEvent(event) # вызываем метод родительского класса


    def load_video(self):  # загрузка видео
        self.video_path, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.webm)")  # выбор файла
        if self.video_path:  # если пользователь выбрал файл
            self.cap = cv2.VideoCapture(self.video_path)  # открываем видео
            ret, frame = self.cap.read()  # прочитываем 1 кадр
            if ret:  # если кадр есть
                self.show_frame_on_label(frame)  # покажем его на виджете

            # при загрузке видео показывается номер последнего кадра:
            frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Получаем количество кадров
            self.slider.setMaximum(frame_count)  # Устанавливаем максимальное значение слайдера
            self.end_label.setText(str(frame_count))  # Устанавливаем конечное значение слайдера для диалогового окна
            self.update_info_widget()  # обновляем информационный виджет
            self.update_slider_position()  # обновляем положение слайдера
            self.start_label.setText("1")  # устанавливаем начальное значение

            # Устанавливаем имя файла для сохранения 
            base_name = os.path.basename(self.video_path)  # Имя файла
            video_name_without_extension = os.path.splitext(base_name)[0]  # Имя без расширения
            self.output_name.setText(video_name_without_extension)  # Устанавливаем имя файла для сохранения

            # Ограничение размеров приложения максимальными высотой и шириной экрана монитора
            screen_size = QApplication.primaryScreen().size()  # Размер экрана
            print(f'\nРазмер экрана {screen_size}')
            screen_width = screen_size.width() - 20  # Максимальная ширина для отображения 
            screen_height = screen_size.height() - 80  # Максимальная высота для отображения
            print(f'Размер: {screen_width}x{screen_height}\n')
            self.setMaximumSize(QSize(screen_width, screen_height))  # Максимальная ширина и высота
            self.setMinimumSize(QSize(640, 500))  # Минимальная ширина и высота
            self.center()  # Центрируем виджет


    def show_frame_on_label(self, frame):  # показать кадр на виджете
        screen_size = QApplication.primaryScreen().size()  # Размер экрана
        if screen_size.height() > 1000:  # Если экран больше 1000 пикселей по высоте
            MAX_HEIGHT = 720  # Максимальная высота для отображения
        else:
            MAX_HEIGHT = int(screen_size.height() * 0.65)  # Максимальная высота для отображения 80% экрана
        scaling_factor = 1  # Фактор масштабирования
        
        # После выбора видео загрузка первого кадра и подгон размера окна
        height, width, _ = frame.shape  # Получаем размеры кадра и количество каналов (channel)

        # Если высота кадра больше максимальной, вычисляем фактор масштабирования
        if height > MAX_HEIGHT:
            scaling_factor = MAX_HEIGHT / height

        scaled_width = int(width * scaling_factor)  # Вычисляем масштабированную ширину
        scaled_height = int(height * scaling_factor)  # Вычисляем масштабированную высоту
        
        bytes_per_line = 3 * width  # Вычисляем количество байтов в строке
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)  # Создаем QImage из кадра
        pixmap = QPixmap.fromImage(q_image)  # Преобразуем QImage в QPixmap
        
        # Устанавливаем масштабированный QPixmap на image_label
        scaled_pixmap = pixmap.scaled(scaled_width, scaled_height, Qt.AspectRatioMode.KeepAspectRatio)  # Масштабируем Pixmap 
        self.image_label.setPixmap(scaled_pixmap)  # Устанавливаем QPixmap на виджет 
        self.image_label.setFixedSize(scaled_pixmap.size())  # Устанавливаем фиксированную ширину и высоту 

        # Обновляем информационный виджет
        self.setWindowTitle(f'{self.win_title} [{os.path.basename(self.video_path)}] [{scaled_width}x{scaled_height}]')

        # Устанавливаем высоту и ширину видео
        height_of_image = scaled_height  # Используем масштабированную высоту
        height_of_other_widgets = 235  # Высота других элементов управления
        total_height = height_of_image + height_of_other_widgets  # Общая высота окна
        self.setFixedHeight(total_height)  # Устанавливаем фиксированную высоту 

        width_of_image = max(scaled_width, 500)  # Используем масштабированную ширину с дополнительным отступом или минимум 420
        self.setFixedWidth(width_of_image)  # Устанавливаем фиксированную ширину 
        #self.center()

    def update_image(self):  # обновляем изображение 
        pixmap = QPixmap(self.image_path)  # Получаем QPixmap из пути к изображению 
        new_width = max(self.width(), 500)  # Если ширина видео меньше 650, фиксируем ширину в 650
        # new_width = self.width()
        aspect_ratio = pixmap.width() / pixmap.height()  # Вычисляем соотношение ширины и высоты
        new_height = int(new_width / aspect_ratio)  # Вычисляем новую высоту 
        scaled_pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio)  # Масштабируем QPixmap 
        self.image_label.setPixmap(scaled_pixmap)  # Устанавливаем QPixmap на виджет 
        # Обновляем информационный виджет
        self.setWindowTitle(f'{self.win_title} [{new_width}x{new_height}]')  # Устанавливаем новую высоту и ширину видео
        self.center()  # Центрируем виджет 


    def toggle_play(self):  # Переключаем видео на паузу или воспроизведение 
        if self.timer.isActive():  # Если видео воспроизводится
            self.timer.stop()  # останавливаем таймер 
        else:  # Если видео не воспроизводится
            self.timer.start(30)  # запускаем таймер

    def play_video(self):  # Запускаем видео
        if self.cap:  # Если видео загружено 
            ret, frame = self.cap.read()  # Читаем следующий кадр 
            if ret:  # если кадр есть
                height, width, channel = frame.shape  # получаем размеры кадра и количество каналов 
                bytes_per_line = 3 * width  # Вычисляем количество байтов в строке 
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)  # Создаем QImage из кадра 
                pixmap = QPixmap.fromImage(q_image)  # Преобразуем QImage в QPixmap 
                self.image_label.setPixmap(pixmap)  # Устанавливаем QPixmap на виджет 
                self.update_slider_position()  # Обновляем положение слайдера 
            else:  # если кадр не получен 
                self.timer.stop()  # останавливаем таймер 
        else:  # если видео не загружено
            self.timer.stop()  # останавливаем таймер
            self.show_error("Ошибка воспроизведения", "Видео не загружено или произошла ошибка при его чтении.")
            #pass


    def update_slider_position(self):  # Обновляем положение слайдера
        if self.cap:  # Если видео загружено
            self.slider.setValue(int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)))  # Устанавливаем положение слайдера
            # при проигрывании видео и при перемещении ползунка слайдера:
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))  # Получаем текущий кадр 
            self.current_frame_label.setText(f' {current_frame}')  # Устанавливаем текущий кадр на виджете 

    def slider_moved(self):  # При перемещении ползунка слайдера
        # когда будет двигаться слайдер, метка с номером текущего кадра будет автоматически обновляться
        if self.cap:  # Если видео загружено
            # Устанавливаем позицию видео в соответствии с положением слайдера
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.slider.value())  # Устанавливаем положение слайдера 
            # Считаем текущий кадр из видео
            ret, frame = self.cap.read()  # прочитаем 1 кадр из видео 
            if ret:  # если кадр есть
                # Преобразовываем кадр в QPixmap и устанавливаем его для QLabel
                pixmap = self.frame_to_pixmap(frame)  # преобразовываем кадр в QPixmap 
                self.image_label.setPixmap(pixmap)  # Устанавливаем QPixmap на виджет 

            # Обновляем метку с номером текущего кадра
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))  # Получаем текущий кадр 
            self.current_frame_label.setText(f' {current_frame}')  # Устанавливаем текущий кадр на виджете 
        else:
            #self.timer.stop()
            #self.show_error("Ошибка воспроизведения", "Видео не загружено или произошла ошибка при его чтении.")
            pass


    def frame_to_pixmap(self, frame): # функция преобразует кадр из формата OpenCV (BGR) в изображение QPixmap
        # Функция преобразует кадр из формата OpenCV (BGR) в изображение QPixmap, которое можно отображать в QLabel
        height, width, _ = frame.shape  # Получаем размеры кадра и количество каналов (channel)
        bytes_per_line = 3 * width  # Вычисляем количество байтов в строке 
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)  # Создаем QImage из кадра 
        pixmap = QPixmap.fromImage(q_image)  # Преобразуем QImage в QPixmap 
        return pixmap  # Возвращаем преобразованный QPixmap


    def set_video_position(self, position):  # Устанавливаем положение видео на определенную позицию в слайдере 
        if self.cap:  # Если видео загружено 
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)  # Устанавливаем положение слайдера 

    def get_video_info(self):  # Получаем информацию о видео 
        if not self.cap:  # Если видео не загружено 
            return {}  # Возвращаем пустой словарь 
        
        # Получение параметров видео с помощью OpenCV
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Получаем ширину кадра
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Получаем высоту кадра
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))  # Получаем частоту воспроизведения 
        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Получаем количество кадров 
        duration = frame_count / fps  # Получаем длительность видео 
        codec = int(self.cap.get(cv2.CAP_PROP_FOURCC))  # Получаем кодек видео
        codec_name = "".join([chr((codec >> 8 * i) & 0xFF) for i in range(4)])  # Получаем имя кодека 
        
        # Получение размера файла
        file_size = os.path.getsize(self.video_path)  # в байтах
        file_size_mb = file_size / (1024 * 1024)  # в мегабайтах

        info = {
            "⚙️ PATH": self.video_path,
            "\n⚙️ SIZE": f"[{file_size_mb:.2f} MB]",
            "⚙️ CODEC": codec_name,
            "⚙️ DURATION": f"[{duration:.2f} s]",
            "\n⚙️ VIDEO": f"[{width} X {height}]",
            "⚙️ FRAMES": f"[{frame_count}]",
            "⚙️ FPS": f"[{fps}]"
        }
        return info  # Возвращаем словарь с информацией 

    def create_info_widget(self):  # Создаем виджет с информацией 
        # font_style = "background-color: darkgray; font-size: 18px; color: darkblue; font-weight: bold;"
        label_style = "background-color: gray;  font-size: 14px; color: darkgreen; padding: 10px; border: 1px solid #15a049; font-weight: bold;"
        #label_style = "background-color: darkgray; padding: 10px; border: 1px solid #15a049;"  # стили для виджета с информацией
        info_label = QLabel(self)  # Создаем виджет с информацией
        info_label.setWordWrap(True)  # Включаем перенос строк 
        info_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)  # Устанавливаем выравнивание 
        info_label.setStyleSheet(label_style)  # Устанавливаем стили
        info_label.setContentsMargins(25, 15, 5, 15)  # Устанавливаем отступы (Левый отступ - 20, Верхний отступ - 15, Правый отступ - 5, Нижний отступ - 15)
        # Отступы определяют расстояние между границей виджета (или макета) и его содержимым в пикселях 
        # См. https://doc.qt.io/qt-5/qwidget.html#contentsMargins-property
        return info_label  # Возвращаем виджет с информацией 


    def update_info_widget(self):  # Обновляем информационный виджет
        info = self.get_video_info()  # Получаем информацию о видео 
        info_text = " ".join([f"{key}: {value}" for key, value in info.items()])  # Преобразуем словарь в строку 
        self.info_widget.setText(info_text)  # Устанавливаем информационный виджет 


    def cut_frames(self):  # Вырезаем кадры из видео 
        if not hasattr(self, 'video_path') or not self.video_path:  # Если видео не загружено 
            self.show_error("Видео не загружено!", "Пожалуйста, загрузите видео перед выделением кадров.")  # Показываем ошибку в виджете предупреждений
            return  # Выходим 

        start_frame = self.get_label_value(self.start_label)  # Получаем начальное значение 
        end_frame = self.get_label_value(self.end_label)  # Получаем конечное значение
        skip_frames = self.get_label_value(self.skip_frames)  # Получаем пропуск кадров 

        if not all(isinstance(i, int) and i >= 0 for i in [start_frame, end_frame, skip_frames]):  # Если значения не являются целыми числами
            self.show_error("Неверное значение!", "Убедитесь, что значения начала, конца и пропуска кадров являются положительными целыми числами.")
            return  # Выходим 

        if start_frame >= end_frame:  # Если начальный кадр больше конечного 
            self.show_error("Неверный диапазон!", "Конечный кадр должен быть больше начального.")  # Показываем ошибку в виджете предупреждений
            return  # Выходим

        cap = cv2.VideoCapture(self.video_path)  # Загружаем видео 
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Получаем количество кадров 

        if end_frame > frame_count:  # Если конечный кадр больше количества кадров в видео 
            self.show_error("Неверное значение!", "Конечный кадр больше количества кадров в видео.")
            return  # Выходим

        base_name = os.path.basename(self.video_path)  # Получаем имя файла
        video_name_without_extension = os.path.splitext(base_name)[0] # Убираем расширение
        # Если output_name задан, используем его вместо video_name_without_extension
        output_name_value = self.output_name.text().strip() # вместо video_name_without_extension
        if output_name_value:  # Если output_name задан
            video_name_without_extension = output_name_value # Убираем расширение
        else:
            self.output_name.setText(video_name_without_extension) # Обновляем поле для Шаблона

        save_path = os.path.join(self.frames_dir, video_name_without_extension)  # Получаем путь к папке с кадрами 

        if not os.path.exists(save_path):  # Если папка с кадрами не существует 
            os.makedirs(save_path)  # Создаем папку с кадрами 

        count = 0  # Счетчик кадров 
        for i in range(start_frame, end_frame, skip_frames):  # Перебираем кадры 
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)  # Устанавливаем положение слайдера 
            ret, frame = cap.read()  # прочитаем 1 кадр из видео 
            if ret:  # если кадр есть 
                # frame_name = f"{video_name_without_extension}_{count:03}.jpg"
                frame_count = count * skip_frames + start_frame  # Устанавливаем номер кадра 
                frame_name = f"{video_name_without_extension}_{frame_count:04d}.png"  # Формируем имя файла с четырехзначным номером кадра
                frame_path = os.path.join(save_path, frame_name)  # Получаем путь к файлу 
                cv2.imwrite(frame_path, frame)  # Записываем кадр в файл 
                count += 1  # Увеличиваем счетчик кадров 

        cap.release()  # Освобождаем ресурсы 
        self.show_info(f"Фреймы в количестве {count} штук успешно сохранены в папке {save_path}!")  # Показываем сообщение в информационном виджете

    def get_label_value(self, label):  # Получаем значение из виджета
        try:  # Проверяем, является ли значение целым
            return int(label.text().strip())  # Возвращаем значение 
        except ValueError:  # Если не является
            return None  # Возвращаем None

    def show_error(self, title, message):  # Показываем ошибку в виджете предупреждений
        msg_box = QMessageBox(self)  # Создаем виджет предупреждений
        msg_box.setIcon(QMessageBox.Icon.Critical)  # Устанавливаем иконку предупреждения
        msg_box.setWindowTitle(title)  # Устанавливаем заголовок виджета предупреждения
        msg_box.setText(message)  # Устанавливаем сообщение 
        msg_box.exec()  # Отображаем виджет предупреждений 

    def show_info(self, message):  # Показываем информационное окно 
        msg_box = QMessageBox(self)  # Создаем виджет предупреждений 
        msg_box.setIcon(QMessageBox.Icon.Information)  # Устанавливаем иконку предупреждения 
        msg_box.setWindowTitle("Информация")  # Устанавливаем заголовок виджета предупреждения
        msg_box.setText(message)  # Устанавливаем сообщение
        msg_box.exec()  # Отображаем виджет предупреждений 


    def confirm_action(self):  # Подтверждаем действие 
        message = f"Начальный кадр: {self.start_label.text()}\n" \
                f"Конечный кадр: {self.end_label.text()}\n" \
                f"Пропускакть: {self.skip_frames.text()} кадр(ов)\n" \
                f"Шаблон для сохранения: {self.output_name.text()}"

        reply = QMessageBox.question(self, 'Подтвердить действие',
                                    message, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Ok:  # Если действие подтвердили 
            self.cut_frames()  # Выполняем действие 
        else:
            # Если необходимо, можно добавить дополнительные действия при отмене.
            pass


    def return_values(self):  # Возвращаем значения из виджета 
        self.start_label.setText("1")  # Устанавливаем начальное значение 
        self.skip_frames.setText(self.frames_number)  # Устанавливаем пропуск кадров
        self.output_name.setText(self.temp_name)  # Устанавливаем имя для шаблона
        self.slider.setValue(0)  # Устанавливаем положение слайдера на 0
        if self.cap is not None:  # Если видео загружено 
            self.end_label.setText(str(int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))))  # Устанавливаем конечное значение 
        else:  # Если видео не загружено
            # Обработка ошибки или установка дефолтного значения для self.end_label
            self.end_label.setText("30")  # Устанавливаем конечное значение 


if __name__ == "__main__":  # Если запускается как файл, то
    app = QApplication(sys.argv)  # Создаем приложение 
    ex = VideoApp()  # Создаем экземпляр класса VideoApp
    sys.exit(app.exec())  # Завершаем выполнение 
