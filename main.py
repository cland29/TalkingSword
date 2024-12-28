import serial
import time
import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import QTimer

serial_port = "COM8"  # Windows example
    # port = "/dev/ttyUSB0"  # Linux example
    # port = "/dev/tty.usbserial-1420"  # macOS example

serial_baud_rate = 115200  # Must match the Arduino's baud rate
serial_timeout = 1

action_types = ["idle", "ready", "start-run", "on-ground", "running", "swing-hit", "swing-miss", "stab-hit", "stab-miss", "high-cross", "side-wrap-hit", "side-wrap-miss", "legsweep-hit", "legsweep-miss"]
action = "unclassified"

global_output_file = 0
global_app = 0


def changeAction(actionType):
    global action
    action = actionType

def establish_serial_connection(port, baud_rate, timeout=1):
    output_file = open("myfile.txt", "w")
    
    
    output_file.write("timestamp, gyroX, gyroY, gyroZ, Accel_1_X, Accel_1_Y, Accel_1_Z, Accel_2_X, Accel_2_Y, Accel_2_Z, classification\n")

    try:
        # Open the serial port
        serial_connection = serial.Serial(port, baud_rate, timeout=serial_timeout)
        print(f"Connected to {port} at {baud_rate} baud.")
            
        # Wait for the Arduino to initialize
        time.sleep(2)
        print("Ready to read data. Press Ctrl+C to stop.")
    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nSerial communication terminated by user.")
    return serial_connection, output_file

def close_app():
    global_output_file.close()
    sys.exit()

def create_window_with_buttons():
    serial_connection, output_file = establish_serial_connection(serial_port, serial_baud_rate)
    global global_output_file
    global_output_file = output_file
    global global_app
    app = QApplication(sys.argv)
    global_app = app
    window = QWidget()
    window.setWindowTitle("Button Window")

    # Layout for the buttons
    layout = QVBoxLayout()

    # Create and add buttons to the layout
    for i in range(len(action_types)):
        button = QPushButton(f"{action_types[i]}")
        button.pressed.connect(lambda b=action_types[i]: changeAction(b))
        button.released.connect(lambda b="unclassified": changeAction(b))
        layout.addWidget(button)

    button = QPushButton("End Recording Session")
    button.clicked.connect(lambda a=app: close_app())
    layout.addWidget(button)

    window.setLayout(layout)

    timer = QTimer()
    timer.timeout.connect(lambda conn=serial_connection, file=output_file: read_serial_data(conn, file))
    timer.start(10)

    window.show()

    sys.exit(app.exec_())

# def read_serial_data(port, baud_rate, timeout=1):
def read_serial_data(conn, file):
    if conn.in_waiting > 0:
        # Read a line of data from the serial port
        line = conn.readline().decode('utf-8').strip()
        # data = line.split(",")
        print(f"Received: {line + ", " + action}")
        file.write(line + ", " + action + "\n")

if __name__ == "__main__":
    # Replace with your Arduino's port
    
    create_window_with_buttons()
    # read_serial_data(port, baud_rate)
    # read_serial_data()
