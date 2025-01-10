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