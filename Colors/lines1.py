import cv2
import numpy as np

# Загрузим изображение манометра из файла
image_path = '/mnt/data/image.png'
image = cv2.imread(image_path)

# Конвертируем изображение в серый цвет для обработки
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Применим оператор Canny для обнаружения краев
edges = cv2.Canny(gray_image, threshold1=50, threshold2=150, apertureSize=3)

# Применим преобразование Хафа для обнаружения линий
lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=200)

# Отобразим результаты
output = image.copy()
if lines is not None:
    for rho, theta in lines[:, 0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(output, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Сохраним результаты на диск для вывода
output_path = '/mnt/data/manometer_detected_lines.png'
cv2.imwrite(output_path, output)

output_path
