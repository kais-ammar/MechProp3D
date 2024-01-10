import warnings
warnings.simplefilter("ignore")
import os, sys
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QFrame, QApplication, QVBoxLayout
from MechProp3D.FE_gui import Play_toolbar, font_toolbar, Scalarbar_toolbar, MechProp3D_widget, warning_msg
import pyvista as pv
from pyvistaqt import QtInteractor
from typing import Optional
field = ["young","shear","poisson","compressiblity"]
                                             
""" Main Class to create GUI Interface viewer"""
class MechProp3D(QMainWindow):
    def __init__(self, application, **kwargs):        
        super(MechProp3D, self).__init__(None)
        self._app = application
        self.main_widget = MechProp3D_widget()  
        frame = QFrame()
        vlayout = QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)                  
        self.plotter = QtInteractor(self)
        self.plotter.set_background(color='paraview')                       
        vlayout.addWidget(self.plotter.interactor) 
        vlayout.addWidget(self.main_widget)                                           
        frame.setLayout(vlayout)   
        self.type_plot = "young"        
        self.camera_info = dict()                
        self.setCentralWidget(frame)                 
        self.ipath = os.path.dirname(__file__)
        self.setWindowTitle("MechProp3D")  
        self.setWindowIcon(QIcon(os.path.join(self.ipath,'icons/3D_parameter.png')))       
        self.Play_toolbar()                        
        self.font_toolbar = font_toolbar(self)        
        self.addToolBar(self.font_toolbar)   
        self.Scalarbar_toolbar = Scalarbar_toolbar()        
        self.addToolBar(Qt.RightToolBarArea,self.Scalarbar_toolbar)                          
        self.resize(1300, 1000)
        #self.showMaximized()        
        self.Scalarbar_toolbar.Scalarbar_width.valueChanged.connect(self.slider_moved)
        self.Scalarbar_toolbar.Scalarbar_height.valueChanged.connect(self.slider_moved)
        self.Scalarbar_toolbar.Scalarbar_xpos.valueChanged.connect(self.slider_moved)
        self.Scalarbar_toolbar.Scalarbar_ypos.valueChanged.connect(self.slider_moved)
        QMetaObject.connectSlotsByName(self)   
             
    def Play_toolbar(self):    
        self.toolbar_draw = Play_toolbar()        
        self.addToolBar(self.toolbar_draw)                      
        self.toolbar_draw.button_young.triggered.connect(self.draw_3D_field)
        self.toolbar_draw.button_shear.triggered.connect(self.draw_3D_field)
        self.toolbar_draw.button_poisson.triggered.connect(self.draw_3D_field)
        self.toolbar_draw.button_compressiblity.triggered.connect(self.draw_3D_field)                
        self.toolbar_draw.button_Slice.triggered.connect(self.draw_3D_field)  
        self.toolbar_draw.button_take_screenshot.triggered.connect(self.takeScreenShot)  
        self.toolbar_draw.ISO.triggered.connect(lambda: self.draw_3D_field(True))                 
        self.toolbar_draw.button_vtk.triggered.connect(self.generate_vtk_file)           
        self.toolbar_draw.button_close.triggered.connect(self.close)

    def draw_3D_field(self,  view_iso: Optional[bool]=False):
        try:   
            self.plotter.add_axes(interactive=True, color=self.font_toolbar.txt_color) 
            self.plotter.clear()  
            if self.sender().text() in field:  
                self.type_plot = self.sender().text()                          
            self.var_name = self.Scalarbar_toolbar.champ_var.text()                                        
            self.main_widget.write3DPlotData_vtk(self.type_plot)   
            self.mesh = pv.read("%s/FE_gui/VTK_TEMP/%s.vtk"%(self.ipath,self.type_plot))             
        
            data = self.mesh.point_data["VARIABLE"]
            if(not self.Scalarbar_toolbar.champ_min.text()==''):
                Min_value = float(self.Scalarbar_toolbar.champ_min.text())
            else :
                Min_value = min(data)
            if(not self.Scalarbar_toolbar.champ_max.text()==''):
                Max_value = float(self.Scalarbar_toolbar.champ_max.text())
            else :
                Max_value = max(data)

            if (self.sender().text() == "Slice") :
                self.plotter.add_mesh_clip_box(self.mesh, show_edges=self.font_toolbar.Show_edge.isChecked(),  edge_color = self.font_toolbar.line_color, show_scalar_bar=False, cmap = self.font_toolbar.colorbar.currentText(), line_width=1, clim=[Min_value,Max_value]) #scalar_bar_args=sargs) 
                self.plotter.box_clipped_meshes  
            else :
                self.plotter.add_mesh(self.mesh, show_edges=self.font_toolbar.Show_edge.isChecked(), edge_color = self.font_toolbar.line_color, show_scalar_bar=False, cmap = self.font_toolbar.colorbar.currentText(), line_width=1, clim=[Min_value,Max_value]) #scalar_bar_args=sargs)                          
            if(not self.font_toolbar.Show_axes.isChecked()):
                self.plotter.hide_axes()
            
            orientation = False    
            if(self.Scalarbar_toolbar.orientation.currentText()=='vertical'):
                orientation = True
            if (self.font_toolbar.Show_colorbar.isChecked()):
                self.plotter.add_scalar_bar(title=self.var_name, n_labels=8, width=self.Scalarbar_toolbar.Scalarbar_width.value()/100., height=self.Scalarbar_toolbar.Scalarbar_height.value()/100., position_x=self.Scalarbar_toolbar.Scalarbar_xpos.value()/100., position_y=self.Scalarbar_toolbar.Scalarbar_ypos.value()/100., vertical=orientation, interactive=False, title_font_size=self.font_toolbar.font_size, label_font_size=self.font_toolbar.font_size, color=self.font_toolbar.txt_color, font_family=self.font_toolbar.font_family)                                                       
            if bool(self.camera_info.get("zoom")): 
                self.plotter.camera.zoom = self.camera_info['zoom']              
            self.camera_info['zoom'] = self.plotter.camera.zoom         
            if(view_iso):
                self.plotter.view_isometric()                             
        except Exception as err:
            warning_msg(str(err)) 
                                     
    def slider_moved(self, pos):                    
        if(self.sender().toolTip().startswith('Scalarbar')):
            if(self.font_toolbar.Show_colorbar.isChecked()): 
                self.plotter.remove_scalar_bar()
                orientation = False
                if(self.Scalarbar_toolbar.orientation.currentText()=='vertical'):
                    orientation = True                                
                if(self.sender().toolTip()=="Scalarbar_y_pos"):                                                                 
                    if ( self.font_toolbar.Show_colorbar.isChecked()):
                        self.Scalarbar_toolbar.Scalarbar_ypos_label.setText("Y pos: %d"%(pos))                        
                        self.plotter.add_scalar_bar(title=self.var_name, n_labels=8, width=self.Scalarbar_toolbar.Scalarbar_width.value()/100., height=self.Scalarbar_toolbar.Scalarbar_height.value()/100., position_x=self.Scalarbar_toolbar.Scalarbar_xpos.value()/100., position_y=pos/100., vertical=orientation, interactive=False, title_font_size=self.font_toolbar.font_size, label_font_size=self.font_toolbar.font_size, color=self.font_toolbar.txt_color, font_family=self.font_toolbar.font_family)                                                
                if(self.sender().toolTip()=="Scalarbar_x_pos"):
                    if ( self.font_toolbar.Show_colorbar.isChecked()):
                        self.Scalarbar_toolbar.Scalarbar_xpos_label.setText("X pos: %d"%(pos))
                        self.plotter.add_scalar_bar(title=self.var_name, n_labels=8, width=self.Scalarbar_toolbar.Scalarbar_width.value()/100., height=self.Scalarbar_toolbar.Scalarbar_height.value()/100., position_x=pos/100., position_y=self.Scalarbar_toolbar.Scalarbar_ypos.value()/100., vertical=orientation, interactive=False, title_font_size=self.font_toolbar.font_size, label_font_size=self.font_toolbar.font_size, color=self.font_toolbar.txt_color, font_family=self.font_toolbar.font_family)
                if(self.sender().toolTip()=="Scalarbar_width"):
                    if ( self.font_toolbar.Show_colorbar.isChecked()):
                        self.Scalarbar_toolbar.width_label.setText("width: %d"%(pos))
                        self.plotter.add_scalar_bar(title=self.var_name, n_labels=8, width=pos/100., height=self.Scalarbar_toolbar.Scalarbar_height.value()/100., position_x=self.Scalarbar_toolbar.Scalarbar_xpos.value()/100., position_y=self.Scalarbar_toolbar.Scalarbar_ypos.value()/100., vertical=orientation, interactive=False, title_font_size=self.font_toolbar.font_size, label_font_size=self.font_toolbar.font_size, color=self.font_toolbar.txt_color, font_family=self.font_toolbar.font_family) 
                if(self.sender().toolTip()=="Scalarbar_height"):
                    if ( self.font_toolbar.Show_colorbar.isChecked()):
                        self.Scalarbar_toolbar.height_label.setText("height: %d"%(pos))
                        self.plotter.add_scalar_bar(title=self.var_name, n_labels=8, width=self.Scalarbar_toolbar.Scalarbar_width.value()/100., height=pos/100., position_x=self.Scalarbar_toolbar.Scalarbar_xpos.value()/100., position_y=self.Scalarbar_toolbar.Scalarbar_ypos.value()/100., vertical=orientation, interactive=False, title_font_size=self.font_toolbar.font_size, label_font_size=self.font_toolbar.font_size, color=self.font_toolbar.txt_color, font_family=self.font_toolbar.font_family)            
                          
    def takeScreenShot(self):
        """ Save the scene as image. """
        try: 
            fname = QFileDialog.getSaveFileName(self, 'Open File', None, "Image files (*.jpg *.png)")[0]
            if fname:
                if not len(fname.split('.')) == 2:
                    fname += '.png'
                self.plotter.screenshot(fname,transparent_background=False)
        except Exception as err:
            warning_msg(str(err))                                     
                      
    def generate_vtk_file(self):
        try: 
            fname = QFileDialog.getSaveFileName(self, 'Open File', None, "Vtk file (*.vtk)")[0]    
            if fname:
                if not len(fname.split('.')) == 2:
                    fname += '.vtk'                                
            self.mesh.save(fname)            
        except Exception as err:
            warning_msg(str(err))                      
                      
    def closeEvent(self, event):
        os.system("rm -Rf %s/VTK_TEMP"%self.ipath)
        self.plotter.deep_clean()     
        self.plotter.closeEvent(event)
        pv.close_all()

def main():
    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x to run.\n")
        sys.exit(1)
    app = QApplication(sys.argv)         
    s3d = MechProp3D(app)
    s3d.show()
    sys.exit(app.exec_())
