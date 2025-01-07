from PyQt6.QtWidgets import QApplication,QLabel,QWidget,QGridLayout,\
                             QLineEdit,QPushButton,QMainWindow
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
        
app=QApplication(sys.argv)
student_app=MainWindow()
student_app.show()
sys.exit(app.exec())                      