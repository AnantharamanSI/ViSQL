from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QComboBox
from utils import get_tables, get_table_attributes
from components import Table, ConditionsBox 

class GroupBy(QWidget):
  '''Group by queries for aggregate functions'''
  def __init__(self, con):
    super().__init__()
    self.cur = con.cursor()

    # Layout is very similar to select queries layout, with similar utility functions
    layout = QVBoxLayout()

    heading = QLabel("GroupBy and Aggregation")
    heading.setAccessibleName("heading")
    layout.addWidget(heading)

    about_this_page = """Let's learn how to find statistics and aggregate data!\n
    1) Select a table from the drop-down menu.
    2) Suppose we had a table where we want to find the max age of people in a table. Ley's say we want to group them by the city they live in and ensure that they are taller than 5ft.
    3) We would select the "max" function for the "Age" attribute.
    4) We could set a condition where "height" > 5.
    5) We would group the data by the "City" attribute.
    6) Click "Run Query" and a pop up will appear with the appropriate columns of the table.

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
    att_title = QLabel("Function: ")

    self.agg_function = QComboBox()
    functions = ['max', 'min', 'avg', 'sum', 'count', 'count(*)']
    self.agg_function.addItems(functions)
    self.agg_function.setDisabled(True)
    
    self.att_dropdown = QComboBox()
    self.att_dropdown.setDisabled(True)

    layout_att.addWidget(att_title)
    layout_att.addWidget(self.agg_function)
    layout_att.addWidget(self.att_dropdown)


    # Where functionality
    self.conditions_box = ConditionsBox()
    
    layout_group = QHBoxLayout()
    layout_group.addWidget(QLabel("Grouped by: "))
    self.group_dropdown = QComboBox()
    self.group_dropdown.setDisabled(True)

    layout_group.addWidget(self.group_dropdown)

    # TODO: Disable button when no text in table
    self.btn_query = QPushButton("Run Query")
    self.btn_query.clicked.connect(lambda: self.run_query())
    self.btn_query.setDisabled(True)

    layout.addLayout(layout_table)
    layout.addLayout(layout_att)
    layout.addWidget(self.conditions_box)
    layout.addLayout(layout_group)
    layout.addWidget(self.btn_query)
    self.setLayout(layout)


  def table_activated(self):
    
    self.btn_query.setDisabled(False)
    self.agg_function.setDisabled(False)
    self.att_dropdown.setDisabled(False)
    self.att_dropdown.clear()

    table = self.table_dropdown.currentText()
    self.all_attributes = list(get_table_attributes(self.cur, table))
    self.conditions_box.attributes = self.all_attributes.copy()
    self.att_dropdown.addItems(self.all_attributes)

    self.group_dropdown.setDisabled(False)
    self.group_dropdown.clear()

    self.all_attributes = list(get_table_attributes(self.cur, table))
    self.group_dropdown.addItems(self.all_attributes)

    
  def run_query(self):
    table = self.table_dropdown.currentText()
    attribute = self.att_dropdown.currentText()
    func = self.agg_function.currentText()
    conditions = self.conditions_box.conditions
    group_by = self.group_dropdown.currentText()
    
    table = Table(self.cur, table, group_by=True, func=func, attribute=attribute, conditions=conditions, group_by_attr=group_by)
    table.exec()
