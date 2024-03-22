from PyQt6.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QComboBox
from styles import queryStyles
from server import *
import mysql.connector as connector
from utils import get_tables, get_table_attributes, format_insert_data, insert_data

class DataItem(QDialog):
  '''Dialog to insert data for a row of the table'''
  def __init__(self, parent, table):
    super().__init__()
    self.parent = parent
    
    layout = QVBoxLayout()
    
    # Get the selected table's attributes for data entry
    labels = get_table_attributes(self.parent.cur, table)
    num_fields = len(labels)

    # Create an input box for each atttribute's data
    self.lineEdits = [QLineEdit() for i in range(num_fields)]
    layouts = [QHBoxLayout() for i in range(num_fields)]

    # Add attribute and data input to sublayouts
    for i in range(num_fields):
      layouts[i].addWidget(QLabel(labels[i]))
      layouts[i].addWidget(self.lineEdits[i])

    # Button to add data row
    self.set_att = QPushButton("Confirm")
    self.set_att.clicked.connect(self.set_attribute)

    # Add all sublayouts to main layout
    for sublayout in layouts:
      layout.addLayout(sublayout)
    
    layout.addWidget(self.set_att)

    self.setLayout(layout)


  def set_attribute(self):
    # Retrieve all data entered in input fields    
    params = [line.text() for line in self.lineEdits]
    # Pass row data to parent component
    self.parent.data.append(params)

    # Update parent component to display the new data row
    currentRowCount = self.parent.table.rowCount()
    self.parent.table.insertRow(currentRowCount)   

    for i, param in enumerate(params):
      self.parent.table.setItem(currentRowCount, i, QTableWidgetItem(param))

    self.close()  


class InsertData(QWidget):
  '''Insert data into an existing table'''
  def __init__(self, db):
    super().__init__()
    self.con = connector.connect(host=host, password=session, user=user, database=db) 
    self.cur = self.con.cursor()
    layout = QVBoxLayout()

    heading = QLabel("Insert Rows")
    heading.setAccessibleName("heading")
    layout.addWidget(heading)

    about_this_page = """Let's learn how to insert content into a new table in the database!\n
    1) First, select the table.
    2) Next, click on "Add Data Item".
    3) Enter the data for each attribute in the table. Remember to enter VARCHAR and DATE data in quotes!
    4) Feel free to add more rows. 
    5) Click on "Insert Data"! 

    Remember to refer to visql_log.txt to see the SQL commands that would have the same impact of creating the table!
    """

    about_pg = QLabel(about_this_page)
    about_pg.setAccessibleName("aboutme")
    layout.addWidget(about_pg)
    
    self.table_name = None
    # Sublayout to select table
    layout_title = QHBoxLayout()
    layout_title.addWidget(QLabel("Table Name: "))

    # Get all tables in current database
    self.name = QComboBox()
    self.name.activated.connect(self.set_table)
    self.name.addItems(get_tables(self.cur))
    self.name.setPlaceholderText('--selection--')
    self.name.setCurrentIndex(-1)
    self.table_name = self.name.currentText()
    
    layout_title.addWidget(self.name)

    # Open dialog to enter a row's data
    add_att = QPushButton("Add Data Item")
    add_att.clicked.connect(self.add_item)

    # Create an empty table to display data rows
    self.table = QTableWidget(0, 0)

    create_table_btn = QPushButton("Insert Data")
    create_table_btn.clicked.connect(self.insert_data)
    
    layout.addLayout(layout_title)
    layout.addWidget(add_att)
    layout.addWidget(self.table)
    layout.addWidget(create_table_btn)

    self.data = []
    self.setLayout(layout)
    self.setMinimumSize(750, 500)
    self.setStyleSheet(queryStyles)


  def add_item(self):
    # Open dialog to enter a row's data
    dialog = DataItem(self, self.table_name)
    dialog.exec()
    

  def set_table(self):
    self.table_name = self.name.currentText()
    print('table name', self.table_name, self.name.currentText())
    header = get_table_attributes(self.cur, self.table_name)
    # Set diplay table dimensions and attributes as header
    self.table.setRowCount(0)
    self.table.setColumnCount(len(header))
    self.table.setHorizontalHeaderLabels(header)
    self.table.horizontalHeader().setStyleSheet("color: black;")
    self.table.setStyleSheet("QTableWidget::item { background-color: #f0f0f0; }")


  def insert_data(self):
    # Retrieve the currently selected table
    name = self.name.currentText()
    # Format insert data for query
    data = format_insert_data(self.data)
    insert_data(self.con, name, data)
    
    
  def close(self):
    self.con.close()
    super().close()

