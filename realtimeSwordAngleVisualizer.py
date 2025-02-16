import serial
import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

serial_port = "COM5"  # Replace with your port
serial_baud_rate = 115200  # Match Arduino baud rate
serial_timeout = 1

gyro_angles = [0, 0, 0]  # [X, Y, Z] angles in degrees
offsets = [0, 0, 0]  # Offsets for each axis

class StickVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Stick Visualizer")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

        self.serial_connection = self.establish_serial_connection()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_angles)
        self.timer.start(10)

    def init_ui(self):
        layout = QVBoxLayout()

        # Canvas for drawing
        self.canvas = QWidget(self)
        self.canvas.setFixedSize(600, 400)
        layout.addWidget(self.canvas)

        # Real-time gyroscope value labels
        self.gyro_labels = []
        gyro_layout = QHBoxLayout()
        for i, axis in enumerate(["X", "Y", "Z"]):
            label = QLabel(f"{axis}: 0.00")
            label.setAlignment(Qt.AlignCenter)
            gyro_layout.addWidget(label)
            self.gyro_labels.append(label)

        layout.addLayout(gyro_layout)

        # Offset controls
        offset_layout = QHBoxLayout()
        self.offset_inputs = []
        for i, axis in enumerate(["X", "Y", "Z"]):
            label = QLabel(f"{axis} Offset:")
            offset_input = QLineEdit("0")
            offset_input.setFixedWidth(50)
            offset_input.textChanged.connect(lambda val, idx=i: self.update_offset(val, idx))

            offset_layout.addWidget(label)
            offset_layout.addWidget(offset_input)
            self.offset_inputs.append(offset_input)

        layout.addLayout(offset_layout)

        self.setLayout(layout)

    def establish_serial_connection(self):
        try:
            serial_connection = serial.Serial(serial_port, serial_baud_rate, timeout=serial_timeout)
            print(f"Connected to {serial_port} at {serial_baud_rate} baud.")
            return serial_connection
        except serial.SerialException as e:
            print(f"Error: {e}")
            sys.exit(1)

    def update_offset(self, value, index):
        try:
            offsets[index] = float(value)
        except ValueError:
            offsets[index] = 0

    def update_angles(self):
        if self.serial_connection.in_waiting > 0:
            try:
                line = self.serial_connection.readline().decode('utf-8').strip()
                angles = [float(x) for x in line.split(",")]
                global gyro_angles
                gyro_angles = [angles[i] + offsets[i-1] for i in range(1, 4)]

                # Update gyroscope value labels
                for i, label in enumerate(self.gyro_labels):
                    label.setText(f"{['X', 'Y', 'Z'][i]}: {gyro_angles[i]:.2f}")

                self.repaint()
            except (ValueError, IndexError):
                pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 2))

        # Center of the canvas
        center_x, center_y = self.canvas.width() // 2, self.canvas.height() // 2

        # Stick parameters
        stick_length = 1000

        # Calculate stick end coordinates based on angles
        angle_x = math.radians(gyro_angles[0])
        angle_y = math.radians(gyro_angles[1])

        # 3D rotation (simple perspective projection)
        end_x = center_x + stick_length * math.sin(angle_y)
        end_y = center_y - stick_length * math.sin(angle_x)

        # Draw the stick
        painter.drawLine(center_x, center_y, int(end_x), int(end_y))
        painter.end()

    def closeEvent(self, event):
        self.serial_connection.close()
        print("Serial connection closed.")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    visualizer = StickVisualizer()
    visualizer.show()
    sys.exit(app.exec_())
