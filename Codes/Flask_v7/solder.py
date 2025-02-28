import RPi.GPIO as GPIO
import time
import sys
import os

# Define GPIO pins for the stepper motor
DIR_PIN_X = 26  # Direction pin for X-axis
STEP_PIN_X = 17  # Step pin for X-axis
DIR_PIN_Y = 23  # Direction pin for Y-axis
STEP_PIN_Y = 24  # Step pin for Y-axis
EN_PIN = 22   # Enable pin (optional, if using)

# Servo motor pin
SERVO_PIN = 18

# Steps per inch (example value, adjust based on your calculation)
STEPS_PER_INCH_X = 180
STEPS_PER_INCH_Y = 172

# Maximum movement limit in inches for both axes
MAX_MOVEMENT_LIMIT_X = 1.5748
MAX_MOVEMENT_LIMIT_Y = 1.5748

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN_X, GPIO.OUT)
GPIO.setup(STEP_PIN_X, GPIO.OUT)
GPIO.setup(DIR_PIN_Y, GPIO.OUT)
GPIO.setup(STEP_PIN_Y, GPIO.OUT)
GPIO.setup(EN_PIN, GPIO.OUT)
GPIO.output(EN_PIN, GPIO.LOW)  # Enable the stepper motor driver

GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz PWM frequency for servo motor
servo.start(0)  # Start with servo off

def move_stepper(steps, direction, dir_pin, step_pin):
    if direction == "clockwise":
        GPIO.output(dir_pin, GPIO.HIGH)
    elif direction == "counter-clockwise":
        GPIO.output(dir_pin, GPIO.LOW)
    
    for _ in range(steps):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(0.005)  # Adjust delay as needed
        GPIO.output(step_pin, GPIO.LOW)
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

def move_servo_down():
    servo.ChangeDutyCycle(7)  # Adjust as needed for your servo to move down
    time.sleep(3)  # Wait for 3 seconds

def move_servo_up():
    servo.ChangeDutyCycle(2)  # Adjust as needed for your servo to move up
    time.sleep(0.5)

def main():
    # Get the file path from command-line arguments
    if len(sys.argv) < 2:
        print("Error: No coordinates file path provided.")
        sys.exit(1)
    
    coordinates_path = sys.argv[1]

    if not os.path.isfile(coordinates_path):
        print(f"Error: The file {coordinates_path} does not exist.")
        sys.exit(1)

    # Read coordinates from file
    coordinates = read_coordinates(coordinates_path)
    
    current_position_x = 0.0  # Start at the origin for X-axis
    current_position_y = 0.0  # Start at the origin for Y-axis
    
    try:
        for coord in coordinates:
            x, y = coord

            # Calculate the steps needed for X-axis movement
            target_position_x = x
            if target_position_x > MAX_MOVEMENT_LIMIT_X:
                print("Target position exceeds maximum X movement limit. Skipping.")
                continue

            x_steps = int((target_position_x - current_position_x) * STEPS_PER_INCH_X)
            if x_steps >= 0:
                direction_x = "clockwise"
            else:
                direction_x = "counter-clockwise"

            # Move stepper motor for X-axis
            move_stepper(abs(x_steps), direction_x, DIR_PIN_X, STEP_PIN_X)
            current_position_x = target_position_x  # Update the current position

            # Wait for 0.5 seconds before moving the Y-axis
            time.sleep(0.5)
            
            # Calculate the steps needed for Y-axis movement
            target_position_y = y
            if target_position_y > MAX_MOVEMENT_LIMIT_Y:
                print("Target position exceeds maximum Y movement limit. Skipping.")
                continue

            y_steps = int((target_position_y - current_position_y) * STEPS_PER_INCH_Y)
            direction_y = "clockwise" if y_steps >= 0 else "counter-clockwise"

            # Move stepper motor for Y-axis
            move_stepper(abs(y_steps), direction_y, DIR_PIN_Y, STEP_PIN_Y)
            current_position_y = target_position_y  # Update the current position
            
            # Wait for 0.5 seconds before activating the servo
            time.sleep(0.5)
            
            # Activate servo motor to lower and raise soldering iron
            move_servo_down()
            move_servo_up()
            
    except KeyboardInterrupt:
        print("Interrupted by user")
    
    finally:
        # Stop the servo and clean up GPIO settings before exiting, but keep EN_PIN enabled
        servo.stop()
        
        # Disable the Enable pin for the stepper motor to avoid unwanted movement
        GPIO.output(EN_PIN, GPIO.HIGH)  # Disabling the motor driver
        
        # Clean up all GPIO settings except the EN_PIN
        GPIO.cleanup([DIR_PIN_X, STEP_PIN_X, DIR_PIN_Y, STEP_PIN_Y, SERVO_PIN])
        
        print("GPIO cleanup done, EN_PIN remains active to prevent stepper movement. Exiting.")

if __name__ == '__main__':
    main()
