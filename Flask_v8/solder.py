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

# Relay pins for heating element and solder wire feeder
HEATING_ELEMENT_PIN = 21
SOLDER_WIRE_FEEDER_PIN = 5

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

# Setup relay pins for heating element and solder wire feeder
GPIO.setup(HEATING_ELEMENT_PIN, GPIO.OUT)
GPIO.setup(SOLDER_WIRE_FEEDER_PIN, GPIO.OUT)

# Heating control variables
initial_heating_done = False
last_heating_time = 0

def toggle_heating_element(state):
    GPIO.output(HEATING_ELEMENT_PIN, GPIO.LOW if state else GPIO.HIGH)

def feed_solder_wire():
    GPIO.output(SOLDER_WIRE_FEEDER_PIN, GPIO.LOW)  # Activate solder wire feeder
    time.sleep(5)  # Feed solder wire for 5 seconds
    GPIO.output(SOLDER_WIRE_FEEDER_PIN, GPIO.HIGH)  # Stop solder wire feeder

def move_stepper(steps, direction, dir_pin, step_pin):
    GPIO.output(dir_pin, GPIO.HIGH if direction == "clockwise" else GPIO.LOW)
    
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
    for duty_cycle in range(7, 13):  # Gradually increase to move down
        servo.ChangeDutyCycle(duty_cycle)
        time.sleep(0.05)  # Adjust the sleep time for slower/faster movement
    time.sleep(0.5)  # Wait at the bottom position

def move_servo_up():
    for duty_cycle in range(12, 6, -1):  # Gradually decrease to move up
        servo.ChangeDutyCycle(duty_cycle)
        time.sleep(0.05)  # Adjust the sleep time for slower/faster movement
    time.sleep(0.5)  # Wait at the top position

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

    # Ensure the feeder is off before starting heating
    GPIO.output(SOLDER_WIRE_FEEDER_PIN, GPIO.HIGH)  # Feeder off

    # Initial heating for 120-seconds
    print("Heating element on for 120-seconds...")
    toggle_heating_element(True)
    time.sleep(120)  # 120 initial heating
    #toggle_heating_element(False)
    print("Initial heating done.")
    initial_heating_done = True
    last_heating_time = time.time()

    try:
        for coord in coordinates:
            # Check if we need to toggle the heating element (30-second on/off)
            #if initial_heating_done and time.time() - last_heating_time >= 30:
                #toggle_heating_element(True)
                #time.sleep(15)
                #toggle_heating_element(False)
                #last_heating_time = time.time()
            
            x, y = coord

            # Calculate the steps needed for X-axis movement
            target_position_x = x
            if target_position_x > MAX_MOVEMENT_LIMIT_X:
                print("Target position exceeds maximum X movement limit. Skipping.")
                continue

            x_steps = int((target_position_x - current_position_x) * STEPS_PER_INCH_X)
            direction_x = "counter-clockwise" if x_steps >= 0 else "clockwise"

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
            
            # Wait for 0.5 seconds before activating the servo and solder wire feeder
            time.sleep(0.5)
            
            # Feed solder wire before lowering the servo
            feed_solder_wire()
            time.sleep(1)

            # Activate servo motor to lower the soldering iron
            move_servo_down()
            time.sleep(8)

            # Feed solder wire again after lowering the servo
            #feed_solder_wire()
            #time.sleep(4)

            # Raise soldering iron
            move_servo_up()

    except KeyboardInterrupt:
        print("Interrupted by user")
    
    finally:
        # Stop the servo and clean up GPIO settings before exiting, but keep EN_PIN enabled
        servo.stop()
        
        # Disable the Enable pin for the stepper motor to avoid unwanted movement
        GPIO.output(EN_PIN, GPIO.HIGH)  # Disabling the motor driver
        
        # Clean up all GPIO settings except the EN_PIN
        GPIO.cleanup([DIR_PIN_X, STEP_PIN_X, DIR_PIN_Y, STEP_PIN_Y, SERVO_PIN, HEATING_ELEMENT_PIN, SOLDER_WIRE_FEEDER_PIN])
        
        print("GPIO cleanup done, EN_PIN remains active to prevent stepper movement. Exiting.")

if __name__ == '__main__':
    main()

