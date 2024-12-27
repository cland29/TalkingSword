import serial
import time

def read_serial_data(port, baud_rate, timeout=1):
    try:
        # Open the serial port
        with serial.Serial(port, baud_rate, timeout=timeout) as ser:
            print(f"Connected to {port} at {baud_rate} baud.")
            
            # Wait for the Arduino to initialize
            time.sleep(2)
            print("Ready to read data. Press Ctrl+C to stop.")
            
            while True:
                if ser.in_waiting > 0:
                    # Read a line of data from the serial port
                    line = ser.readline().decode('utf-8').strip()
                    print(f"Received: {line}")
    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nSerial communication terminated by user.")

if __name__ == "__main__":
    # Replace with your Arduino's port
    port = "COM5"  # Windows example
    # port = "/dev/ttyUSB0"  # Linux example
    # port = "/dev/tty.usbserial-1420"  # macOS example

    baud_rate = 115200  # Must match the Arduino's baud rate

    read_serial_data(port, baud_rate)
