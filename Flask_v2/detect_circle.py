import cv2
import numpy as np
import sys

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python detect_circle.py <image_path>")
    sys.exit(1)

# Get the image path from the command-line argument
image_path = sys.argv[1]

# Read the image
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply GaussianBlur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Hough Circle Transform
circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    dp=1,
    minDist=50,
    param1=50,
    param2=30,
    minRadius=10,
    maxRadius=27
)

# If circles are found, draw them on the original image and get coordinates
if circles is not None:
    circles = np.uint16(np.around(circles))
    coordinates = []
    for i in circles[0, :]:
        # Coordinates of the center of the circle
        x, y = i[0], i[1]
        coordinates.append((x, y))
        # Draw the outer circle
        cv2.circle(image, (x, y), i[2], (0, 255, 0), 2)
        # Draw the center of the circle
        cv2.circle(image, (x, y), 2, (0, 0, 255), 3)

    # Print or use the coordinates
    print("Circle Coordinates (Pixels):", coordinates)

    # Convert pixel coordinates to real-world coordinates
    pixels_per_cm = 100  # Replace with your actual conversion factor
    real_world_coordinates = [(x / pixels_per_cm, y / pixels_per_cm) for x, y in coordinates]
    print("Circle Coordinates (cm):", real_world_coordinates)

    # Save the output image with detected circles
    output_path = 'output.jpeg'
    cv2.imwrite(output_path, image)
    print("Output image saved to:", output_path)

    # Display the result
    #cv2.imshow('Detected Circles', image)   #Uncomment this to display the output
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No circles found.")
