import RPi.GPIO as GPIO
import time

# Define GPIO pins
DIR_PIN = 27  # Direction pin
STEP_PIN = 17  # Step pin

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)

# Function to move stepper motor
def move_stepper(steps, delay, direction):
    if direction == "clockwise":
        GPIO.output(DIR_PIN, GPIO.HIGH)
    elif direction == "counter-clockwise":
        GPIO.output(DIR_PIN, GPIO.LOW)
    else:
        return
    
    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(delay)

try:
    while True:
        # Move 40 steps clockwise
        move_stepper(40, 0.005, "clockwise")  # Adjust delay as needed
        
        time.sleep(1)
        
        # Move 40 steps counter-clockwise
        move_stepper(40, 0.005, "counter-clockwise")  # Adjust delay as needed
        
        time.sleep(1)
        
except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    # Clean up GPIO settings before exiting
    GPIO.cleanup()
    print("GPIO cleanup done. Exiting.")
