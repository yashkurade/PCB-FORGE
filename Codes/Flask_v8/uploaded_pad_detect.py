import cv2
import numpy as np
import sys
import os

# Function to convert pixel coordinates to inches
def pixels_to_inches(pixels, dpi=195):
    inches = pixels / dpi
    return inches

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python uploaded_pad_detect.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    filepath = os.path.join('/home/yash/PCB_FORGE/Flask_v8/uploads', filename)

    # Load the image
    image = cv2.imread(filepath)

    if image is None:
        print(f'Failed to load image {filename}')
        sys.exit(1)

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for green color in HSV space
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    # Create a mask for the green color
    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Find contours in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # List to store the coordinates of the green solder pads in inches
    solder_pads_coords_inches = []

    # Iterate through the contours
    for contour in contours:
        # Calculate the bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)

        # Calculate the center of the bounding box
        center_x = x + w / 2
        center_y = y + h / 2

        # Convert the center coordinates from pixels to inches
        center_x_inches = pixels_to_inches(center_x)
        center_y_inches = pixels_to_inches(center_y)

        # Add the coordinates to the list
        solder_pads_coords_inches.append((center_x_inches, center_y_inches))

        # Draw the bounding box and center point on the image (optional for visualization)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(image, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)

    # Save the processed image
    processed_image_path = os.path.join('static/processed', filename)
    cv2.imwrite(processed_image_path, image)

    # Save the coordinates to a text file
    coord_file_path = os.path.join('static/processed', f'{filename}_coordinates.txt')
    with open(coord_file_path, 'w') as file:
        for coord in solder_pads_coords_inches:
            file.write(f'X: {coord[0]:.4f} inches, Y: {coord[1]:.4f} inches\n')

    print(f'Processed image saved: {processed_image_path}')
    print(f'Coordinates saved: {coord_file_path}')
