from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import pandas as pd
    
class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)
        loadUi("graph.ui",self)
        self.button.clicked.connect(self.graph)
        self.addToolBar(NavigationToolbar(self.matplotlib_widget.canvas, self))


    def graph(self):
        path = "output-tables/block_0_day_converted.csv"
        
        data = pd.read_csv(path)
        x = data.day
        y = data.energy_sum
        
        self.matplotlib_widget.canvas.axes.clear()
        self.matplotlib_widget.canvas.axes.plot(x,y)
        self.matplotlib_widget.canvas.axes.tick_params(labelrotation=45)
        self.matplotlib_widget.canvas.axes.set(xlabel="Days", ylabel="Energy Consumption (KiloWatt*Hour)", title="Weekly Consumption of a HouseHold")
        self.matplotlib_widget.canvas.draw()

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()

