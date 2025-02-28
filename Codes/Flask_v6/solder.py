import RPi.GPIO as GPIO
import time

# Define GPIO pins for the stepper motor
DIR_PIN = 27  # Direction pin
STEP_PIN = 17  # Step pin
EN_PIN = 22   # Enable pin (optional, if using)

# Steps per inch (example value, adjust based on your calculation)
STEPS_PER_INCH = 200

# Maximum movement limit in inches
MAX_MOVEMENT_LIMIT = 1.5748

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(EN_PIN, GPIO.OUT)
GPIO.output(EN_PIN, GPIO.LOW)  # Enable the stepper motor driver

def move_stepper(steps, direction):
    if direction == "clockwise":
        GPIO.output(DIR_PIN, GPIO.HIGH)
    elif direction == "counter-clockwise":
        GPIO.output(DIR_PIN, GPIO.LOW)
    
    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(0.005)  # Adjust delay as needed
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(0.005)  # Adjust delay as needed

def read_coordinates(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y = line.strip().split(',')
            x = float(x.split(': ')[1].replace(' inches', ''))
            y = float(y.split(': ')[1].replace(' inches', ''))
            coordinates.append((x, y))
    return coordinates

def main():
    # Specify the path to your coordinates file
    file_path = '/home/yash/PCB_FORGE/Stepper_Motor/coordinates/coordinates_01.txt'
   
    # Read coordinates from file
    coordinates = read_coordinates(file_path)
    
    current_position = 0.0  # Start at the origin
    try:
        for coord in coordinates:
            x, y = coord
            # Calculate the steps needed for X-axis movement
            target_position = x
            if target_position > MAX_MOVEMENT_LIMIT:
                print("Target position exceeds maximum movement limit. Skipping.")
                continue

            x_steps = int((target_position - current_position) * STEPS_PER_INCH)
            direction = "clockwise" if x_steps >= 0 else "counter-clockwise"
            
            # Move stepper motor for X-axis
            move_stepper(abs(x_steps), direction)
            current_position = target_position  # Update the current position
            time.sleep(1)  # Pause for 1 second between movements
            
            # Future implementation: Move stepper motor for Y-axis
            # y_steps = int(y * STEPS_PER_INCH)
            # direction = "clockwise" if y >= 0 else "counter-clockwise"
            # move_stepper(abs(y_steps), direction)
            # time.sleep(1)  # Pause for 1 second between movements
            
            # Future implementation: Activate Z-axis servo motor to release for 3 seconds
            # GPIO.output(Z_SERVO_PIN, HIGH)
            # time.sleep(3)
            # GPIO.output(Z_SERVO_PIN, LOW)
            
    except KeyboardInterrupt:
        print("Interrupted by user")
    
    finally:
        # Clean up GPIO settings before exiting
        GPIO.cleanup()
        print("GPIO cleanup done. Exiting.")

if __name__ == '__main__':
    main()
