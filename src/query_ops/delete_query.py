from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QComboBox
from utils import get_tables, get_table_attributes, delete_rows, MessageDialog
from styles import *
from components import Table, ConditionsBox 

  
class DeleteData(QWidget):
  '''Delete data from tables'''
  def __init__(self, con):
    super().__init__()
    self.con = con
    self.cur = con.cursor()

    # Layout is very similar to select queries layout, with similar utility functions
    layout = QVBoxLayout()

    heading = QLabel("Delete")
    heading.setAccessibleName("heading")
    layout.addWidget(heading)

    about_this_page = """Let's learn how to delete rows from a table in our database!\n
    1) Select a table from the drop-down menu.
    2) You can also add deletion conditions! For example, if you want to delete rows where col="Abel" or id=1, you can add these conditions.
    3) Click "Delete Rows" and a pop up will appear with the appropriate columns of the table.

    Remember to check the visql_log.txt file to see the SQL command that would have the same impact!
    """

    about_pg = QLabel(about_this_page)
    about_pg.setAccessibleName("aboutme")
    layout.addWidget(about_pg)
    

    layout_table = QHBoxLayout()
    table_title = QLabel("Table: ")
    self.table_dropdown = QComboBox()
    self.table_dropdown.addItems(get_tables(self.cur))
    self.table_dropdown.activated.connect(self.table_activated)
    self.table_dropdown.setPlaceholderText('--selection--')
    self.table_dropdown.setCurrentIndex(-1)

    layout_table.addWidget(table_title)
    layout_table.addWidget(self.table_dropdown)
    
    self.conditions_box = ConditionsBox()

    # TODO: Disable button when no text in table
    self.btn_delete = QPushButton("Delete Rows")
    self.btn_delete.clicked.connect(lambda: self.run_delete())
    self.btn_delete.setDisabled(True)

    layout.addLayout(layout_table)
    layout.addWidget(self.conditions_box)
    layout.addWidget(self.btn_delete)

    self.setLayout(layout)


  def table_activated(self):
    self.btn_delete.setDisabled(False)
    table = self.table_dropdown.currentText()
    self.conditions_box.attributes = list(get_table_attributes(self.cur, table))

  def run_delete(self):
    table = self.table_dropdown.currentText()
    conditions = self.conditions_box.conditions
    delete_rows(self.con, table, conditions)
    

class NaturalJoin(QWidget):
  '''Join 2 tables'''
  def __init__(self, con):
    super().__init__()
    self.cur = con.cursor()

    layout = QVBoxLayout()

    heading = QLabel("Natural Join")
    heading.setAccessibleName("heading")
    layout.addWidget(heading)

    about_this_page = """Let's learn how to join tables!\n
    1) Select two tables from the drop-down menu.
    2) Click "Join" and a pop up will display the contents of the merged tables.

    Remember to check the visql_log.txt file to see the SQL command that would have the same impact!
    """

    about_pg = QLabel(about_this_page)
    about_pg.setAccessibleName("aboutme")
    layout.addWidget(about_pg)
    
    sublayout = QHBoxLayout()
    
    tables = list(get_tables(self.cur))
    
    # Sublayouts to select the 2 tables to join
    table_title_1 = QLabel("Table 1: ")
    self.table_dropdown_1 = QComboBox()
    self.table_dropdown_1.addItems(tables)

    table_title_2 = QLabel("Table 2: ")
    self.table_dropdown_2 = QComboBox()
    self.table_dropdown_2.addItems(tables)


    sublayout.addWidget(table_title_1)
    sublayout.addWidget(self.table_dropdown_1)
    sublayout.addWidget(table_title_2)
    sublayout.addWidget(self.table_dropdown_2)
    
    btn = QPushButton("Join")
    btn.clicked.connect(self.run_query)
    
    layout.addWidget(QLabel("Select tables to join."))
    layout.addLayout(sublayout)
    layout.addWidget(btn)
    
    self.setLayout(layout)

  def run_query(self):
    table_1 = self.table_dropdown_1.currentText()
    table_2 = self.table_dropdown_2.currentText()
    
    if table_1 == table_2 or table_1 == '' or table_2 == '':
      dialog = MessageDialog("Please select different tables", error=True)
      dialog.exec()
      return
    
    show_table = Table(self.cur, table_1, other_table=table_2, join=True)
    show_table.exec()
    