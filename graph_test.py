import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Canvas(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots(figsize=(12, 8), dpi=100)
        super().__init__(fig)
        self.setParent(parent)

        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)

        """
        button = QPushButton("Button1", self)
        button.move(500, 700)

        button2 = QPushButton("Button2", self)
        button2.move(700, 700)
        """

        data = pd.read_csv(r"C:\Users\ismailfiratarslan\Downloads\block_0.csv", nrows=7)
        x = data.day
        y = data.energy_sum
        self.ax.plot(x, y, '.-', color='red', label="energy_sum")
        plt.legend(loc="upper left")
        self.ax.set(xlabel="Days", ylabel="Energy Consumption (KiloWatt*Hour)", title="Weekly Consumption of a HouseHold")
        self.ax.grid()


class TestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1200, 800)
        self.setWindowTitle("Matplotlib in PyQt5")
        Canvas(self)


app = QApplication(sys.argv)
test = TestApp()
test.show()
sys.exit(app.exec_())
