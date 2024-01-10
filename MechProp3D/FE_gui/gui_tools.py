from PyQt5.QtWidgets import QPushButton, QLineEdit, QComboBox, QLabel, QCheckBox
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox

def warning_msg(message): 
    msg = QMessageBox()
    msg.setWindowTitle("Message Box") 
    font = QtGui.QFont()
    font.setFamily("Arial")
    font.setPointSize(12)  
    font.setBold(True)        
    msg.setFont(font)     
    msg.setText(message)     
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.Cancel)     
    msg.exec_() 

class GButton(QPushButton):
    def __init__(self, text:str =None, tooltip:str =None, checkable:bool =False, size:float =None):
        super(GButton, self).__init__(None)
        self.setText(text)
        self.setToolTip(tooltip)
        self.setCheckable(checkable)
        if size is not None:
            self.setFixedSize(*size)
        self.setStyleSheet("QPushButton { min-height: 40px; max-height: 40px; min-width: 150px; max-width: 150px;}");                          

class GComboBox(QComboBox):
    def __init__(self, tooltip:str=None, index:int=0, **field):
        super(GComboBox, self).__init__(None)
        self.setToolTip(tooltip)
        self.setStyleSheet("QComboBox { background-color: rgb(249, 255, 255); selection-background-color: rgb(53, 107, 255); }"); 
        for value in field.values():
            self.addItem(value) 
        self.setCurrentIndex(index)    
                
class GCheckBox(QCheckBox):
    def __init__(self, text:str =None, tooltip:str=None,  checkable:bool =False,  Checked:bool =False):
        super(GCheckBox, self).__init__(None)
        self.setToolTip(tooltip)
        self.setText(text)
        self.setCheckable(checkable)
        self.setChecked(Checked)

class GLineEdit_Float(QLineEdit):
    def __init__(self, tooltip:str =None, ReadOnly:bool =False):
        super(GLineEdit_Float, self).__init__(None)
        dbl_validator = QRegExpValidator(QRegExp("[+-]?\d+(\.\d+)?[Ee][+-]?\d+"))
        self.setFixedWidth(130)  
        self.setToolTip(tooltip)
        self.setInputMethodHints(Qt.ImhNone)
        self.setValidator(dbl_validator)
        self.setReadOnly(ReadOnly) 
        
class GLineEdit(QLineEdit):
    def __init__(self, tooltip:str =None, ReadOnly:bool =False):
        super(GLineEdit, self).__init__(None)
        self.setFixedWidth(130)  
        self.setToolTip(tooltip)
        self.setInputMethodHints(Qt.ImhNone)
        self.setReadOnly(ReadOnly)        
               
class GLabel(QLabel):
    def __init__(self, text:str =None, tooltip:str =None):
        super(GLabel, self).__init__(None)
        self.setToolTip(tooltip)
        self.setText(text)               