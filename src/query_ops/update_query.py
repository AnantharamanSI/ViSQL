from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QComboBox, QLineEdit
from utils import get_tables, get_table_attributes, update_data
from components import ConditionsBox 

class UpdateQueries(QWidget):
  '''Update query to update tables'''
  def __init__(self, con):
    super().__init__()
    self.cur = con.cursor()

    # Layout is very similar to select queries layout, with similar utility functions
    layout = QVBoxLayout()


    heading = QLabel("Update Data")
    heading.setAccessibleName("heading")
    layout.addWidget(heading)

    about_this_page = """Let's learn how to find update data in a table!\n
    1) Select a table from the drop-down menu.
    2) Suppose we want to update all employees who worked in Austin to now work in SF.
    3) We would set the "Location" attribute to "SF"
    4) We would create a condition that checks if the Location attribute = "Austin"
    6) Click "Run Query" and a pop up stating that the update success status.

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

    layout_att = QHBoxLayout()

    self.att_dropdown = QComboBox()
    self.att_dropdown.setDisabled(True)
    self.update_value = QLineEdit()

    layout_att.addWidget(QLabel("Set Attribute: "))
    layout_att.addWidget(self.att_dropdown)
    layout_att.addWidget(QLabel("To"))
    layout_att.addWidget(self.update_value)

    self.conditions_box = ConditionsBox()

    self.btn_query = QPushButton("Run Query")
    self.btn_query.clicked.connect(lambda: self.run_query())
    self.btn_query.setDisabled(True)

    layout.addLayout(layout_table)
    layout.addLayout(layout_att)
    layout.addWidget(self.conditions_box)
    layout.addWidget(self.btn_query)
    self.setLayout(layout)


  def table_activated(self):
    self.btn_query.setDisabled(False)
    self.att_dropdown.setDisabled(False)
    self.att_dropdown.clear()

    table = self.table_dropdown.currentText()
    self.all_attributes = list(get_table_attributes(self.cur, table))
    self.conditions_box.attributes = self.all_attributes.copy()
    self.att_dropdown.addItems(self.all_attributes)
    
  def run_query(self):
    table = self.table_dropdown.currentText()
    attribute = self.att_dropdown.currentText()
    value = self.update_value.text()
    conditions = self.conditions_box.conditions.copy()
    update_data(self.cur, table, attribute, value, conditions)
    
  def close(self):
    self.con.close()
    super().close()
