from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QAbstractItemView
from PyQt6.QtCore import Qt
import mysql.connector as connector
from components import MessageDialog
from utils import get_tables
from server import *
from styles import queryStyles

class DescribeTable(QWidget):
  '''Display table structure'''
  def __init__(self, db):
    super().__init__()
    self.con = connector.connect(host=host, password=session, user=user, database=db)
    self.cur = self.con.cursor()
    self.layout = QVBoxLayout()

    heading = QLabel("Describe Table")
    heading.setAccessibleName("heading")
    self.layout.addWidget(heading)

    about_this_page = """Let's learn how to describe a table from our database! The describe command lists all the columns of a table along with their attributes.\n
    1) Select a table from the drop-down menu.
    2) CLick on "Describe Table".
    3) You will see the description displayed on the screen. 
    
    Remember to check the visql_log.txt file to see the SQL command that would have the same impact!
    """

    about_pg = QLabel(about_this_page)
    about_pg.setAccessibleName("aboutme")
    self.layout.addWidget(about_pg)

    # Dropdown to select table
    layout_table = QHBoxLayout()
    table_title = QLabel("Table: ")
    self.table_dropdown = QComboBox()
    self.table_dropdown.addItems(get_tables(self.cur))
    self.table_dropdown.activated.connect(self.table_activated)
    self.table_dropdown.setPlaceholderText('--selection--')
    self.table_dropdown.setCurrentIndex(-1)

    layout_table.addWidget(table_title)
    layout_table.addWidget(self.table_dropdown)

    self.desc_table_btn = QPushButton("Describe Table")
    self.desc_table_btn.setDisabled(True)
    self.desc_table_btn.clicked.connect(self.desc_table)    

    self.layout.addLayout(layout_table)
    self.layout.addWidget(self.desc_table_btn)

    self.setLayout(self.layout)
    self.setMinimumSize(750, 500)
    self.setStyleSheet(queryStyles)
    
  def table_activated(self):
    self.desc_table_btn.setDisabled(False)
    
  def desc_table(self):
    table_name = self.table_dropdown.currentText()
    
    try:
      self.table.hide() # Hide previous table structure displayed
    except:
      pass

    self.cur.execute(f"desc {table_name}")
    self.results = self.cur.fetchall()

    headers = list(map(lambda i : i[0], self.cur.description)) # Extract the structure attributes

    try:
      # Table to display structure of selected mysql table
      x, y = len(self.results), len(self.results[0])
      self.table = QTableWidget(x, y)
      self.table.setHorizontalHeaderLabels(headers)
      self.table.horizontalHeader().setStyleSheet("color: black;")


      for i in range(x):
        for j in range(y):
          item = self.results[i][j]
          # Mysql returns some values as byte strings; convert to regular utf-8
          if type(item) is bytes: 
            cell = QTableWidgetItem(str(item, 'utf-8'))
          else:
            cell = QTableWidgetItem(str(item))

          cell.setFlags(Qt.ItemFlag.ItemIsEnabled)
          self.table.setItem(i, j, cell)

      self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
      self.table.setStyleSheet("QTableWidget::item { background-color: #f0f0f0; }")
      self.layout.addWidget(self.table)
      
    except Exception as e:
      dialog = MessageDialog(str(e), error=True)
      dialog.exec()
