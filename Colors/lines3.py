# Let's apply contour analysis to detect the shapes of the needle and the dial on the manometer.

# First, find contours on the thresholded image
contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# We will draw all the contours on the image to see what has been detected
output_contours = image.copy()
cv2.drawContours(output_contours, contours, -1, (0, 255, 0), 3)

# Save and display the output image with detected contours
output_path_with_contours = '/mnt/data/manometer_detected_contours.png'
cv2.imwrite(output_path_with_contours, output_contours)

output_path_with_contours
