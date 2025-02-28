import RPi.GPIO as GPIO
import time

# Define GPIO pins
DIR_PIN = 27  # Direction pin
STEP_PIN = 17  # Step pin

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)

# Set direction (high or low)
GPIO.output(DIR_PIN, GPIO.HIGH)  # Change to GPIO.LOW to reverse direction

# Function to move stepper motor
def move_stepper(steps, delay):
    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(delay)

try:
    while True:
        # Move 200 steps (adjust number of steps as needed)
        move_stepper(20, 0.001)  # 0.001s delay between steps (1ms)
        
        # Halt for 1 second
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    # Clean up GPIO settings before exiting
    GPIO.cleanup()
    print("GPIO cleanup done. Exiting.")
