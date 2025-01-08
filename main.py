from PyQt6.QtWidgets import QApplication,QLabel,QWidget,QGridLayout,\
                             QLineEdit,QPushButton,QMainWindow,QTableWidget,\
                            QTableWidgetItem,QDialog,QVBoxLayout,QComboBox
from PyQt6.QtGui import QAction 
import sys
import sqlite3

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
        add_student_action.triggered.connect(self.insert)
        
         
        file_menu_item.addAction(add_student_action)# Add this action to "File" menu
        
        about_action=QAction("About",self)# Creates an about action to help menu   
        help_menu_item.addAction(about_action) 
        
        #Removes the default behavior for "About" menu action 
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        
        self.table=QTableWidget()# A widget that displays data in a tabular form(like a spreadsheet)
        self.table.setColumnCount(4)# Defines number of columns in the table
        self.table.setHorizontalHeaderLabels(("ID","Name","Course","Mobile"))# set header labels for columns and tuple id specifies name of each col
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)#places Qtablewidget in main windows central area replacing any existing central widgets
        
    def load_data(self):
        connection=sqlite3.connect("data.db")
        result=connection.execute(" SELECT * FROM Student_Data")
        self.table.setRowCount(0) 
        for row_number,row_data in enumerate(result):
            self.table.insertRow(row_number) 
            for column_number , data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
                                   
        connection.close()  
                
    def insert(self):
        dialog=InsertDialog()#creates an instance of Insert dialog
        dialog.exec()# display dialog window( a model dialog that blocks interaction with other windows until)
        self.load_data()
        
class InsertDialog(QDialog):#creates a diaolog window where user can input student data  
  def __init__(self):
      super().__init__()
      self.setWindowTitle("Insert Student Data")
      self.setFixedHeight(300)
      self.setFixedWidth(300)  
      
      layout=QVBoxLayout()# creates a vertical layout to arrange widgets vertically
      
      self.student_name=QLineEdit()
      self.student_name.setPlaceholderText("Name")  
      layout.addWidget(self.student_name) 
      self.course_name=QComboBox()    
      self.courses=["Biology","Math","Astronomy","Physics","Computer Science"] 
      self.course_name.addItems(self.courses)
      layout.addWidget(self.course_name)   
      self.mobile=QLineEdit()
      self.mobile.setPlaceholderText("Phone no.")  
      layout.addWidget(self.mobile) 
      button=QPushButton("Register")
      button.clicked.connect(self.add_student)
      layout.addWidget(button)
         
      self.setLayout(layout) 
  def add_student(self):
      name=self.student_name.text()
      course=self.course_name.itemText(self.course_name.currentIndex())
      mobile=self.mobile.text()
      
      connection=sqlite3.connect("data.db")    
      cursor=connection.cursor()
      cursor.execute("INSERT INTO Student_Data (Name,Course,Mobile) VALUES(?,?,?)",
                     (name,course,mobile))
      connection.commit()
      connection.close()         
        
app=QApplication(sys.argv)
student_app=MainWindow()
student_app.show()
student_app.load_data()
sys.exit(app.exec())                      