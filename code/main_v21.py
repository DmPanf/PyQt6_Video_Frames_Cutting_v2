import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, 
                             QLabel, QSlider, QLineEdit, QPushButton, QFileDialog)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QPixmap, QGuiApplication, QImage
import cv2
import os
import configparser


def read_config():
    config = configparser.ConfigParser()
    if not os.path.exists('config.ini'):
        raise FileNotFoundError("config.ini not found!")
    
    config.read('config.ini')

    image_path = config.get('CONFIG', 'basic_image_path', fallback="./images/00.jpg")
    frames_dir = config.get('CONFIG', 'default_frames_dir', fallback="./OUTPUT/")
    temp_name = config.get('CONFIG', 'temp_name', fallback="temp")
    frames_number = config.get('CONFIG', 'frames_number', fallback="5")
    win_title = config.get('CONFIG', 'win_title', fallback="Video")
    return image_path, frames_dir, temp_name, frames_number, win_title


class VideoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.video_path = None
        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.play_video)

        # Загрузка конфигурации и установка начального изображения
        self.image_path, self.frames_dir, self.temp_name, self.frames_number, self.win_title = read_config()
        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()

        # Создаем QLabel для отображения изображения
        self.image_label = QLabel(self)
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap.scaled(640, 400, Qt.AspectRatioMode.KeepAspectRatio))  # 640x400 - примерные размеры

        layout.addWidget(self.image_label)

        # Video Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.valueChanged.connect(self.slider_moved) # обработчик событий для события valueChanged слайдера  
        layout.addWidget(self.slider)
        # Connect the slider valueChanged signal to the set_video_position function
        self.slider.valueChanged.connect(self.set_video_position)
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
                margin: -8px 0; /* размер ползунка по отношению к треку */
                border-radius: 12px; /* закругленные углы ползунка */
            }
            QSlider {
                border: 2px solid #0c0c0c; /* рамка вокруг всего слайдера */
                padding: 3px;
            }
        """)


        # Info Panel
        info_layout = QHBoxLayout()
        
        self.start_label = QLineEdit("1")
        self.current_frame_label = QLabel(" 0")  # Начальное значение
        self.end_label = QLineEdit("30")
        self.skip_frames = QLineEdit(self.frames_number)
        self.name_label = QLabel("Template:")
        self.output_name = QLineEdit(self.temp_name)

        # Устанавливаем стили для QLineEdit:
        font_style = "background-color: darkgray; font-size: 18px; color: darkblue; font-weight: bold;"
        self.start_label.setFixedWidth(65)
        self.start_label.setStyleSheet(font_style)
        self.current_frame_label.setFixedWidth(65)
        self.current_frame_label.setStyleSheet("font-size: 18px; font-weight: bold;")
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
        info_layout.addWidget(self.current_frame_label)
        info_layout.addWidget(self.end_label)
        info_layout.addWidget(self.skip_frames)
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.output_name)
        
        layout.addLayout(info_layout)

        # Button Panel
        btn_layout = QHBoxLayout()
        
        self.load_btn = QPushButton("VIDEO LOAD")
        self.play_btn = QPushButton("PLAY/STOP")
        self.cut_btn = QPushButton("CUT and SAVE")
        self.return_btn = QPushButton("RESET")

        buttons = [self.load_btn, self.play_btn, self.cut_btn, self.return_btn]
        for button in buttons:
            button.setFixedHeight(42)  # Устанавливаем высоту
            button.setStyleSheet("""
                QPushButton {
                    background-color: #15a049;
                    color: white;
                    border-radius: 12px;
                }
                QPushButton:hover {
                    background-color: #0e6f33;
                }
            """)

        self.load_btn.clicked.connect(self.load_video)
        self.play_btn.clicked.connect(self.toggle_play)
        #self.cut_btn.clicked.connect(self.cut_frames)
        self.cut_btn.clicked.connect(self.confirm_action)  # будет представлено диалоговое окно с подтверждением
        self.return_btn.clicked.connect(self.return_values)

        btn_layout.addWidget(self.load_btn)
        btn_layout.addWidget(self.play_btn)
        btn_layout.addWidget(self.cut_btn)
        btn_layout.addWidget(self.return_btn)
        
        layout.addLayout(btn_layout)

        # Info Widget 
        self.info_widget = self.create_info_widget()
        self.info_widget.setStyleSheet("background-color: #464646;")
        layout.addWidget(self.info_widget)
        layout.addSpacing(10)

        self.setLayout(layout)
        self.setWindowTitle(self.win_title)
        self.update_image()
        self.center()
        self.show()


    def center(self):
        screen = QGuiApplication.screens()[0]
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        window_geometry.moveTop(window_geometry.top() - 100)
        self.move(window_geometry.topLeft())


    def update_image(self):
        pixmap = QPixmap(self.image_path)
        # Если ширина видео меньше 650, фиксируем ширину в 650
        new_width = max(self.width() + 20, 650)
        # new_width = self.width()
        aspect_ratio = pixmap.width() / pixmap.height()
        new_height = int(new_width / aspect_ratio)
        scaled_pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)
        self.center()


    def resizeEvent(self, event):
        super().resizeEvent(event)


    def load_video(self):
        self.video_path, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.webm)")
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            ret, frame = self.cap.read()
            if ret:
                self.show_frame_on_label(frame)

            self.slider.setMaximum(int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)))
            # при загрузке видео показывается номер последнего кадра:
            self.end_label.setText(str(int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))))
            self.update_info_widget() # обновляем информационный виджет
            self.update_slider_position()
            self.start_label.setText("1")

            # Устанавливаем имя файла для сохранения 
            base_name = os.path.basename(self.video_path)
            video_name_without_extension = os.path.splitext(base_name)[0]
            self.output_name.setText(video_name_without_extension)

            # Ограничение размеров приложения максимальными высотой и шириной экрана монитора
            screen_size = QApplication.primaryScreen().size()
            screen_width = screen_size.width() - 20
            screen_height = screen_size.height() - 80
            self.setMaximumSize(QSize(screen_width, screen_height))
            self.setMinimumSize(QSize(640, 600))
            self.center()


    def show_frame_on_label(self, frame):
        # После выбора видео загрузка первого кадра и подгон размера окна
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.AspectRatioMode.KeepAspectRatio))

        # Устанавливаем высоту и ширину видео
        height_of_image = pixmap.height()
        height_of_other_widgets = 235
        total_height = height_of_image + height_of_other_widgets
        self.setFixedHeight(total_height)
        width_of_image = max(pixmap.width() + 20, 650) # Устанавливаем ширину в 650, если она меньше
        self.setFixedWidth(width_of_image)

        # Обновляем информационный виджет
        self.setWindowTitle(f'{self.win_title} [{os.path.basename(self.video_path)}]')


    def toggle_play(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(30)

    def play_video(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                self.image_label.setPixmap(pixmap)
                self.update_slider_position()
            else:
                self.timer.stop()
        else:
            self.timer.stop()
            self.show_error("Ошибка воспроизведения", "Видео не загружено или произошла ошибка при его чтении.")
            #pass


    def update_slider_position(self):
        if self.cap:
            self.slider.setValue(int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)))
            # при проигрывании видео и при перемещении ползунка слайдера:
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.current_frame_label.setText(f' {current_frame}')

    def slider_moved(self):
        # когда будет двигаться слайдер, метка с номером текущего кадра будет автоматически обновляться
        if self.cap:
            # Устанавливаем позицию видео в соответствии с положением слайдера
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.slider.value())
            # Считаем текущий кадр из видео
            ret, frame = self.cap.read()
            if ret:
                # Преобразовываем кадр в QPixmap и устанавливаем его для QLabel
                pixmap = self.frame_to_pixmap(frame)
                self.image_label.setPixmap(pixmap)

            # Обновляем метку с номером текущего кадра
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.current_frame_label.setText(f' {current_frame}')
        else:
            #self.timer.stop()
            #self.show_error("Ошибка воспроизведения", "Видео не загружено или произошла ошибка при его чтении.")
            pass


    def frame_to_pixmap(self, frame):
        # Функция преобразует кадр из формата OpenCV (BGR) в изображение QPixmap, которое можно отображать в QLabel
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image)
        return pixmap


    def set_video_position(self, position):
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)

    def get_video_info(self):
        if not self.cap:
            return {}
        
        # Получение параметров видео с помощью OpenCV
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        codec = int(self.cap.get(cv2.CAP_PROP_FOURCC))
        codec_name = "".join([chr((codec >> 8 * i) & 0xFF) for i in range(4)])
        
        # Получение размера файла
        file_size = os.path.getsize(self.video_path)  # в байтах
        file_size_mb = file_size / (1024 * 1024)  # в мегабайтах

        info = {
            "\n ⚙️ PATH": self.video_path,
            "⚙️ SIZE": f"[{file_size_mb:.2f} MB]",
            "⚙️ CODEC": codec_name,
            "\n ⚙️ DURATION": f"[{duration:.2f} s]",
            "⚙️ FPS": f"[{fps}]",
            "⚙️ VIDEO": f"[{width} X {height}]",
            "⚙️ FRAMES": f"[{frame_count}]"
        }
        return info

    def create_info_widget(self):
        # font_style = "background-color: darkgray; font-size: 18px; color: darkblue; font-weight: bold;"
        # label_style = "background-color: darkgray;  font-size: 18px; color: darkblue; padding: 10px; border: 1px solid #15a049; font-weight: bold;"
        label_style = "background-color: darkgray; padding: 10px; border: 1px solid #15a049;"
        info_label = QLabel(self)
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        info_label.setStyleSheet(label_style)
        return info_label


    def update_info_widget(self):
        info = self.get_video_info()
        info_text = " ".join([f"{key}: {value}" for key, value in info.items()])
        self.info_widget.setText(info_text)


    def cut_frames(self):
        if not hasattr(self, 'video_path') or not self.video_path:
            self.show_error("Видео не загружено!", "Пожалуйста, загрузите видео перед выделением кадров.")
            return

        start_frame = self.get_label_value(self.start_label)
        end_frame = self.get_label_value(self.end_label)
        skip_frames = self.get_label_value(self.skip_frames)

        if not all(isinstance(i, int) and i >= 0 for i in [start_frame, end_frame, skip_frames]):
            self.show_error("Неверное значение!", "Убедитесь, что значения начала, конца и пропуска кадров являются положительными целыми числами.")
            return

        if start_frame >= end_frame:
            self.show_error("Неверный диапазон!", "Конечный кадр должен быть больше начального.")
            return

        cap = cv2.VideoCapture(self.video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if end_frame > frame_count:
            self.show_error("Неверное значение!", "Конечный кадр больше количества кадров в видео.")
            return

        base_name = os.path.basename(self.video_path)  # Получаем имя файла
        video_name_without_extension = os.path.splitext(base_name)[0] # Убираем расширение
        # Если output_name задан, используем его вместо video_name_without_extension
        output_name_value = self.output_name.text().strip() # вместо video_name_without_extension
        if output_name_value:  # Если output_name задан
            video_name_without_extension = output_name_value # Убираем расширение
        else:
            self.output_name.setText(video_name_without_extension) # Обновляем поле для Шаблона

        save_path = os.path.join(self.frames_dir, video_name_without_extension)

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        count = 0
        for i in range(start_frame, end_frame, skip_frames):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                # frame_name = f"{video_name_without_extension}_{count:03}.jpg"
                frame_count = count * skip_frames + start_frame
                frame_name = f"{video_name_without_extension}_{frame_count:04d}.png"  # Формируем имя файла с четырехзначным номером кадра
                frame_path = os.path.join(save_path, frame_name)
                cv2.imwrite(frame_path, frame)
                count += 1

        cap.release()
        self.show_info(f"Фреймы в количестве {count} штук успешно сохранены в папке {save_path}!")

    def get_label_value(self, label):
        try:
            return int(label.text().strip())
        except ValueError:
            return None

    def show_error(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def show_info(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Информация")
        msg_box.setText(message)
        msg_box.exec()


    def confirm_action(self):
        message = f"Начальный кадр: {self.start_label.text()}\n" \
                f"Конечный кадр: {self.end_label.text()}\n" \
                f"Пропускакть: {self.skip_frames.text()} кадр(ов)\n" \
                f"Шаблон для сохранения: {self.output_name.text()}"

        reply = QMessageBox.question(self, 'Подтвердить действие',
                                    message, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Ok:
            self.cut_frames()
        else:
            # Если необходимо, можно добавить дополнительные действия при отмене.
            pass


    def return_values(self):
        self.start_label.setText("1")
        self.skip_frames.setText(self.frames_number)
        self.output_name.setText(self.temp_name)
        self.slider.setValue(0)
        if self.cap is not None:
            self.end_label.setText(str(int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))))
        else:
            # Обработка ошибки или установка дефолтного значения для self.end_label
            self.end_label.setText("30")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = VideoApp()
    sys.exit(app.exec())
