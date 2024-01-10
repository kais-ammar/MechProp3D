from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QSlider,  QToolBar
from .gui_tools import GComboBox, GLabel, GLineEdit_Float, GLineEdit

class Scalarbar_toolbar(QToolBar):
    def __init__(self):
        super().__init__()              
        self.setWindowTitle("Scalar Bar options")
        self.setStatusTip("Scalar Bar options")
        self.initUI()
        self.setMovable(False)              
        self.addWidget(self.Label_ScalarBar)  
        self.addWidget(self.frame_ScalarBar) 
        self.addSeparator()  
        self.addWidget(self.label_var)        
        self.addWidget(self.champ_var)           
        self.addWidget(self.label_max)        
        self.addWidget(self.champ_max)           
        self.addWidget(self.label_min)        
        self.addWidget(self.champ_min)             
                        
    def initUI(self):                    
        self.orientation = GComboBox(V1='vertical', V2='horizontal', tooltip="Scroll/Click to select Scalarbar orientation")        
        self.orientation.setCurrentIndex(0)               
        self.Scalarbar_width = QSlider(Qt.Horizontal)
        self.Scalarbar_width.setToolTip("Scalarbar_width")        
        self.Scalarbar_height = QSlider(Qt.Horizontal)
        self.Scalarbar_height.setToolTip("Scalarbar_height")        
        self.Scalarbar_width.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.Scalarbar_height.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.Scalarbar_width.setValue(8)        
        self.Scalarbar_height.setValue(82)
        self.Scalarbar_xpos = QSlider(Qt.Horizontal)
        self.Scalarbar_xpos.setToolTip("Scalarbar_x_pos")                
        self.Scalarbar_ypos = QSlider(Qt.Horizontal)
        self.Scalarbar_ypos.setToolTip("Scalarbar_y_pos")                
        self.Scalarbar_xpos.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.Scalarbar_ypos.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.Scalarbar_xpos.setValue(86)        
        self.Scalarbar_ypos.setValue(7)
        self.Scalarbar_xpos_label = GLabel("X pos: %d"%self.Scalarbar_xpos.value())       
        self.Scalarbar_ypos_label = GLabel("Y pos: %d"%self.Scalarbar_ypos.value())
        self.width_label = GLabel("width: %d"%self.Scalarbar_width.value())
        self.height_label = GLabel("height: %d"%self.Scalarbar_height.value())        
        self.Label_ScalarBar = GLabel("Scalar Bar:")         
        self.frame_ScalarBar = QFrame()  
        self.frame_ScalarBar.setFixedWidth(130)
        self.frame_ScalarBar.setFrameShadow(QFrame.Plain)
        self.frame_ScalarBar.setLineWidth(1)
        self.frame_ScalarBar.setFrameShape(QFrame.Box)
        self.frame_ScalarBar.setObjectName("frame")           
        self.label_max = GLabel("Max Value:") 
        self.champ_max = GLineEdit_Float()
        self.label_min = GLabel("Min Value:") 
        self.champ_min = GLineEdit_Float()             
        self.label_var = GLabel("Variable:") 
        self.champ_var = GLineEdit()                                             
        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.orientation)                          
        self.Vbox.addWidget(self.Scalarbar_xpos_label)
        self.Vbox.addWidget(self.Scalarbar_xpos)
        self.Vbox.addWidget(self.Scalarbar_ypos_label)
        self.Vbox.addWidget(self.Scalarbar_ypos)  
        self.Vbox.addWidget(self.width_label)
        self.Vbox.addWidget(self.Scalarbar_width)        
        self.Vbox.addWidget(self.height_label)        
        self.Vbox.addWidget(self.Scalarbar_height)     
        self.frame_ScalarBar.setLayout(self.Vbox)