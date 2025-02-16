import sys
import pandas as pd
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPainter, QPen, QMatrix4x4, QVector3D

class RodVisualizer(QMainWindow):
    def __init__(self, df):
        super().__init__()

        self.df = df
        self.current_index = 0
        self.timer = QTimer()
        self.is_playing = False

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Gyro Rod Visualizer (3D)")

        # Main widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Canvas for drawing the rod
        self.canvas = Canvas(self.df)
        main_layout.addWidget(self.canvas)

        # Controls layout
        controls_layout = QHBoxLayout()

        # Slider to scroll through the data
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.df) - 1)
        self.slider.valueChanged.connect(self.update_position)
        controls_layout.addWidget(self.slider)

        # Play button
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.toggle_play)
        controls_layout.addWidget(self.play_button)

        main_layout.addLayout(controls_layout)

        # Set central widget
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Timer for real-time playback
        self.timer.timeout.connect(self.play)

    def update_position(self, index):
        self.current_index = index
        self.canvas.update_position(index)

    def toggle_play(self):
        if self.is_playing:
            self.timer.stop()
            self.play_button.setText("Play")
        else:
            self.timer.start(30)  # Adjust playback speed as needed
            self.play_button.setText("Pause")
        self.is_playing = not self.is_playing

    def play(self):
        if self.current_index < len(self.df) - 1:
            self.current_index += 1
            self.slider.setValue(self.current_index)
        else:
            self.timer.stop()
            self.is_playing = False
            self.play_button.setText("Play")


class Canvas(QWidget):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.current_index = 0

    def update_position(self, index):
        self.current_index = index
        self.update()

    def paintEvent(self, event):
        if self.df.empty:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Get the current gyro angles
        row = self.df.iloc[self.current_index]
        angles = QVector3D(row['x_angle'], row['y_angle'], row['z_angle'])

        # Set up a 3D rotation matrix
        rotation_matrix = QMatrix4x4()
        rotation_matrix.rotate(angles.x(), QVector3D(1, 0, 0))  # Rotate around x-axis
        rotation_matrix.rotate(angles.y(), QVector3D(0, 1, 0))  # Rotate around y-axis
        rotation_matrix.rotate(angles.z(), QVector3D(0, 0, 1))  # Rotate around z-axis

        # Define the rod in 3D space (as a line segment)
        rod_start = QVector3D(0, 0, 0)
        rod_end = QVector3D(0, -100, 0)  # 100 units in negative y direction

        # Apply rotation
        rod_end = rotation_matrix * rod_end

        # Map 3D points to 2D for display
        center_x = self.width() // 2
        center_y = self.height() // 2

        def project_to_2d(point):
            return center_x + point.x(), center_y - point.y()

        start_2d = project_to_2d(rod_start)
        end_2d = project_to_2d(rod_end)

        # Draw the rod
        pen = QPen(Qt.black, 4)
        painter.setPen(pen)
        painter.drawLine(int(start_2d[0]), int(start_2d[1]), int(end_2d[0]), int(end_2d[1]))

        # Draw the pivot point
        pen = QPen(Qt.red, 6)
        painter.setPen(pen)
        painter.drawPoint(int(center_x), int(center_y))


def main():
    # Sample DataFrame for testing
    data = {
        'timestamp': np.arange(0, 10000, 100),  # Timestamps in milliseconds
        'x_angle': np.linspace(0, 360, 100),    # Rotation around x-axis in degrees
        'y_angle': np.linspace(0, 180, 100),    # Rotation around y-axis in degrees
        'z_angle': np.linspace(0, 90, 100)      # Rotation around z-axis in degrees
    }
    df = pd.DataFrame(data)

    df = pd.read_csv("data1.txt")
    roll_window = 5
    df["x_angle"] = df["gyroX"].mul(45).rolling(window=roll_window).mean()
    df["y_angle"] = df["gyroY"].mul(45).rolling(window=roll_window).mean()
    df["z_angle"] = df["gyroZ"].mul(45).rolling(window=roll_window).mean()
    df = df.iloc[roll_window:]

    app = QApplication(sys.argv)
    visualizer = RodVisualizer(df)
    visualizer.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
