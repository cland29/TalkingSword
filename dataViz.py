import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QScrollBar, QPushButton, QLabel, QFileDialog, QSlider, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class DataFrameViewer(QMainWindow):
    def __init__(self, dataframe):
        super().__init__()

        self.dataframe = dataframe
        self.timeframe = 50  # Number of rows to display at a time
        self.start_index = 0

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Pandas DataFrame Viewer")

        # Main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Scrollbar
        self.scrollbar = QScrollBar()
        self.scrollbar.setOrientation(1)  # Horizontal orientation
        self.scrollbar.setMaximum(len(self.dataframe) - self.timeframe)
        self.scrollbar.valueChanged.connect(self.update_plot)
        layout.addWidget(self.scrollbar)

        # Timeframe slider
        slider_layout = QHBoxLayout()
        self.slider_label = QLabel(f"Timeframe: {self.timeframe}")
        self.timeframe_slider = QSlider()
        self.timeframe_slider.setOrientation(1)  # Horizontal orientation
        self.timeframe_slider.setMinimum(10)
        self.timeframe_slider.setMaximum(100)
        self.timeframe_slider.setValue(self.timeframe)
        self.timeframe_slider.valueChanged.connect(self.update_timeframe)

        slider_layout.addWidget(self.slider_label)
        slider_layout.addWidget(self.timeframe_slider)
        layout.addLayout(slider_layout)

        # Save button
        self.save_button = QPushButton("Save Current View")
        self.save_button.clicked.connect(self.save_current_view)
        layout.addWidget(self.save_button)

        # Info label
        self.info_label = QLabel("Scroll to view different timeframes.")
        layout.addWidget(self.info_label)

        # Initial plot
        self.update_plot()

    def update_plot(self):
        self.start_index = self.scrollbar.value()
        end_index = self.start_index + self.timeframe
        visible_data = self.dataframe.iloc[self.start_index:end_index]

        # Update Matplotlib plot
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Plot features using timestamp as x-axis, excluding timestamp and classification columns from y
        for column in visible_data.columns:
            if column not in ["timestamp", "classification"]:
                ax.plot(visible_data['timestamp'], visible_data[column], label=column)

        ax.set_title("Data Viewer")
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Values")

        # Add classification line
        unique_classes = visible_data["classification"].unique()
        class_colors = {cls: color for cls, color in zip(unique_classes, ["red", "blue", "green", "orange", "purple"])}
        classification_colors = visible_data["classification"].map(class_colors)
        ax.scatter(visible_data['timestamp'], [-0.1] * len(visible_data), c=classification_colors, label="Classification", marker="|")

        # Add legend
        handles = [ax.plot([], [], color=color, label=str(cls))[0] for cls, color in class_colors.items()]
        ax.legend(handles=handles, title="Classification")

        self.canvas.draw()

    def update_timeframe(self):
        self.timeframe = self.timeframe_slider.value()
        self.slider_label.setText(f"Timeframe: {self.timeframe}")
        self.scrollbar.setMaximum(len(self.dataframe) - self.timeframe)
        self.update_plot()

    def save_current_view(self):
        end_index = self.start_index + self.timeframe
        visible_data = self.dataframe.iloc[self.start_index:end_index]

        # Get classification value
        classification_value = str(visible_data["classification"].iloc[0])
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", f"{classification_value}.csv", "CSV Files (*.csv)")

        if filename:
            visible_data.to_csv(filename, index=False)
            self.info_label.setText(f"Saved to {filename}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create a sample DataFrame
    data = {
        "timestamp": pd.date_range(start="2023-01-01", periods=200, freq="D"),
        "Feature1": np.sin(np.linspace(0, 20, 200)),
        "Feature2": np.cos(np.linspace(0, 20, 200)),
        "classification": ["A"] * 50 + ["B"] * 50 + ["C"] * 50 + ["D"] * 50
    }
    df = pd.DataFrame(data)

    df = pd.read_csv("data1.txt")

    viewer = DataFrameViewer(df)
    viewer.show()

    sys.exit(app.exec_())
