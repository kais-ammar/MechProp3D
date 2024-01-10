import matplotlib as mpl
import numpy as np
from PyQt5.QtCore import QPointF, QRect, QSize, Qt
from PyQt5.QtGui import QFont, QPixmap, QPainter, QLinearGradient, QColor, QBrush, QIcon, QPen
from PyQt5.QtWidgets import QLineEdit, QToolBar, QAction, QToolButton, QMenu, QColorDialog, QActionGroup, QStyle
from .gui_tools import GComboBox, warning_msg
import os  

CMAPS = ['jet', 'hot', 'viridis', 'plasma','Greys', 'Blues', 'Greens', 'Reds', 'gray', 'Spectral', 'seismic', 'Set3', 'terrain', 
         'rainbow', 'YlOrRd', 'magma', 'PuBuGn', 'BuGn', 'YlOrBr', 'YlGn', 'autumn', 'winter', 'copper', 'turbo', 'gnuplot']
colors = ["black","white","red","blue","green","yellow","cyan","magenta"]
font_size_list = [6,7,8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,32,36,40]

def createline(cmaps=colors):
    """ Generator to create icons shown in the comboboxes where the colormap is selected."""
    w = 60
    h = 20
    for cmap in cmaps:
        px = QPixmap(w, h)
        p = QPainter(px)
        gradient = QColor(cmap)
        brush = QBrush(gradient)
        p.fillRect(QRect(0, 0, w, h), brush)
        p.end()
        yield QIcon(px)

def createPixmap(cmaps=CMAPS):
    """ Generator to create icons shown in the comboboxes where the colormap is selected."""
    w = 60
    h = 20
    for cmap in cmaps:
        cMap = mpl.cm.get_cmap(cmap)
        px = QPixmap(w, h)
        p = QPainter(px)
        gradient = QLinearGradient(QPointF(0, 0), QPointF(w, 0))
        for t in np.linspace(0., 1., 15):
             rgba = cMap(t)
             gradient.setColorAt(
                t, QColor(rgba[0]*255, rgba[1]*255, rgba[2]*255))
        brush = QBrush(gradient)
        p.fillRect(QRect(0, 0, w, h), brush)
        p.end()
        yield QIcon(px), cmap

