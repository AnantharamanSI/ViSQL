from PyQt6.QtWidgets import QWidget, QDialog, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QCheckBox, QComboBox
from PyQt6.QtCore import Qt
import mysql.connector as connector
from utils import create_table, format_attribute
from server import *


from styles import queryStyles

class CreateTable(QWidget):
  '''Create table in database'''
  def __init__(self, db):
    super().__init__()
    self.con = connector.connect(host=host, password=session, user=user, database=db)
    self.cur = self.con.cursor()
    layout = QVBoxLayout()

    heading = QLabel("Create Table")
    heading.setAccessibleName("heading")
    layout.addWidget(heading)

    about_this_page = """Let's learn how to create a new table in the database!\n
    1) First, enter the table name.
    2) Next, click on "Add attribute".
    3) Let's a "primary key"! 
      a) Name the key, say "id". 
      b) Now ensure you select "Not Null" and "Primary Key". Remember the primary key is always unique and cannot be null!
      c) Finally, click on "Confirm".
    4) We can keep adding more attributes in this way. 
    5) Click on "Create Table"! The table is now in the DB. Close the dialog box and proceed!

    Remember to refer to visql_log.txt to see the SQL commands that would have the same impact of creating the table!
    """

    about_pg = QLabel(about_this_page)
    about_pg.setAccessibleName("aboutme")
    layout.addWidget(about_pg)

    # Input field to enter new table name
    layout_title = QHBoxLayout()
    layout_title.addWidget(QLabel("Table Name: "))
    self.name = QLineEdit()
    layout_title.addWidget(self.name)

    add_att = QPushButton("Add Attribute")
    add_att.clicked.connect(self.add_attribute)

    self.attributes = []

    # Table to display attributes created
    headers = ['Name', 'Data Type', 'Not Null?', 'Primary Key?', 'Default Value']
    self.table = QTableWidget(0, 5)
    self.table.setHorizontalHeaderLabels(headers)
    self.table.horizontalHeader().setStyleSheet("color: black;")
    self.table.setStyleSheet("QTableWidget::item { background-color: #f0f0f0; }")

    create_table_btn = QPushButton("Create Table")
    create_table_btn.clicked.connect(self.create_table)
    
    layout.addLayout(layout_title)
    layout.addWidget(add_att)
    layout.addWidget(self.table)
    layout.addWidget(create_table_btn)

    self.setLayout(layout)
    self.setMinimumSize(750, 500)
    self.setStyleSheet(queryStyles)


  def add_attribute(self):
    # Dialog to add new attribute
    dialog = CreateAttribute(self)
    dialog.exec()


  def create_table(self):
    # Run mysql query to create table
    create_table(self.cur, self.name.text(), self.attributes)
    
    
  def close(self):
    self.con.close()
    super().close()


class CreateAttribute(QDialog):
  '''Dialog to create attribute while creating a new table'''
  def __init__(self, parent):
    super().__init__()
    layout = QVBoxLayout()

    num_fields = 5

    layouts = [QHBoxLayout() for i in range(num_fields)]
    labels = ['Name of Attribute', 'Data Type', 'Not Null', 'Primary Key', 'Default Value'] 

    # Adding titles to all sublayouts
    for i in range(num_fields):
      layouts[i].addWidget(QLabel(labels[i]))

    # Layout for attribute name
    self.name = QLineEdit()
    layouts[0].addWidget(self.name)

    # Layout for data type
    self.type = QComboBox()
    types = ['Integer', 'Varchar(30)', 'Varchar(500)', 'Date'] # TODO
    self.type.addItems(types)
    layouts[1].addWidget(self.type)
    
    # Layout for not null condition
    self.not_null = QCheckBox("Yes")
    layouts[2].addWidget(self.not_null)
    
    # Layout for primary key condition
    self.primary_key = QCheckBox("Yes")
    layouts[3].addWidget(self.primary_key)
    
    # Layout for default value
    self.default = QLineEdit()
    layouts[4].addWidget(self.default)

    # Add attribute
    self.set_att = QPushButton("Confirm")
    self.set_att.clicked.connect(self.set_attribute)

    # Add all attributes to main layout
    for sublayout in layouts:
      layout.addLayout(sublayout)
    
    layout.addWidget(self.set_att)

    self.setLayout(layout)
    self.parent = parent


  def set_attribute(self):
    
    # Formatting display for main window for new attribute
    params = [self.name.text(), self.type.currentText(), self.not_null.isChecked(), self.primary_key.isChecked(), self.default.text()]
    self.parent.attributes.append(format_attribute(*params))

    params[2] = 'Yes' if params[2] else 'No'
    params[3] = 'Yes' if params[3] else 'No'
    params[4] = params[4] if params[4] else 'None'


    # Update main window to display the new attribute
    currentRowCount = self.parent.table.rowCount()
    self.parent.table.insertRow(currentRowCount)   
    for i, param in enumerate(params):
      cell = QTableWidgetItem(param)
      cell.setFlags(Qt.ItemFlag.ItemIsEnabled)
      self.parent.table.setItem(currentRowCount, i, cell)

    self.close()  
