## PyQt6 Video Frames Cutting Project 🎥✂️

### Introduction 📌
Welcome to the 'PyQt6 Video Frames Cutting' project! This repository contains a user-friendly application built with PyQt6, designed for cutting and editing video frames. Dive into the realm of video editing with our intuitive GUI!

### Description 🖼️
`darken_rgb_color` is a handy function within this project that allows users to darken HEX color values. It's perfect for UI customization and enhancing the visual aspects of your application.

### Features 🌟
- **Video Frame Editing**: Easily cut and edit frames from your videos.
- **Color Customization**: Use `darken_rgb_color` to adjust UI colors.
- **PyQt6 Integration**: Experience a smooth and modern GUI.
- **OpenCV for Video Processing**: Leverage the power of OpenCV for efficient video handling.

### Prerequisites 📋
- Python 3.6+
- Git

### Installation 🚀
1. **Clone the Repository**:
   ```
   git clone https://github.com/DmPanf/PyQt6_Video_Frames_Cutting_v2.git
   ```

2. **Navigate to the Project Directory**:
   ```
   cd PyQt6_Video_Frames_Cutting_v2
   ```

3. **Set Up the Virtual Environment**:
   ```
   python -m venv venv
   ```

4. **Activate the Virtual Environment**:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```
     source venv/bin/activate
     ```

5. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

### Usage 🖥️
Run the application by executing the main script:
```
python main.py
```
Enjoy cutting and editing your video frames with ease!

### Contribution 🤝
Contributions to enhance this project are highly encouraged. Feel free to fork the repo, make your changes, and submit a pull request!

### License 📜
This project is licensed under the [MIT License](LICENSE).

### Contact 📬
For any inquiries or contributions, please contact [project-email].

---

## Examples

![image](https://github.com/DmPanf/PyQt6_Video_Frames_Cutting/assets/99917230/b60ddaf1-5be1-418d-a113-fd90bcf35ecf)

## def darken_rgb_color Description:


This code defines a function darken_rgb_color that takes a HEX color value (e.g., #15a049) and an optional factor (defaulted to 0.8) as its inputs. It performs the following steps:

1. Convert the HEX value into its RGB components.
2. Convert the RGB values to HSV (Hue, Saturation, Value) format using the colorsys library.
3. Multiply the value (brightness) component of the HSV with the given factor to darken the color.
4. Convert the modified HSV values back to RGB format.
5. Convert the RGB values back to HEX format.
6. Return the darkened HEX color.

## 

---
