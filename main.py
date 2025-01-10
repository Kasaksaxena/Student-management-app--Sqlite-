from PyQt6.QtWidgets import QApplication,QLabel,QWidget,QGridLayout,\
                 QLineEdit,QPushButton,QMainWindow,QTableWidget,\
                 QTableWidgetItem,QDialog,QVBoxLayout,QComboBox,QMessageBox,\
                 QToolBar,QStatusBar
from PyQt6.QtGui import QAction,QIcon
import sys
import sqlite3
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):# inherits From QMainWindow a predefined class that provides a main application window
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")  
        self.setMinimumSize(800,600)
        # menubar-creates a menu bar for the main window
        #addMenu- Add a"File"or "Help" menu to the menubar.. the & allow the "F" or "H" to be used
                  # as keyboard shortcut(Alt +F)  
        file_menu_item=self.menuBar().addMenu("&File")
        help_menu_item=self.menuBar().addMenu("&Help")  
        edit_menu_item=self.menuBar().addMenu("&Edit")
        
        #Creates an action labeled "Add student" that can be used in "File" menu
        add_student_action=QAction(QIcon("icons\\add.png"),"Add Student",self)
        add_student_action.triggered.connect(self.insert)
        search_edit_action=QAction(QIcon("icons\\search.png"),"Search",self)
        search_edit_action.triggered.connect(self.search)
        
         
        file_menu_item.addAction(add_student_action)# Add this action to "File" menu
        
        about_action=QAction("About",self)# Creates an about action to help menu   
        help_menu_item.addAction(about_action) 
        edit_menu_item.addAction(search_edit_action)
        
        #Removes the default behavior for "About" menu action 
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)
        self.table=QTableWidget()# A widget that displays data in a tabular form(like a spreadsheet)
        self.table.setColumnCount(4)# Defines number of columns in the table
        self.table.setHorizontalHeaderLabels(("ID","Name","Course","Mobile"))# set header labels for columns and tuple id specifies name of each col
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)#places Qtablewidget in main windows central area replacing any existing central widgets
        
        #create toolbar and add toolbar elementsis widget that provides way to create 
        # and organize toolbar buttons ,menus and other controls
        #QToolBar 
        toolbar=QToolBar()
        toolbar.setMovable(True)#determines whether toolbar can be moved or repositioned by user
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_edit_action)
        
        # create a status barr and its elements
        self.statusbar=QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # Detect a click
        self.table.cellClicked.connect(self.cell_clicked)
        
    def cell_clicked(self):
        edit_button=QPushButton("Edit Record")  
        edit_button.clicked.connect(self.edit) 
        delete_button=QPushButton("Delete Record") 
        delete_button.clicked.connect(self.delete) 
        
        #checks if any QPushbotton in status bar and remove them
        #ensures that any existing buttons are cleared before adding new ones
        children=self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)
                
                
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)
        
         
         
        
        
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
        
    def search(self):
        search_dialog=SearchDialog()
        search_dialog.exec()
        
    def edit(self):
        edit_dialog=EditDialog()
        edit_dialog.exec()
    
    def delete(self):
        dialog=DeleteDialog()
        dialog.exec()
    
    def about(self):
        dialog=AboutDialog()
        dialog.exec()           
        
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
      self.courses=["Biology","Math","Astronomy","Physics","Computer Science","Biotechnology","Civil Engineering","Mechanical Engineering"] 
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
    
