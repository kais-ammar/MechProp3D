import os, sys
import numpy as np
from PyQt5.QtWidgets import  QFrame, QVBoxLayout, QGridLayout
from .gui_tools import GLineEdit_Float, GLabel, warning_msg
from MechProp3D.Script import GENERATE_PLOT3D, write3DPlotData_vtk

"""  FE GUI viewer, using pyvista's QtInteractor class."""
class MechProp3D_widget(QFrame):
    def __init__(self, parent=None):
        super(MechProp3D_widget, self).__init__(parent)               
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.grid_input_tensor = QGridLayout()      
        self.list_champs=[]
        for line in range(6): 
            nvline = [] 
            for col in range(6): 
                label_ = GLabel("C%d%d:"%((line+1),(col+1)))
                champ = GLineEdit_Float()
                nvline.append(label_) 
                nvline.append(champ) 
            self.list_champs.append(nvline)         

        for i in range(6):
            for j in range(i,6):        
                self.grid_input_tensor.addWidget(self.list_champs[i][2*j]   ,i, 2*j,   1, 1)               
                self.grid_input_tensor.addWidget(self.list_champs[i][2*j+1] ,i, 1+2*j, 1, 1)       
        self.grid_botton = QGridLayout()      
        vbox.addLayout(self.grid_input_tensor)   
        vbox.addLayout(self.grid_botton)
        
        matrix = np.array([[184.88,	67.96,	83.44,	0.00,	0.00,	0.00],
                           [0.00,	184.88,	83.44,	0.00,	0.00,	0.00],
                           [0.00,	0.00,	395.18,	0.00,	0.00,	0.00],
                           [0.00,	0.00,	0.00,	76.50,	0.00,	0.00],
                           [0.00,	0.00,	0.00,	0.00,	76.50,	0.00],
                           [0.00,	0.00,	0.00,	0.00,	0.00,	9.89]])
                           
        for i in range(6):
            for j in range(i, 6):
                self.list_champs[i][2*j+1].setText(str(matrix[i][j]))
          
    def write3DPlotData_vtk(self,type_plot):    
        try:                                         
            matrix = np.empty((6, 6), dtype=np.float32)
            for i in range(6):
                for j in range(i,6):
                    matrix[i][j] = float(self.list_champs[i][2*j+1].text()) 
                    if(not i == j):       
                        matrix[j][i] = float(self.list_champs[i][2*j+1].text()) 
            print("********************************")
            print("The elasticity tensor=")
            for i in range(6):
                string = ""
                for j in range(6):
                    string += "%f  "%matrix[i][j]
                print(string)
            print("********************************")
            dataX, dataY, dataZ, dataR = GENERATE_PLOT3D(matrix, type_plot) 
            ipath = os.path.dirname(__file__)     
            os.system("rm -Rf %s/VTK_TEMP"%ipath)             
            os.system("mkdir -p %s/VTK_TEMP"%ipath)                    
            write3DPlotData_vtk("%s/VTK_TEMP/%s"%(ipath,type_plot), dataX, dataY, dataZ, dataR)
        except Exception as err:
            warning_msg(str(err)) 