from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import pandas as pd
import DailyConverter


class MatplotlibWidget(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)
        loadUi("graph.ui", self)

        # selecting the date on the calendar if desired
        self.dateEditInput.setCalendarPopup(True)
        self.dateEditOutput.setCalendarPopup(True)

        self.graphButton.clicked.connect(self.graph)
        self.addToolBar(NavigationToolbar(self.matplotlib_widget.canvas, self))

        self.household()

    def household(self):

        path_input = "input-tables/block_0.csv" 
        householdData = pd.read_csv(path_input) # reading csv file
        id = householdData['LCLid'].tolist() # converting column data to list
        id = list(dict.fromkeys(id)) # the duplicate elements in the list are removed using the "dictionary" structure in python.
        menu = QMenu() # creating menu

        self.householdButton.setMenu(menu) # button turns into menu.

        menu.triggered.connect(lambda x: self.householdButton.setText(x.text())) # the clicked item is written on the button
        menu.triggered.connect(self.actionClicked) # after selecting the item from the menu with the button, the "actionClicked" function is called.

        self.addMenu(id, menu) # "id" and "menu" are sending to "addMenu" function
    
    def actionClicked(self, action):
        self.householdId = action.text() # the item selected from the menu is assigned to the variable "householdId"

    def addMenu(self, householdData, menuObject): #in this function the households are added to the menu
        if isinstance(householdData, dict):
            for i, j in householdData.items():
                subMenu = QMenu(i, menuObject)
                menuObject.addMenu(subMenu)
                self.addMenu(j, subMenu)

        elif isinstance(householdData, list):
            for element in householdData:
                self.addMenu(element, menuObject)

        else:
            action = menuObject.addAction(householdData)
            action.setIconVisibleInMenu(False)

    def graph(self):

        # sending required data to DailyConverter.py
        path_input = "input-tables/block_0.csv"
        path_output = "output-tables/block_0_day_converted.csv"
        start = str(self.dateEditInput.date().toPyDate())
        end = str(self.dateEditOutput.date().toPyDate())

        DailyConverter.convert(path_input, path_output, self.householdId, start, end)

        # reading the generated csv file and splitting its axes
        data = pd.read_csv(path_output)
        x = data.day
        y = data.energy_sum

        # deleting the old chart before the new chart is created
        self.matplotlib_widget.canvas.axes.clear()
        self.matplotlib_widget.canvas.axes.plot(x, y)  # plotting
        # arrangement of the way the information on the axes is written in terms of readability
        self.matplotlib_widget.canvas.axes.tick_params(labelrotation=45)
        self.matplotlib_widget.canvas.axes.set(xlabel="Days", ylabel="Energy Consumption (kWh)", title="Consumption of a HouseHold")
        self.matplotlib_widget.canvas.axes.grid()
        self.matplotlib_widget.canvas.draw()


app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()
