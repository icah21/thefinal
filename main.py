import time
import threading
from stepper_motor import StepperMotor
from ir_sensor import IRSensor
from servo import ServoController
from camera_dashboard import camera_dashboard

# Initialize IR sensor, stepper motor, and servo
ir_sensor = IRSensor(pin=17)
motor = StepperMotor(in1=18, in2=23, in3=24, in4=25)
servo = ServoController(pin=13)  # Update pin if needed

# Shared state
current_angle = 0

def motor_thread_func():
    global current_angle
    while True:
        if ir_sensor.is_object_detected():
            print("Object detected!")

            # Stepper movement example (optional for you)
            current_angle = motor.go_to_angle(current_angle, 90)
            time.sleep(3)
            current_angle = motor.go_to_angle(current_angle, 180)
            time.sleep(2)
            current_angle = motor.go_to_angle(current_angle, 0)
            time.sleep(2)
        else:
            time.sleep(0.1)

def sort_bean_callback(bean_type):
    print(f"Sorting bean type: {bean_type}")
    servo.rotate_to_sort(bean_type)

try:
    # Link camera to servo
    camera_dashboard.sort_callback = sort_bean_callback

    # Start motor thread (optional if you only want camera and servo)
    motor_thread = threading.Thread(target=motor_thread_func)
    motor_thread.daemon = True
    motor_thread.start()
except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
