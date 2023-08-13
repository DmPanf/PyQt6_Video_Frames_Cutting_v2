# Если надо сделать цвет темнее, необходимо уменьшить его яркость. 
# Один из способов — использовать цветовые пространства, такие как 
# HSL (Hue, Saturation, Lightness) или HSV (Hue, Saturation, Value).
# Необходимо изменить фактор (0.7) на другое значение меньше 1, чтобы сделать цвет темнее!
import colorsys

def darken_rgb_color(hex_color, factor=0.8):
    # Конвертация HEX в RGB
    r = int(hex_color[1:3], 16) / 255.0
    g = int(hex_color[3:5], 16) / 255.0
    b = int(hex_color[5:7], 16) / 255.0

    # Конвертация RGB в HSV
    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    # Уменьшаем яркость
    v = max(0, min(1, v * factor))

    # Конвертируем обратно в RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    # Конвертация RGB обратно в HEX
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))

color = "#15a049"
darker_color = darken_rgb_color(color, 0.7)
print(darker_color)
