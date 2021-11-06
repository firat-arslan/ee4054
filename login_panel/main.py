import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
import sqlite3

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui", self)
        self.login.clicked.connect(self.loginFunction)
        self.login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.create_account.clicked.connect(self.createAccount) #createAccount ekranına geçiş
        self.create_account.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.show_hide.clicked.connect(self.toggleVisibility)

    def toggleVisibility(self):
        if self.password_field.echoMode()==(QtWidgets.QLineEdit.Password):
            self.show_hide.setStyleSheet("background-image : url(images/hide.jpg);")
            self.password_field.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.show_hide.setStyleSheet("background-image : url(images/show.jpg);")
            self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
                

    def loginFunction(self):
        user = self.username_field.text()
        password = self.password_field.text()


        if len(user)==0 or len(password)==0:
            self.error_field.setText("Please input all fields.")
        else:
            connection = sqlite3.connect("user_info.db") #database connection
            cursor = connection.cursor()
            query = "SELECT password FROM user_info WHERE username =\'"+user+"\'"
            cursor.execute(query)
            result_pass = cursor.fetchone()[0]

            if result_pass == password:
                # başarılı giriş yapıldığı zaman, message box kaldırılıp bu block üzerinden sonraki sayfaya yönlendirilecek.
                self.welcomeAccount()
                """message = QMessageBox()
                message.setIcon(QMessageBox.Information)
                message.setText("You have successfully logged in")
                message.setWindowTitle("Login")
                message.setStandardButtons(QMessageBox.Ok)
                message.exec()"""
                self.error_field.setText("")
            else:
                self.error_field.setText("Invalid username or password.")


    def createAccount(self):
        create = createAccountScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def welcomeAccount(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcome.ui", self)

class createAccountScreen(QDialog):
    def __init__(self):
        super(createAccountScreen, self).__init__()
        loadUi("create_account.ui", self)
        self.reg.clicked.connect(self.signUp)
        self.reg.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.show_hide.clicked.connect(self.toggleVisibility_1)
        self.show_hide_2.clicked.connect(self.toggleVisibility_2)

    def toggleVisibility_1(self):
        if self.password_field.echoMode()==(QtWidgets.QLineEdit.Password):
            self.show_hide.setStyleSheet("background-image : url(images/hide.jpg);")
            self.password_field.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.show_hide.setStyleSheet("background-image : url(images/show.jpg);")
            self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)

        
    def toggleVisibility_2(self):
        if self.confirm_password_field.echoMode()==(QtWidgets.QLineEdit.Password):
            self.show_hide_2.setStyleSheet("background-image : url(images/hide.jpg);")
            self.confirm_password_field.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.show_hide_2.setStyleSheet("background-image : url(images/show.jpg);")
            self.confirm_password_field.setEchoMode(QtWidgets.QLineEdit.Password)


    def signUp(self):
        user = self.username_field.text()
        password = self.password_field.text()
        confirm_password = self.confirm_password_field.text()

        if len(user)==0 or len(password)==0:
            self.error_field.setText("Please input all fields.")
            self.error_field.setText("")
        elif password != confirm_password:
            self.error_field.setText("Passwords do not match.")
            self.error_field.setText("")
        else:
            connection = sqlite3.connect("user_info.db")
            cursor = connection.cursor()

            user_info = [user, password]
            cursor.execute('INSERT INTO user_info (username, password) VALUES (?,?)', user_info) #database'e info ekleme

            message = QMessageBox()
            message.setIcon(QMessageBox.Information)
            message.setText("You have successfully registered in the system. You are redirected to the login page.")
            message.setWindowTitle("Register")
            message.setStandardButtons(QMessageBox.Ok)
            returnValue = message.exec()
            if returnValue == QMessageBox.Ok:
                self.login() #kayıt tamamlandığında login ekranına dönüş
            
            self.error_field.setText("")

            connection.commit()
            connection.close()
        
    def login(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)



app = QApplication(sys.argv)
login = LoginScreen()
login.show()
widget = QtWidgets.QStackedWidget()
widget.addWidget(login)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
sys.exit(app.exec_())