import time
import picamera

# Create a PiCamera object
camera = picamera.PiCamera()

try:
    # Set camera resolution to maximum
    camera.resolution = (1944, 1944)  # Maximum resolution for Raspberry Pi Camera v1.3

    # Capture an image at highest quality
    camera.capture('image.jpg', quality=100)

    print("Image captured successfully!")

finally:
    # Close the PiCamera
    camera.close()
