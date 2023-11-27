Для создания интерактивного скрипта подбора цвета на Python, мы можем использовать ваш код как основу и расширить его функционал. Мы добавим возможность выбора исходного цвета пользователем, а также предоставим несколько вариантов утемнения этого цвета. Для визуализации результатов будем использовать библиотеку `matplotlib`.

Вот как будет выглядеть наш план:
1. Пользователь вводит HEX-код цвета.
2. Программа отображает исходный цвет.
3. Затем программа предлагает пользователю выбрать степень утемнения.
4. Программа отображает полосу с разными вариантами утемнения исходного цвета.
5. Показывает их HEX-коды для каждого варианта.

![image](https://github.com/DmPanf/PyQt6_Video_Frames_Cutting_v2/assets/99917230/4934aad5-565a-4391-9b96-7569c9212616)

Для работы скрипта потребуется установить библиотеку `matplotlib`. Если она еще не установлена, вы можете сделать это с помощью команды `pip install matplotlib`.

Вот интерактивный скрипт, основанный на вашем коде, для подбора цвета онлайн. Сначала он отображает полоску с исходным цветом и его различными уровнями утемнения. На каждом шаге отображается HEX-код соответствующего цвета.

```python
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
base_color = "#15a049"  # You can replace this with user input
factors = [1, 0.9, 0.8, 0.7, 0.6, 0.5]  # Different levels of darkness
show_color_palette(base_color, factors)

```

В данном примере мы использовали исходный цвет `#15a049` и показали его варианты с утемнением на 10%, 20%, 30%, 40%, и 50%. Вы можете настроить этот скрипт, чтобы принимать входные данные от пользователя и отображать нужные уровни утемнения.

Для работы этого скрипта вам потребуется библиотека `matplotlib`. Если она еще не установлена, вы можете установить ее, используя команду `pip install matplotlib`. 

Для взаимодействия с пользователем в реальном времени вы можете запустить этот скрипт в среде, которая поддерживает интерактивный ввод, например, в Jupyter Notebook.
