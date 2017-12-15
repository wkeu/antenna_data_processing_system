import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
 
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 input dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        #Choose the type of antenna
        self.getChoice()
        
        #Find out how many tilts
        self.getTiltnumber()
        
        #TODO:
        #Get the name of each file
        self.getText()
        
        self.show()
 
    #TODO: Save file
    def getChoice(self):
        items = ("Sector Antenna","Omnidirectional","Tri Sector")
        item, okPressed = QInputDialog.getItem(self, "Get item","Color:", items, 0, False)
        if okPressed and item:
            print(item)
    
    def getTiltnumber(self):
        i, okPressed = QInputDialog.getInt(self, "Get integer","Percentage:", 28, 0, 100, 1)
        if okPressed:
            return i
 
    """
    def getDouble(self):
        d, okPressed = QInputDialog.getDouble(self, "Get double","Value:", 10.50, 0, 100, 10)
        if okPressed:
            return d
    """

    """
    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Get text","Your name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
    """
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())