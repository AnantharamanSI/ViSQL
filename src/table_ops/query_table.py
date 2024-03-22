from PyQt6.QtWidgets import *
from components import *

from utils import *
from server import *

from styles import queryStyles
from query_ops import join_query, select_query, delete_query, update_query, groupby_query


class QueryTables(QWidget):
  '''Querying operations on a table'''
  def __init__(self, db):
    super().__init__()

    self.con = connector.connect(host=host, password=session, user=user, database=db)
    layout = QVBoxLayout()

    # CHeckboxes for selecting table operation
    db_action_layout = QHBoxLayout()
    check1 = QRadioButton('Select')
    check1.toggled.connect(lambda:self.select_action(check1))
    check2 = QRadioButton('Update')
    check2.toggled.connect(lambda:self.select_action(check2))
    check3 = QRadioButton('Aggregate Functions')
    check3.toggled.connect(lambda:self.select_action(check3))
    check4 = QRadioButton('Delete')
    check4.toggled.connect(lambda:self.select_action(check4))
    check5 = QRadioButton('Natural Join')
    check5.toggled.connect(lambda:self.select_action(check5))

    db_action_layout.addWidget(check1)
    db_action_layout.addWidget(check2)
    db_action_layout.addWidget(check3)
    db_action_layout.addWidget(check4)
    db_action_layout.addWidget(check5)

    # Fetch components
    self.select_layout = select_query.SelectQueries(self.con)
    self.update_layout = update_query.UpdateQueries(self.con)
    self.group_layout = groupby_query.GroupBy(self.con)
    self.delete_layout = delete_query.DeleteData(self.con)
    self.join_layout = join_query.NaturalJoin(self.con)

    layout.addLayout(db_action_layout)
    layout.addWidget(self.select_layout)
    layout.addWidget(self.update_layout)
    layout.addWidget(self.group_layout)
    layout.addWidget(self.delete_layout)
    layout.addWidget(self.join_layout)

    self.setLayout(layout)
    self.setMinimumSize(750, 500)
    self.setStyleSheet(queryStyles)

    self.select_layout.hide()
    self.update_layout.hide()
    self.group_layout.hide()
    self.delete_layout.hide()
    self.join_layout.hide()

    # default to select table
    check1.setChecked(True)

  def select_action(self, b):
    # Shows page corresponding to operation selected
    if b.text() == "Select":
      if b.isChecked():
        self.select_layout.show()
      else:
        self.select_layout.hide()
        
    elif b.text() == "Update":
      if b.isChecked():
        self.update_layout.show()
      else:
        self.update_layout.hide()
        
    elif b.text() == "Aggregate Functions":
      if b.isChecked():
        self.group_layout.show()
      else:
        self.group_layout.hide()
        
    elif b.text() == "Delete":
      if b.isChecked():
        self.delete_layout.show()
      else:
        self.delete_layout.hide()
        
    elif b.text() == "Natural Join":
      if b.isChecked():
        self.join_layout.show()
      else:
        self.join_layout.hide()
        
        
  def close(self):
    self.con.close()
    super().close()
