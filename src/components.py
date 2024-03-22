from PyQt6.QtWidgets import QWidget, QDialog, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QAbstractItemView
from PyQt6.QtCore import Qt
import mysql.connector as connector
from utils import create_database, get_data, natural_join, group_by_data, aggregate, MessageDialog
from styles import *

class CreateDb(QDialog):
  '''Dialog to create a new database'''
  def __init__(self):
    super().__init__()

    self.setWindowTitle('Create Database')
    mainlayout = QVBoxLayout()
    sublayout = QHBoxLayout()

    self.label = QLabel("Enter database name: ")
    self.edit = QLineEdit()
    self.push = QPushButton("Create")
    self.push.clicked.connect(self.create_db) # run the database creation query

    # Error field in case the name of the database is invalid
    self.error = QLabel()

    sublayout.addWidget(self.label)
    sublayout.addWidget(self.edit)
    sublayout.addWidget(self.push)

    mainlayout.addLayout(sublayout)
    mainlayout.addWidget(self.error)

    self.setLayout(mainlayout)

  def create_db(self):
    name = self.edit.text() # Get database name

    # Check if name is a valid attribute name (follows the same rules as python identifiers)
    if name.isidentifier():
      try:
        create_database(name)
        # self.edit.hide()
        # self.push.hide()
        # self.error.hide()
        # self.label.hide()
        self.close()
      except connector.errors.DatabaseError: 
        self.error.setText("A database with that name already exists.")
    else:
      self.error.setText("Invalid database name!")


class Table(QDialog):
  '''Dialog with table to display results of all queries'''
  def __init__(self, cursor, table, attributes=None, conditions=None, order_by=None, join=False, other_table=None, group_by=False, func=None, attribute=None, group_by_attr=None):
    super().__init__()
    self.showMaximized()
    self.setWindowTitle('Table Output')
    layout = QVBoxLayout()
    if not join and not group_by and attributes:
      # Normal select query
      self.results = get_data(cursor, table, attributes, conditions, order_by)
    elif join:
      # Natural join query
      self.results = natural_join(cursor, table, other_table)
    elif group_by and attribute:
      # Group by aggregate function query
      self.results = group_by_data(cursor, table, func, attribute, conditions, group_by_attr)
    elif attribute:
      # Group by aggregate function query
      self.results = aggregate(cursor, table, func, attribute, conditions)
    
    # Get attribute names for table headers
    des = cursor.description
    attributes = list(map(lambda x: x[0], des))
    
    try:
      # Populate table with results
      x, y = len(self.results), len(self.results[0])
      self.table = QTableWidget(x, y)
      self.table.setHorizontalHeaderLabels(attributes)
      self.table.horizontalHeader().setStyleSheet("color: black;")


      for i in range(x):
        for j in range(y):
          cell = QTableWidgetItem(str(self.results[i][j]))
          cell.setFlags(Qt.ItemFlag.ItemIsEnabled)
          self.table.setItem(i, j, cell)

      self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
      self.table.setStyleSheet("QTableWidget::item { background-color: #f0f0f0; }")
      layout.addWidget(self.table)
      self.setLayout(layout)
    except:
      dialog = MessageDialog("No data in the table", error=True)
      dialog.exec()
      self.close()


