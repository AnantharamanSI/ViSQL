from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QComboBox
from utils import MessageDialog, get_tables, get_table_attributes
from components import Table, ConditionsBox 

class SelectQueries(QWidget):
  '''Create select query to get data from tables'''
  def __init__(self, con):
    super().__init__()
    self.cur = con.cursor()

    layout = QVBoxLayout()

    heading = QLabel("Select")
    heading.setAccessibleName("heading")
    layout.addWidget(heading)

    about_this_page = """Let's learn how to select columns to display from  a table from our database!\n
    1) Select a table from the drop-down menu.
    2) Now we need to select the attributes to display. You can "Add all attributes" or add attributes one by one using the "Add" button.
    3) You can remove attributes using the "Remove" button. You can also clear all attributes using the "Clear" button.
    4) You can also add conditions! For example, if you want to display rows where col="Abel" or id=1, you can add these conditions.
    5) Click "Run Query" and a pop up will appear with the appropriate columns of the table.

    Remember to check the visql_log.txt file to see the SQL command that would have the same impact!
    """

    about_pg = QLabel(about_this_page)
    about_pg.setAccessibleName("aboutme")
    layout.addWidget(about_pg)
    
    # Sublayout to select table
    layout_table = QHBoxLayout()
    table_title = QLabel("Table: ")
    self.table_dropdown = QComboBox()
    self.table_dropdown.addItems(get_tables(self.cur))
    # Allow selection of attributes only when table is selected
    self.table_dropdown.activated.connect(self.table_activated)
    self.table_dropdown.setPlaceholderText('--selection--')
    self.table_dropdown.setCurrentIndex(-1)

    self.all_attributes = []
    self.selected_attributes = []

    layout_table.addWidget(table_title)
    layout_table.addWidget(self.table_dropdown)

    # Sublayout to select attributes
    layout_att = QHBoxLayout()
    att_title = QLabel("Attributes: ")

    self.att_dropdown = QComboBox()
    self.att_dropdown.setDisabled(True)

    self.att_add = QPushButton("Add")
    self.att_add.clicked.connect(self.add_attribute)
    
    self.att_remove = QPushButton("Remove")
    self.att_remove.clicked.connect(lambda: self.remove_attribute())
    
    self.att_clear = QPushButton("Clear")
    self.att_clear.clicked.connect(lambda: self.clear_attributes())

    self.att_addAll = QPushButton("Add all attributes")
    self.att_addAll.clicked.connect(lambda: self.add_all_attributes())
    
    self.att_selected = QLabel("No attribtues selected.") # Display selected attributes

    layout_att.addWidget(att_title)
    layout_att.addWidget(self.att_dropdown)
    layout_att.addWidget(self.att_add)
    layout_att.addWidget(self.att_remove)
    layout_att.addWidget(self.att_clear)
    layout_att.addWidget(self.att_addAll)


    # Where clause functionality
    self.conditions_box = ConditionsBox()
    
    # Sublayout for order by clause
    layout_order = QHBoxLayout()
    layout_order.addWidget(QLabel("Sorted by: "))
    self.order_dropdown = QComboBox()
    self.order_dropdown.setDisabled(True)

    layout_order.addWidget(self.order_dropdown)

    # Run the final query
    self.btn_query = QPushButton("Run Query")
    self.btn_query.clicked.connect(self.run_query)
    self.btn_query.setDisabled(True)

    layout.addLayout(layout_table)
    layout.addLayout(layout_att)
    layout.addWidget(self.att_selected)
    layout.addWidget(self.conditions_box)
    layout.addLayout(layout_order)
    layout.addWidget(self.btn_query)

    self.setLayout(layout)

  def table_activated(self):
    # Allow selection of attributes only when table is selected
    self.btn_query.setDisabled(False)
    self.clear_attributes()
    self.att_dropdown.setDisabled(False)
    self.att_dropdown.clear()

    table = self.table_dropdown.currentText()
    
    self.all_attributes = list(get_table_attributes(self.cur, table))
    
    self.conditions_box.attributes = self.all_attributes.copy()
    self.att_dropdown.addItems(self.all_attributes)

    self.order_dropdown.setDisabled(False)
    self.order_dropdown.clear()

    self.all_attributes = list(get_table_attributes(self.cur, table))
    self.order_dropdown.addItem("None")
    self.order_dropdown.addItems(self.all_attributes)

  def add_attribute(self):
    attribute = self.att_dropdown.currentText()
    if attribute in self.selected_attributes:
      return

    self.selected_attributes.append(attribute)
    self.att_selected.setText("Attributes: " + ', '.join(self.selected_attributes))

  def remove_attribute(self):
    attribute = self.att_dropdown.currentText()
    if attribute not in self.selected_attributes:
      return
    self.selected_attributes.remove(attribute)
    if self.selected_attributes:
      self.att_selected.setText("Attributes: " + ', '.join(self.selected_attributes))
    else:
      self.att_selected.setText("No attribtues selected.")
  
  def clear_attributes(self):
    self.selected_attributes.clear()
    self.att_selected.setText('No attributes selected.')

  def add_all_attributes(self):
    self.selected_attributes = self.all_attributes.copy()
    self.att_selected.setText('All attributes selected.')

  def run_query(self):
    
    # Get data for query
    table = self.table_dropdown.currentText()
    attributes = self.selected_attributes
    conditions = self.conditions_box.conditions
    order_by = self.order_dropdown.currentText()
    if order_by in ['', 'None']:
      order_by = None

    if attributes:
      show_table = Table(self.cur, table, attributes, conditions, order_by)
      show_table.exec()
    else:
      error_dialog = MessageDialog("Please make sure the table and at least 1 attribute is selected.", error=True)
      error_dialog.exec()
