import cv2
import numpy as np
import sys
import os

def template_matching(reference_img_paths, target_img_path):
    # Load target image
    target_img = cv2.imread(target_img_path)  # Load as color

    # Check if target image is loaded successfully
    if target_img is None:
        print("Error: Couldn't load target image.")
        return

    # Convert target image to grayscale for template matching
    target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)

    # Define threshold
    threshold = 0.6

    # Loop through each reference image
    for reference_img_path in reference_img_paths:
        # Load reference image
        reference_img = cv2.imread(reference_img_path, cv2.IMREAD_GRAYSCALE)  # Load as grayscale

        # Check if reference image is loaded successfully
        if reference_img is None:
            print("Error: Couldn't load reference image:", reference_img_path)
            continue

        # Get dimensions of the reference image
        height, width = reference_img.shape

        # Apply template matching
        res = cv2.matchTemplate(target_gray, reference_img, cv2.TM_CCOEFF_NORMED)

        # Find locations where the correlation coefficient is greater than threshold
        loc = np.where(res >= threshold)

        # Draw rectangles around the matched regions
        for pt in zip(*loc[::-1]):
            cv2.rectangle(target_img, pt, (pt[0] + width, pt[1] + height), (0, 255, 0), 2)

    # Define the output directory and filename
    output_dir = '/home/yash/PCB_FORGE/Flask_v7/outputs'
    os.makedirs(output_dir, exist_ok=True)
    processed_image_path = os.path.join(output_dir, os.path.basename(target_img_path))

    # Save the output image with rectangles drawn
    cv2.imwrite(processed_image_path, target_img)

    # Save the result
    print(f'Rectangle detection completed! Processed image saved: {processed_image_path}')

    # Display result
    cv2.imshow('Matched Result', target_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    target_image_path = sys.argv[1]
    reference_image_paths = ['solderpad_2.png', 'solderpad_3.png']
    template_matching(reference_image_paths, target_image_path)
