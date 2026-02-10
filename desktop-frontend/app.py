# app.py
import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class EquipmentVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(300, 100, 800, 600)
        self.df = None  # Store CSV data

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Upload CSV button
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        self.layout.addWidget(self.upload_btn)

        # Show chart button
        self.show_btn = QPushButton("Show Summary Chart")
        self.show_btn.clicked.connect(self.show_summary)
        self.layout.addWidget(self.show_btn)

        # Matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def upload_csv(self):
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                # Check required columns
                required_cols = [
                    "equipment_id","equipment_name","equipment_type",
                    "status","location","purchase_year","condition"
                ]
                if not all(col in self.df.columns for col in required_cols):
                    QMessageBox.critical(
                        self, "Error",
                        "CSV columns do not match required format!"
                    )
                    self.df = None
                    return
                QMessageBox.information(self, "Success", "CSV loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def show_summary(self):
        if self.df is None:
            QMessageBox.warning(self, "Error", "Load a CSV first!")
            return

        summary = self.df['equipment_type'].value_counts()

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(summary.index, summary.values, color="skyblue")
        ax.set_title(f"Total Equipment: {len(self.df)}")
        ax.set_ylabel("Count")
        ax.set_xlabel("Equipment Type")
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EquipmentVisualizer()
    window.show()
    sys.exit(app.exec_())
