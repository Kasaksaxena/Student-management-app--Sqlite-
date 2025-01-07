from PyQt6.QtWidgets import QApplication,QLabel,QWidget,QGridLayout,\
                             QLineEdit,QPushButton,QMainWindow,QTableWidget
from PyQt6.QtGui import QAction 
import sys

class MainWindow(QMainWindow):# inherits From QMainWindow a predefined class that provides a main application window
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")  
        
        # menubar-creates a menu bar for the main window
        #addMenu- Add a"File"or "Help" menu to the menubar.. the & allow the "F" or "H" to be used
                  # as keyboard shortcut(Alt +F)  
        file_menu_item=self.menuBar().addMenu("&File")
        help_menu_item=self.menuBar().addMenu("&Help")  
        
        #Creates an action labeled "Add student" that can be used in "File" menu
        add_student_action=QAction("Add Student",self)   
        file_menu_item.addAction(add_student_action)# Add this action to "File" menu
        
        about_action=QAction("About",self)# Creates an about action to help menu   
        help_menu_item.addAction(about_action) 
        
        #Removes the default behavior for "About" menu action 
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        
        self.table=QTableWidget()# A widget that displays data in a tabular form(like a spreadsheet)
        self.table.setColumnCount(4)# Defines number of columns in the table
        self.table.setHorizontalHeaderLabels(("ID","Name","Course","Mobile"))# set header labels for columns and tuple id specifies name of each col
        self.setCentralWidget(self.table)#places Qtablewidget in main windows central area replacing any existing central widgets
        
        
app=QApplication(sys.argv)
student_app=MainWindow()
student_app.show()
sys.exit(app.exec())                      