# CSS styling for all pages

queryStyles = '''
  QLabel {
    border-radius: 4px;
    border-width: 1px;
    height: 20px;
    padding: 4px 4px 4px 4px;
    font-size: 12px;
    font-family: consolas, sans-serif;
  }
  
  QLabel[accessibleName="heading"] {
    border-radius: 4px;
    background: #FFFFFF;
    /* padding: 4px 4px 4px 4px; */
    font-size: 18px;
    height: 12px;
    font-family: consolas, sans-serif;
  }

  QLabel[accessibleName="aboutme"] {
    border-radius: 4px;
    background: #FFFFFF;
    padding: 4px 4px 4px 4px;
    font-size: 14px;
    font-family: consolas, sans-serif;
  }
  
  QRadioButton {
    background: #b1f2ef;
  }
  QVBoxLayout {
    background: #ffffff;
    width: 400px;
  }
  QPushButton {
    padding: 4px 4px 4px 4px;
    background: #f2bbb8;
  }
  QComboBox {
    background: #C1D1FD;
  }
  QLineEdit {
    background: #F2E8B1
  }
  QRadioButton { 
    margin: 6px;
  }
'''


homeStyles = '''
  QWidget {
    background: #b1f2ef;
  }
  QLabel {
    background: #8cffba;
    border-radius: 10px;
    border-style: solid;
    border-width: 2px;
    padding: 20px 20px 20px 20px;
    font-size: 64px;
    font-family: consolas, sans-serif;
  }
  QVBoxLayout {
    background: #ffffff;
    width: 400px;
  }
  QMenu {
    background: #D4D4D4;
  }
  QMenu::item:selected {
    background: #395D93;
  }
  QMenuBar::item:selected {
    background: #23395B;
    color: #ffffff;
  }
'''

dialogStyles = {
    'success': "QDialog { background: #8ACB88; }",
    'error': "QDialog { background: #FE5F55; }",
  }