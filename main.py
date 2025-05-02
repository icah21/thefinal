import time
import threading
from stepper_motor import StepperMotor
from ir_sensor import IRSensor
from servo import ServoController
import camera_dashboard  # This runs the GUI and detection

# Initialize IR sensor, stepper motor, and servo
ir_sensor = IRSensor(pin=17)
motor = StepperMotor(in1=18, in2=23, in3=24, in4=25)
servo = ServoController(pin=13)

# Shared state for stepper angle
current_angle = 0

def motor_thread_func():
    global current_angle
    while True:
        if ir_sensor.is_object_detected():
            print("[Main] Object detected by IR sensor.")
            current_angle = motor.go_to_angle(current_angle, 90)
            time.sleep(3)
            current_angle = motor.go_to_angle(current_angle, 180)
            time.sleep(2)
            current_angle = motor.go_to_angle(current_angle, 0)
            time.sleep(2)
        else:
            time.sleep(0.1)

def handle_sort_callback(detected_type):
    print(f"[Main] Sorting bean of type: {detected_type}")
    servo.rotate_to_sort(detected_type)

if __name__ == "__main__":
    try:
        # Assign camera callback for sorting
        camera_dashboard.sort_callback = handle_sort_callback

        # Start motor thread for IR-based activation
        motor_thread = threading.Thread(target=motor_thread_func)
        motor_thread.daemon = True
        motor_thread.start()

        # Run GUI/detection loop (runs in its own mainloop)
        camera_dashboard.root.mainloop()

    except KeyboardInterrupt:
        print("Exiting program.")
        servo.cleanup()
