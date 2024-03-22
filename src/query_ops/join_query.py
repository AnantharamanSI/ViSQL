from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QComboBox
from utils import MessageDialog, get_tables
from components import Table 


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
    