class font_toolbar(QToolBar):    
    def __init__(self, parent=None):
        super(font_toolbar, self).__init__(parent=parent)    
        self._parent = parent
        self.setWindowTitle("Font options")
        self.initUI()
        self._createActions()    
        self.line_color = 'black'
        self.txt_color = 'white'        
        self.font_size = 20
        self.font_family =  'courier'    
        self.actor_point_labels = None
                
    def initUI(self):               
        self.colorbar = GComboBox(tooltip="Scroll/Click to select color map")
        for icon, name in createPixmap():
            self.colorbar.addItem(icon, name)
            self.colorbar.setIconSize(QSize(40, 15))                
        ipath = os.path.dirname(__file__)        
        self.options = QToolButton()
        self.options.setText('')
        self.toolmenu_options = QMenu(self)        
        self.Show_colorbar = QAction('Show Scalar Bar',checkable=True, checked = True)
        self.toolmenu_options.addAction(self.Show_colorbar)        
        self.Show_edge = QAction('Show Edges',checkable=True, checked = True)
        self.toolmenu_options.addAction(self.Show_edge)        
        self.Show_axes = QAction('Show Axes',checkable=True, checked = True)
        self.toolmenu_options.addAction(self.Show_axes)          

        self.options.setMenu(self.toolmenu_options)
        self.options.setPopupMode(QToolButton.InstantPopup)        
        self.options.setIcon(QIcon(os.path.join(ipath, '../icons/settings-solid.svg')))             
        self.button_backgroundcolor = QToolButton()
        self.button_backgroundcolor.setText('')
        self.toolmenu = QMenu(self)        
        self.Paraview_color = QAction('Paraview Background (Default)')
        self.toolmenu.addAction(self.Paraview_color)        
        self.Warm_Gray_color = QAction('Warm Gray Background')
        self.toolmenu.addAction(self.Warm_Gray_color)        
        self.Neutral_Gray_color = QAction('Neutral Gray Background')
        self.toolmenu.addAction(self.Neutral_Gray_color)          
        self.Light_Gray_color = QAction('Light Gray Background')
        self.toolmenu.addAction(self.Light_Gray_color)  
        self.Black_color = QAction('Black Background')
        self.toolmenu.addAction(self.Black_color)                  
        self.While_color = QAction('While Background')
        self.toolmenu.addAction(self.While_color)                  
        self.Edit_color_palette = QAction('Edit Current Palette ...')
        self.toolmenu.addAction(self.Edit_color_palette)                                 
        self.button_backgroundcolor.setMenu(self.toolmenu)
        self.button_backgroundcolor.setPopupMode(QToolButton.InstantPopup)        
        self.button_backgroundcolor.setIcon(QIcon(os.path.join(ipath, '../icons/background_icon.ico'))) 
        
        self.button_line_color = QToolButton()
        self.button_line_color.setText('line_color')
        self.toolmenu1 = QMenu(self)
        self.group = QActionGroup(self.toolmenu1)
        size = self.style().pixelMetric(QStyle.PM_LargeIconSize)
        for color in colors:        
            pm = QPixmap(size, size) # create a pixmap based on the default size, "clear" its content (this is *very* important, otherwise the pixmap will use random data based on memory dump
            pm.fill(Qt.transparent)            
            qp = QPainter(pm) # create a QPainter for the pixmap, set the pen color and draw a line  placed in the middle using that color
            pen = QPen(QColor(color), 5, Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(0, size / 2, size, size / 2)            
            qp.end() # end painting on the pixmap, this is important also!                        
            action = QAction(QIcon(pm), color, self) # create the action with an icon based on the pixmap
            action.setCheckable(True)
            self.group.addAction(action)            
            self.toolmenu1.addAction(action)
        action = QAction('Edit Palette')
        self.group.addAction(action)            
        self.toolmenu1.addAction(action)
        self.button_line_color.setMenu(self.toolmenu1)
        self.button_line_color.setPopupMode(QToolButton.InstantPopup)      

        pm = QPixmap(size, size) # create a pixmap based on the default size, "clear" its content (this is *very* important, otherwise the pixmap will use random data based on memory dump
        pm.fill(Qt.transparent)          
        qp = QPainter(pm)
        pen = QPen(Qt.black, 5, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(0, size/2, size, size/2)
        qp.end()     
        self.button_line_color.setIcon(QIcon(pm))                    
        self.button_line_color.triggered.connect(self.choose_color)
        self.button_txt_color = QToolButton()
        self.button_txt_color.setText('txt_color')
        self.tool_txt_color = QMenu(self)
        self.group_txt_color = QActionGroup(self.tool_txt_color)
        font = QFont()
        font.setFamily("Tahoma")
        font.setPixelSize(30)
        font.setBold(True)         
        for color in colors:        
            pm = QPixmap(size, size) # create a pixmap based on the default size, "clear" its content (this is *very* important, otherwise the pixmap will use random data based on memory dump
            pm.fill(Qt.transparent)            
            qp = QPainter(pm) # create a QPainter for the pixmap, set the pen color and draw a line  placed in the middle using that color            
            pen = QPen(QColor(color), 5, Qt.SolidLine)
            qp.setPen(pen)
            qp.setFont(font)         
            qp.drawText(1*size/4,  0.8*size, "A")
            qp.end() # end painting on the pixmap, this is important also!                        
            action = QAction(QIcon(pm), color, self) # create the action with an icon based on the pixmap
            action.setCheckable(True)
            self.group_txt_color.addAction(action)            
            self.tool_txt_color.addAction(action)
        action = QAction('Edit Palette')
        self.group_txt_color.addAction(action)            
        self.tool_txt_color.addAction(action)
        self.button_txt_color.setMenu(self.tool_txt_color)
        self.button_txt_color.setPopupMode(QToolButton.InstantPopup)  
        
        pm = QPixmap(size, size) # create a pixmap based on the default size, "clear" its content (this is *very* important, otherwise the pixmap will use random data based on memory dump
        pm.fill(Qt.transparent)          
        qp = QPainter(pm)
        pen = QPen(Qt.black, 5, Qt.SolidLine)
        qp.setFont(font)         
        qp.drawText(1*size/4,  0.8*size, "A")
        qp.end()     
        self.button_txt_color.setIcon(QIcon(pm)) 

        self.button_font_family = GComboBox(V1='arial', V2='courier', V3='times', tooltip="Scroll/Click to select font family")        
        self.button_font_family.setCurrentIndex(2)                               
        self.button_font_size = GComboBox(tooltip="Scroll/Click to select font size")        
        for sz in font_size_list:
            self.button_font_size.addItem("%d pt"%sz)            
        self.button_font_size.setFixedWidth(75)            
        self.button_font_size.setLineEdit(QLineEdit()) 
        self.button_font_size.setCurrentIndex(12)     
                          
        self.button_txt_color.triggered.connect(self.choose_color)          
        self.Edit_color_palette.triggered.connect(self.onColorPicker)  
        self.Paraview_color.triggered.connect(self.onColorPicker)  
        self.Warm_Gray_color.triggered.connect(self.onColorPicker)  
        self.Neutral_Gray_color.triggered.connect(self.onColorPicker)  
        self.Light_Gray_color.triggered.connect(self.onColorPicker)  
        self.Black_color.triggered.connect(self.onColorPicker)  
        self.While_color.triggered.connect(self.onColorPicker)          
        self.button_font_family.currentTextChanged.connect(self.font_family_cliked)  
        self.button_font_size.currentTextChanged.connect(self.font_size_cliked)        

    def font_family_cliked(self):
        self.font_family = self.button_font_family.currentText()        
        
    def font_size_cliked(self):
        font_size = self.button_font_size.currentText().split()[0]
        try:
            self.font_size = int(font_size)
        except ValueError:
            self.font_size = 20
        
    def _createActions(self):
        self.setIconSize(QSize(20, 20))
        self.setMovable(True)
        self.addWidget(self.colorbar)         
        self.addWidget(self.button_font_family)  
        self.addWidget(self.button_font_size)  
        self.addWidget(self.options)           
        self.addWidget(self.button_backgroundcolor)           
        self.addWidget(self.button_line_color)  
        self.addWidget(self.button_txt_color)   

    def choose_color(self, action):   
        try:             
            if(action.text() == 'Edit Palette'):
                dlg = QColorDialog(self)   # setting current color 
                dlg.setCurrentColor(QColor("#52576E"))    # default color: Paraview Background  
                dlg.exec_()   
                value = dlg.currentColor()        
                rgb_color = (value.red(),value.green(),value.blue())
            else :
                rgb_color = action.text()            
            if(self.sender().text()=='txt_color'):
                self.txt_color = rgb_color           
            elif(self.sender().text()=='line_color'):
                self.line_color = rgb_color
        except Exception as err:
            warning_msg(str(err))  
            
    def onColorPicker(self):
        try:             
            '''  Show color-picker dialog to select color. Qt will use the native dialog by default.'''
            if(self.sender().text() == 'Paraview Background (Default)'):
                value = QColor("#52576E")       
                rgb_color = (value.red(),value.green(),value.blue()) 
            elif(self.sender().text() == 'Warm Gray Background'):   
                value = QColor("#4A4542")       
                rgb_color = (value.red(),value.green(),value.blue())             
            elif(self.sender().text() == 'Neutral Gray Background'): 
                value = QColor("#6B6B6B")       
                rgb_color = (value.red(),value.green(),value.blue())             
            elif(self.sender().text() == 'Light Gray Background'):   
                value = QColor("#75706B")       
                rgb_color = (value.red(),value.green(),value.blue())             
            elif(self.sender().text() == 'Black Background'):        
                rgb_color = "black"             
            elif(self.sender().text() == 'While Background'):        
                rgb_color = "white"             
            else :        
                dlg = QColorDialog(self)   # setting current color 
                dlg.setCurrentColor(QColor("#52576E"))    # default color: Paraview Background  
                dlg.exec_()   
                value = dlg.currentColor()        
                rgb_color = (value.red(),value.green(),value.blue())
            self._parent.plotter.set_background(color=rgb_color)
        except Exception as err:
            warning_msg(str(err))                