class SearchDialog(QDialog):
    def __init__(self):
      super().__init__()
      self.setWindowTitle("Search Student")
      self.setFixedHeight(300)
      self.setFixedWidth(300)  
      #Create layout and input widget
      layout=QVBoxLayout()
      self.search_name=QLineEdit()
      self.search_name.setPlaceholderText("Type for search")  
      layout.addWidget(self.search_name) 
      button=QPushButton("Search")
      button.clicked.connect(self.search_student)
      layout.addWidget(button)
      
      self.setLayout(layout)
      
    def search_student(self):
        name=self.search_name.text()
        Connection=sqlite3.connect("data.db")
        cursor=Connection.cursor()
        result=cursor.execute("Select * FROM Student_Data \
                               Where name=?",(name,)) 
        rows=list(result)
        print("Result",result)
        print("Row",rows)
        
        if not rows:
            QMessageBox.information(self,"Not Found",f"No student found with name : {name}")#display informational message to users
        #search for matching items in QTablewidget by the name provided
        items=student_app.table.findItems(name, \
               Qt.MatchFlag.MatchFixedString)#ensures  that search looks for exact matches to string you provide (string comparison is case-sensitive)
        for item in items:#iterates over the matching items 
            print(item)
            #and highlights(selects) the corresponding rows in table by calling setSelected(True)
            student_app.table.item(item.row(),\
                1).setSelected(True)     
            
        cursor.close()
        Connection.close()                      
        
     
class EditDialog(QDialog):
  def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)  
        
        layout=QVBoxLayout()# creates a vertical layout to arrange widgets vertically
        
        index=student_app.table.currentRow()
        print("INDEX",index)
        self.student_id=student_app.table.item(index,0).text()
        
        student_Name=student_app.table.item(index,1)
        print("Student",student_Name)
        
        #get student name for selected row
        self.student_name=QLineEdit(student_Name.text()if student_Name else "")
        self.student_name.setPlaceholderText("Name")  
        layout.addWidget(self.student_name) 
        
       
        course_Name=student_app.table.item(index,2)
        course_Name=course_Name.text() if course_Name else""
        print("course:name",course_Name)
        self.course_name=QComboBox()    
        courses=["Biology","Math","Astronomy","Physics","Computer Science","Biotechnology","Civil Engineering","Mechanical Engineering"] 
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_Name)
        layout.addWidget(self.course_name)   
        
        mobile=student_app.table.item(index,3).text()
        self.mobile=QLineEdit(mobile)
        self.mobile.setPlaceholderText("Phone no.")  
        layout.addWidget(self.mobile) 
        button=QPushButton("Register")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)
            
        self.setLayout(layout) 
     
  def update_student(self):
        name=self.student_name.text()
        #currentindex retrieve index of currently selected itm and .itemtext retrives tet at given index
        course=self.course_name.itemText(self.course_name.currentIndex())
        mobile=self.mobile.text()
        id=self.student_id
        
        connection=sqlite3.connect("data.db")       
        cursor=connection.cursor()
        cursor.execute("UPDATE Student_Data SET Name=?, Course=?,Mobile=? WHERE id=?",(name,course,mobile,id))
        connection.commit()
        cursor.close()
        connection.close()
        #resfresh the table
        student_app.load_data()
         
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        layout=QGridLayout()
        confirmation=QLabel("Are you sure you want to delete?")
        yes=QPushButton("Yes")
        no=QPushButton("No")
        
        layout.addWidget(confirmation,0,0,1,2)
        layout.addWidget(yes,1,0)
        layout.addWidget(no,1,1)
        self.setLayout(layout)
        
        yes.clicked.connect(self.delete_student) 
    
    def delete_student(self):
        #Get selected row index and student id from thet selected row
        index=student_app.table.currentRow()
        print("INDEX",index)
        student_id=student_app.table.item(index,0).text()
        
        connection=sqlite3.connect("data.db")       
        cursor=connection.cursor()
        cursor.execute("DELETE FROM  Student_Data WHERE Id=?",(student_id))
        connection.commit()
        cursor.close()
        connection.close()
        student_app.load_data()
        
        self.close()
        
        confirmation_widget=QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()
 
class AboutDialog(QMessageBox):   
  def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        conetnt="""
This Student Management App simplifies the process of managing student data efficiently.
It allows users to add, edit, and delete student records, including details like name, course, 
and contact information.
Built using Python and PyQt6, the app ensures a user-friendly interface with real-time updates for seamless operation.
Perfect for educational institutions and small-scale management needs.

        """
        self.setText(conetnt)    
app=QApplication(sys.argv)
student_app=MainWindow()
student_app.show()
student_app.load_data()
sys.exit(app.exec())                      