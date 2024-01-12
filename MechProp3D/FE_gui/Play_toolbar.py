import os
from PyQt5.QtCore import QSize  
from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtGui import QIcon

class Play_toolbar(QToolBar):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Play ToolBar")        
        self.initUI()
        self._createActions()

    def initUI(self):
        ipath = os.path.dirname(__file__)
        self.button_young = QAction(QIcon(os.path.join(ipath, '../icons/E.png')), "young", self)
        self.button_young.setStatusTip("young")
        self.button_shear = QAction(QIcon(os.path.join(ipath, '../icons/shear.png')), "shear", self)
        self.button_shear.setStatusTip("shear")
        self.button_poisson = QAction(QIcon(os.path.join(ipath, '../icons/nu.png')), "poisson", self)
        self.button_poisson.setStatusTip("poisson")
        self.button_compressiblity = QAction(QIcon(os.path.join(ipath, '../icons/comp.png')), "compressiblity", self)
        self.button_compressiblity.setStatusTip("compressiblity")
        self.button_Slice = QAction(QIcon(os.path.join(ipath, '../icons/slice.png')), "Slice", self)        
        self.button_Slice.setStatusTip("Slice")                    
        self.ISO = QAction(QIcon(os.path.join(ipath, '../icons/iso.ico')), "ISO view", self)
        self.ISO.setStatusTip("ISO_view")        
        self.button_take_screenshot = QAction(QIcon(os.path.join(ipath, '../icons/take_screen.ico') ), "Take Screen", self)
        self.button_take_screenshot.setStatusTip("Take Screenshot")        
        self.button_vtk = QAction(QIcon(os.path.join(ipath, '../icons/vtk.svg')), "generate a vtk file for the selected map", self)
        self.button_vtk.setStatusTip("generate vtk file")                  
        self.button_close = QAction(QIcon(os.path.join(ipath, '../icons/close.ico') ), "Close widget", self)
        self.button_close.setStatusTip("Close widget")
               
    def _createActions(self):
        self.setIconSize(QSize(30, 30))
        self.setMovable(True)
        self.addAction(self.button_young)
        self.addAction(self.button_shear)
        self.addAction(self.button_poisson)  
        self.addAction(self.button_compressiblity)
        self.addAction(self.button_Slice)        
        self.addAction(self.button_take_screenshot)
        self.addAction(self.button_vtk)  
        self.addAction(self.button_close)   
        self.addAction(self.ISO)                                 
