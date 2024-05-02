from PyQt6.QtWidgets import QStyleFactory


class Theme():
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.themeSelector = mainWindow.themeSelector


    def changeTheme(self):
        currentTheme = self.themeSelector.currentText()


        if currentTheme == "Light":
            self.mainWindow.setStyle(QStyleFactory.create('Fusion'))
            self.mainWindow.setStyleSheet(self.lightMode())
        elif currentTheme == "Dark":
            self.mainWindow.setStyle(QStyleFactory.create('Fusion'))
            self.mainWindow.setStyleSheet(self.darkMode())
        elif currentTheme == "Dracula":
            self.mainWindow.setStyle(QStyleFactory.create('Fusion'))
            self.mainWindow.setStyleSheet(self.draculaMode())


    def lightMode(self):
        theme = """
        QWidget {
            background-color: #f0f0f0;
            color:  #000000;
        }
       
        QLineEdit {
            background-color: #ffffff;
            border: 1px outset #000000;
            color: #000000;
        }
        QLineEdit:focus {
            border: 1px outset #005ba3;
        }
       
        QPushButton {
            background-color: #f0f0f0;
            color: #000000;
        }
        QPushButton:hover {
            background-color: #5a5a5a;
        }
        QTableView {
            background: #ffffff;
            border: 1px outset #000000;
            color: #000000;
        }
        """
        return theme


    def darkMode(self):
        theme = """
        QWidget {
            background-color: #333333;
            color: #ffffff;
        }
       
        QLineEdit {
            background-color: #4d4d4d;
            border: 1px outset #000000;
            color: #ffffff;
        }
        QLineEdit:focus {
            border: 1px outset #005ba3;
        }
        QPushButton {
            background-color: #4d4d4d;
            color: #ffffff;
        }
        QPushButton:hover {
            background-color: #0070c9;
        }
        QTableView {
            background: #4d4d4d;
            border: 1px outset #000000;
            color: #ffffff;
        }
        """
        return theme  


    def draculaMode(self):
        theme = """
        QWidget {
            background-color: #282a36;
            color:  #ffffff;
            border-color: #bd93f9;
        }
       
        QLineEdit {
            background-color: #282a36;
            border: 1px outset #000000;
            border-color: #bd93f9;
            color: #ffffff;
        }
        QLineEdit:focus {
            border: 1px outset #ff79c6;
        }
        QPushButton {
            background-color: #282a36;
            color: #ffffff;
            border-color: #bd93f9;
        }
        QPushButton:hover {
            background-color: #bd93f9;
        }
        QTableView {
            background: #21222c;
            border: 1px outset #000000;
            border-color: #bd93f9;
            color: #ffffff;
        }
        """
        return theme