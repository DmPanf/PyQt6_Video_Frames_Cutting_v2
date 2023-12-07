# Let's reprocess the image with an additional step of thresholding to convert it to black and white before edge detection.
# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to smooth out the edges
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Convert the image to black and white with a simple threshold
_, binary_image = cv2.threshold(blurred_image, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Apply Canny edge detection using the computed threshold
edges = cv2.Canny(binary_image, threshold1=50, threshold2=150, apertureSize=3)

# Use HoughLines to detect lines in the edge-detected image
lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

# Draw the lines on the original image
output = image.copy()
if lines is not None:
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Save and display the output image with detected lines
output_path_with_threshold = '/mnt/data/manometer_detected_lines_with_threshold.png'
cv2.imwrite(output_path_with_threshold, output)

output_path_with_threshold
