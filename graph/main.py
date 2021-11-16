from PyQt5.QtWidgets import*
from PyQt5.QtCore import QDate, QDateTime
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT, FigureCanvas)
import pandas as pd
import DailyConverter
    
class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)
        loadUi("graph.ui",self)

        #selecting the date on the calendar if desired
        self.dateEditInput.setCalendarPopup(True)
        self.dateEditOutput.setCalendarPopup(True)

        self.button.clicked.connect(self.graph)
        #self.addToolBar(NavigationToolbar(self.matplotlib_widget.canvas, self))


    def graph(self):
        
        #sending required data to DailyConverter.py
        path_input_day = "input-tables/block_0.csv"
        path_output = "output-tables/block_0_day_converted.csv"
        start = str(self.dateEditInput.date().toPyDate())
        end = str(self.dateEditOutput.date().toPyDate())
        DailyConverter.convert(path_input_day, path_output, 'MAC000002', start, end)

        #reading the generated csv file and splitting its axes
        data = pd.read_csv(path_output)
        x = data.day
        y = data.energy_sum
        
        self.matplotlib_widget.canvas.axes.clear() #deleting the old chart before the new chart is created
        self.matplotlib_widget.canvas.axes.plot(x,y) #plotting
        self.matplotlib_widget.canvas.axes.tick_params(labelrotation=45) #arrangement of the way the information on the axes is written in terms of readability
        self.matplotlib_widget.canvas.axes.set(xlabel="Days", ylabel="Energy Consumption (kWh)", title="Consumption of a HouseHold")
        self.matplotlib_widget.canvas.axes.grid()
        self.matplotlib_widget.canvas.draw()
        

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()

