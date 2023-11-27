import matplotlib.pyplot as plt
import matplotlib.patches as patches
import colorsys

def darken_rgb_color(hex_color, factor):
    """Darken an RGB color."""
    # Convert HEX to RGB
    r = int(hex_color[1:3], 16) / 255.0
    g = int(hex_color[3:5], 16) / 255.0
    b = int(hex_color[5:7], 16) / 255.0

    # Convert RGB to HSV
    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    # Darken the color
    v = max(0, min(1, v * factor))

    # Convert back to RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    # Convert RGB back to HEX
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))

def show_color_palette(base_color, factors):
    """Show a palette of colors based on the base color and list of factors."""
    fig, ax = plt.subplots(figsize=(8, 2))
    for i, factor in enumerate(factors):
        color = darken_rgb_color(base_color, factor)
        rect = patches.Rectangle((i, 0), 1, 1, linewidth=1, edgecolor='none', facecolor=color)
        ax.add_patch(rect)
        plt.text(i + 0.5, -0.2, color, ha='center', va='center')
    plt.xlim(0, len(factors))
    plt.ylim(-0.5, 1)
    plt.axis('off')
    plt.show()

# Example usage
# base_color = "#15a049"  # You can replace this with user input
factors = [1, 0.9, 0.8, 0.7, 0.6, 0.5]  # Different levels of darkness
#show_color_palette(base_color, factors)

def get_user_input():
    # Запрос исходного цвета у пользователя
    base_color = input("Введите HEX-код исходного цвета (например, #15a049): ")

    # Запрос уровней утемнения
    try:
        num_shades = int(input("Сколько уровней утемнения вы хотите увидеть? (например, 5): "))
    except ValueError:
        print("Пожалуйста, введите число.")
        return None, None

    return base_color, num_shades

def generate_shade_factors(num_shades):
    # Генерация списка коэффициентов для утемнения
    return [1 - (i / (num_shades + 1)) for i in range(1, num_shades + 1)]

# Основная функция
def main():
    base_color, num_shades = get_user_input()
    if base_color and num_shades:
        factors = generate_shade_factors(num_shades)
        show_color_palette(base_color, factors)

# Вызов основной функции
main()
