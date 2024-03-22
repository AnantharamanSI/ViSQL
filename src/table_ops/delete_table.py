from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QComboBox
import mysql.connector as connector
from utils import get_tables, delete_table
from server import *

from styles import queryStyles

class DeleteTable(QWidget):
  '''Delete table from database'''
  def __init__(self, db):
    super().__init__()
    self.con = connector.connect(host=host, password=session, user=user, database=db)
    self.cur = self.con.cursor()
    layout = QVBoxLayout()
    
    heading = QLabel("Delete Table")
    heading.setAccessibleName("heading")
    layout.addWidget(heading)

    about_this_page = """Let's learn how to delete a table from our database!\n
    1) Select a table from the drop-down menu.
    2) Click on "Delete Table".
    3) You will see a pop-up confirming the deletion of the table. Close the pop-up and proceed.

    Remember to check the visql_log.txt file to see the SQL command that would have the same impact!
    """

    about_pg = QLabel(about_this_page)
    about_pg.setAccessibleName("aboutme")
    layout.addWidget(about_pg)

    # Dropdown to select table to be deleted
    layout_table = QHBoxLayout()
    table_title = QLabel("Table: ")
    self.table_dropdown = QComboBox()
    self.table_dropdown.addItems(get_tables(self.cur))
    self.table_dropdown.activated.connect(self.table_activated)
    self.table_dropdown.setPlaceholderText('--selection--')
    self.table_dropdown.setCurrentIndex(-1)

    layout_table.addWidget(table_title)
    layout_table.addWidget(self.table_dropdown)

    self.delete_table_btn = QPushButton("Delete Table")
    self.delete_table_btn.setDisabled(True)
    self.delete_table_btn.clicked.connect(self.delete_table)
    
    layout.addLayout(layout_table)
    layout.addWidget(self.delete_table_btn)

    self.setLayout(layout)
    self.setMinimumSize(750, 500)
    self.setStyleSheet(queryStyles)

    
  def table_activated(self):
    self.delete_table_btn.setDisabled(False) # Allow deletion only once table selected

  def delete_table(self):
    table = self.table_dropdown.currentText()
    delete_table(self.cur, table)    
    
  def close(self):
    self.con.close()
    super().close()