class Condition(QDialog):
  def __init__(self, parent, attributes):
    super().__init__()
    self.parent = parent
    
    self.conditions = ['Relational', 'List', 'Regex', 'Is Null', "Is Not Null"]
    
    # Choose the type of condition to add
    self.select_condition = QComboBox()
    self.select_condition.addItems(self.conditions)
    # Toggle between different types of conditions
    self.select_condition.activated.connect(self.condition_selected)
    self.select_condition.setPlaceholderText('--selection--')
    self.select_condition.setCurrentIndex(-1)

    # Attributes of table for current query
    atts = attributes
    self.layout = QVBoxLayout()

    # Attribute dropdowns
    self.combo_boxes = [QComboBox() for _ in range(5)]
    for box in self.combo_boxes:
      box.addItems(atts)

    self.widgets = [QWidget() for _ in range(5)]
    layouts = [QHBoxLayout() for _ in range(5)]
    
    # Layout for comparisons
    self.comparators = QComboBox()
    compare = ['=', '!=', '<', '>', '<=', '>=']
    self.comparators.addItems(compare)
    self.compare_value = QLineEdit()
    
    layouts[0].addWidget(self.combo_boxes[0])
    layouts[0].addWidget(self.comparators)
    layouts[0].addWidget(self.compare_value)
    
    
    # Layouts for is null, is not null
    layouts[3].addWidget(self.combo_boxes[3])
    layouts[4].addWidget(self.combo_boxes[4])
    
    # Layout for in
    layouts[1] = QVBoxLayout()
    sublayout = QHBoxLayout()
    sublayout.addWidget(QLabel("Enter Value: "))
    self.cur_value = QLineEdit()
    self.add_value_btn = QPushButton("Add Value")
    self.add_value_btn.clicked.connect(self.add_value)
    sublayout.addWidget(self.cur_value)
    sublayout.addWidget(self.add_value_btn)
    
    self.selected_values = []
    self.values = QLabel()
    self.clear_values_btn = QPushButton("Clear All Values")
    self.clear_values_btn.clicked.connect(self.clear_values)
    
    self.combo_boxes[1].activated.connect(self.clear_values)
    layouts[1].addWidget(self.combo_boxes[1])
    layouts[1].addLayout(sublayout)
    layouts[1].addWidget(self.values)
    layouts[1].addWidget(self.clear_values_btn)
    
    
    # Layout for regex
    layouts[2].addWidget(self.combo_boxes[2])
    self.regex = QLineEdit()
    layouts[2].addWidget(QLabel("Regex: "))
    layouts[2].addWidget(self.regex)
    
    # Add all sublayouts to subwidgets
    for i in range(5):
      self.widgets[i].setLayout(layouts[i])
      self.widgets[i].hide()

    self.cur_layout = None

    self.btn = QPushButton("Add condition")
    self.btn.clicked.connect(self.add_condition)

    self.layout.addWidget(QLabel("Select condition type:"))
    self.layout.addWidget(self.select_condition)
    
    # Add all subwidets to main layout
    for widget in self.widgets:
      self.layout.addWidget(widget)

    self.layout.addWidget(self.btn)
    self.setLayout(self.layout)

  def condition_selected(self):
    # Toggle between layouts for various types of conditions
    if self.cur_layout is not None:
      self.widgets[self.cur_layout].hide()
    self.cur_layout = self.select_condition.currentIndex()

    self.widgets[self.cur_layout].show()

  def add_condition(self):
    attr = self.combo_boxes[self.cur_layout].currentText()
    condition = None
    
    # Format condition for query
    if self.cur_layout == 0:
      condition = f'{attr} {self.comparators.currentText()} {self.compare_value.text()}'
    elif self.cur_layout == 1:
      condition = f'{attr} in ({self.values.text()})'
    elif self.cur_layout == 2:
      condition = f'{attr} like {self.regex.text()}'
    elif self.cur_layout == 3:
      condition = f'{attr} is null'
    elif self.cur_layout == 4:
      condition = f'{attr} is not null'
    
    # Update parent component
    self.parent.conditions.append(condition)
    cur = self.parent.display_conditions.text()
    new = f'{cur}, {condition}' if cur else condition
    self.parent.display_conditions.setText(new)

    self.close()
  
  def add_value(self):
    # Utility function for in operator
    value = self.cur_value.text()
    if value in self.selected_values:
      return

    self.selected_values.append(value)
    cur = self.values.text()
    new = f'{cur}, {value}' if cur != 'No values added.' else value
    self.values.setText(new)
    self.cur_value.setText("")
  
  def clear_values(self):
    # Utility function for in operator
    self.selected_values.clear()
    self.values.setText('No values added.') 
    

class ConditionsBox(QWidget):
  '''Component to add conditions to query'''
  def __init__(self):
    super().__init__()
    self.conditions = []
    self.attributes = None
    
    btn_condition = QPushButton("Add Condition")
    btn_condition.clicked.connect(self.add_condition)
    
    self.display_conditions = QLabel()
    self.reset_conditions = QPushButton("Remove all conditions")
    self.reset_conditions.clicked.connect(self.call_reset_conditions)
    
    layout = QVBoxLayout()
    layout.addWidget(btn_condition)
    layout.addWidget(self.display_conditions)
    layout.addWidget(self.reset_conditions)
    self.setLayout(layout)

  def call_reset_conditions(self):
    self.display_conditions.setText("")
    self.conditions.clear()

  def add_condition(self):
    if self.attributes is not None:
      dialog = Condition(self, self.attributes)
      dialog.exec()
    else:
      dialog = MessageDialog("Please select a table", error=True)
      dialog.exec()
      dialog.exec()
