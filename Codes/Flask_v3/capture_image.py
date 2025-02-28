# capture_image.py

import os
import picamera
import time
import sys

def capture_image(image_name):
    # Get the directory of the Flask application
    app_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(app_dir, 'inputs')
    image_path = os.path.join(output_dir, f'{image_name}.jpg')  # Use the provided image name

    with picamera.PiCamera() as camera:
        camera.resolution = (1944, 1944)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture(image_path)

if __name__ == '__main__':
    # Get the image name from command line argument
    image_name = sys.argv[1]
    capture_image(image_name)

