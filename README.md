# PyQt6_Video_Frames_Cutting
Video Frames Cutting for AI Projects by PyQt6

![image](https://github.com/DmPanf/PyQt6_Video_Frames_Cutting/assets/99917230/b60ddaf1-5be1-418d-a113-fd90bcf35ecf)

## def darken_rgb_color Description:


This code defines a function darken_rgb_color that takes a HEX color value (e.g., #15a049) and an optional factor (defaulted to 0.8) as its inputs. It performs the following steps:

1. Convert the HEX value into its RGB components.
2. Convert the RGB values to HSV (Hue, Saturation, Value) format using the colorsys library.
3. Multiply the value (brightness) component of the HSV with the given factor to darken the color.
4. Convert the modified HSV values back to RGB format.
5. Convert the RGB values back to HEX format.
. Return the darkened HEX color.
