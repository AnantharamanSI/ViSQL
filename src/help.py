from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from server import *
from styles import dialogStyles

help_msg = f'''
Hello and welcome to ViSQL! 

This tool allows you to interact with a SQL database (DB) using a GUI and teaches you SQL commands as you go along!

1. Accessing a DB
    + The title of the ViSQL window indicates whether a DB has been selected or not.
    + If the message reads (NO DATABASE SELECTED), please select Database Functions > sql5692815.
    + To create a DB, click Create Database in the same dropdown.
        - NOTE: You will not be able to create a DB unless you have a local SQL server!

2. History of all queries performed
    + A log of all queries performed can be found in the visql_log.txt

3. Data Input Format
    + For varchar and datetime data types, enter the values surrounded by "quotes".
    + Example: For conditions of relational type, a comparison of a varchar attribute must be done as shown:
        - <attribute> | <operator> | "string", eg: name = "monty python"

MySQL metadata
    + host: {host}
    + user: {user}

'''

class Help(QDialog):
  '''Dialog to display the help page'''
  def __init__(self):
    super().__init__()
    layout = QVBoxLayout()
    layout.addWidget(QLabel(help_msg))
    self.setWindowTitle('User Guide')
    self.setLayout(layout)    