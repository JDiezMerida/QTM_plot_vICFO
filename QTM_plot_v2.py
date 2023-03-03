# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 16:29:38 2019

@author: Jaime Diez Merida
"""

from PyQt5 import QtWidgets, QtCore,QtGui

import sys
import general_plotting_v2
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
'''
Dummy class. Necessary to be able to add attributes to the class object later
on.
'''
class Object():
    pass

'''Template values'''

template = 'QTM_templates/template_GUI.txt'
labels_temp='QTM_templates/labels_GUI.txt'
labels_dict={}
template_GUI = {}
labels=[]
#commands=np.loadtxt(filename)

with open(template) as fh:
    for line in fh:
        command= line.strip().split("\t")
        try:
            template_GUI[command[0]] = command[1]
        except IndexError:
            template_GUI[command[0]] = ''
with open(labels_temp) as fh:
    for line in fh:
        command= line.strip().split("\t")
        labels.append(command[0])
        if command[0]=='G in S':
            conduct_index=len(labels)
        elif command[0]=='G in eh':
            eh_index=len(labels)
            
        try:
            labels_dict[command[0]] = command[1]
        except IndexError:
            labels_dict[command[0]] = ''
#print(template_GUI)
#print(command[0])
data_direct=template_GUI['data_directory']
template_direct=template_GUI['template_directory']
custom_direct=template_GUI['customized_directory']
#print(labels_dict)
#%%

'''This creates a window with different options'''
class App(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.title = 'QTM plot data'
        '''This defines the position and size of the window'''
        self.left = int(template_GUI['left'])
        self.top = int(template_GUI['top'])
        self.width = int(template_GUI['width'])
        self.height =int(template_GUI['height'])
        window_icon=QtGui.QIcon()
        window_icon.addFile('QTM_images/spin_logo.png')
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(window_icon)
        
        self.initUI()
        '''call the widget with the tabs'''
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        
        
        self.show()
        
    def initUI(self):

        '''This creates the menu on top, it is not necessary to have it
            It will add all the menu tasks that you add below'''
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
        
        '''This adds subbuttons to the menus'''
        exitButton = QtWidgets.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
        
        add_dataButton = QtWidgets.QAction(QtGui.QIcon('Add.png'), 'Add data', self)
        add_dataButton.setShortcut('Ctrl+A')
        editMenu.addAction(add_dataButton)
        
        '''Open the open file system '''
        openfileButton = QtWidgets.QAction(QtGui.QIcon('openfile.png'),'Open file',self)
        openfileButton.setShortcut('Ctrl+F')
        openfileButton.triggered.connect(self.openFileNameDialog)
        fileMenu.addAction(openfileButton)

        
    def openFileNameDialog(self):
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                #print(fileName)
                dataset=fileName
                
                #dataset=dataset
            return dataset
    
    def openFileNamesDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
    
    def saveFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

'''Now create the class for the tabs. This is the most important part
    since all the Widgets are included in this window, which is then added
    to the main App above'''
    
class MyTableWidget(QtWidgets.QWidget):
    
    def __init__(self, parent):
               
        super(QtWidgets.QWidget, self).__init__(parent)
        
       # '''Initial values for the code from template'''
       # '''Accept drops''' 
       # self.setAcceptDrops(True)
        
        self.data_direct=template_GUI['data_directory']
        self.template_direct=template_GUI['template_directory']
        self.custom_direct=template_GUI['customized_directory']
        self.x_axis=template_GUI['x_axis']
        self.y_axis=template_GUI['y_axis']
        self.z_axis=template_GUI['z_axis']
        self.title=template_GUI['title']
        self.cmap=template_GUI['cmap']
        self.makemap_bool=False
        if template_GUI['extent']=='True':
            self.extent_bool=True
        else:
            self.extent_bool=False
        
        self.x_axis2=template_GUI['x_axis2']
        self.y_axis2=template_GUI['y_axis2']
        self.z_axis2=template_GUI['z_axis2']
        self.cmap2=template_GUI['cmap2']
        self.title2=template_GUI['title2']
        if template_GUI['extent2']=='True':
            self.extent_bool2=True
        else:
            self.extent_bool2=False
        self.x_line=int(template_GUI['verline'])
        self.y_line=int(template_GUI['horline'])
        self.conversion_x=template_GUI['x_conversion']
        self.conversion_y=template_GUI['y_conversion']
        self.conversion_z=template_GUI['z_conversion']
        self.conversion_x2=template_GUI['x_conversion2']
        self.conversion_y2=template_GUI['y_conversion2']
        self.conversion_z2=template_GUI['z_conversion2']
        self.x_label=labels_dict[template_GUI['x_label']]
        self.y_label=labels_dict[template_GUI['y_label']]
        self.z_label=labels_dict[template_GUI['z_label']]
        self.x_label2=labels_dict[template_GUI['x_label2']]
        self.y_label2=labels_dict[template_GUI['y_label2']]
        self.z_label2=labels_dict[template_GUI['z_label2']]
        self.offset=template_GUI['offset']
        self.offset_hor=template_GUI['offset_hor']
        self.offset_ver=template_GUI['offset_ver']
        
        if template_GUI['conductance']=='True':
            self.conduct_bool=True
        else:
            self.conduct_bool=False
            
        if template_GUI['conductance2']=='True':
            self.conduct_bool2=True
        else:
            self.conduct_bool2=False
            
        if template_GUI['eh']=='True':
            self.eh_bool=True
        else:
            self.eh_bool=False
            
        if template_GUI['eh2']=='True':
            self.eh_bool2=True
        else:
            self.eh_bool2=False
            
        if template_GUI['labels']=='True':
            self.labels_bool=True
        else:
            self.labels_bool=False
            
        if template_GUI['labels2']=='True':
            self.labels_bool2=True
        else:
            self.labels_bool2=False

        if template_GUI['legend']=='True':
            self.legend_bool=True
        else:
            self.legend_bool=False
            
        self.normalize_y_bool=False
        self.normalize_z_bool=False
        
        
        '''THINGS FOR TAB 1: Raw data plotting'''
        
        '''Import the plotting CLass defined below'''
        self.plotwidget = PlotWidget() 
        self.pop_error_nofile = PopError_nofile()
        self.pop_error_wrongfile = PopError_wrongfile()
        self.pop_error_wrongtemplate = PopError_wrongtemplate()
        
        '''Creates all the buttons and widgets which allow to modify the data'''
        self.databutton = QtWidgets.QPushButton('Dataset')
        self.databutton.setFixedWidth(200)
        self.databutton.clicked.connect(self.openFileName)
        self.newdata_label = QtWidgets.QLabel('Fix')
        self.separator_data=QtWidgets.QFrame()
        self.newdata_box=QtWidgets.QCheckBox()

        self.data_layout=QtWidgets.QHBoxLayout()
        self.data_layout.addWidget(self.databutton)
        self.data_layout.addWidget(self.separator_data)
        self.data_layout.addWidget(self.newdata_label)
        self.data_layout.addWidget(self.newdata_box)
   
                
        self.template_button = QtWidgets.QPushButton('Template load')
        self.template_button.clicked.connect(self.import_template)
        self.template_button.setFixedWidth(200)
        
        self.separator_loading=QtWidgets.QFrame()
        self.customload_button = QtWidgets.QPushButton('Custom load')
        self.customload_button.clicked.connect(self.custom_load)
        self.customload_button.setFixedWidth(150)
        self.customsave_button = QtWidgets.QPushButton('Custom save')
        self.customsave_button.clicked.connect(self.custom_save)
        self.customsave_button.setFixedWidth(150)
        
        self.loading_layout=QtWidgets.QHBoxLayout()
        self.loading_layout.addWidget(self.customload_button)
        self.data_layout.addWidget(self.separator_loading)
        self.loading_layout.addWidget(self.customsave_button)
        
        
        
        '''Pop up a window with the figure shown at the moment'''
        self.Popup_button=QtWidgets.QPushButton('Pop up figure')
        self.Popup_button.clicked.connect(self.popup_figure)
        self.popup_label = QtWidgets.QLabel('Pin')
        self.popupbox=QtWidgets.QCheckBox()
        self.separator_pop=QtWidgets.QFrame()
        self.popup_frame= QtWidgets.QGroupBox()
        self.popup_label_frame= QtWidgets.QGroupBox()
        self.clear_button=QtWidgets.QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear_graph)
        popup_layout = QtWidgets.QHBoxLayout()
        popup_layout.addWidget(self.Popup_button)
        popup_layout.addWidget(self.separator_pop)
        popup_layout.addWidget(self.popup_label)
        popup_layout.addWidget(self.popupbox) 
        popup_layout.addWidget(self.clear_button)
        self.popup_frame.setLayout(popup_layout)
        self.counter=0
        self.pop_dict={}
    
    
        '''Make a box to store the label and combobox in one line'''
        
        self.x_axis_label = QtWidgets.QLabel('x axis')
        self.x_axis_box = QtWidgets.QComboBox()
        self.x_axis_box.addItem('')
        self.x_label_label=QtWidgets.QLabel('x label')
        self.x_label_check=QtWidgets.QCheckBox()
        self.labels_bool=False
        self.x_label_box=QtWidgets.QComboBox()
        self.x_label_box.addItems(labels)
        self.x_conversion_label=QtWidgets.QLabel('Conversion')
        self.x_conversion_box=QtWidgets.QLineEdit()
        self.x_conversion_box.setFixedWidth(50)
        
        
        
        
        
        self.x_axis_frame= QtWidgets.QGroupBox()
        x_axis_total_layout = QtWidgets.QHBoxLayout()
        x_axis_layout=QtWidgets.QVBoxLayout()
        x_tick_layout=QtWidgets.QHBoxLayout()
        x_label_layout=QtWidgets.QVBoxLayout()
        x_conversion_layout=QtWidgets.QVBoxLayout()
        
        x_axis_layout.addWidget(self.x_axis_label)
        x_axis_layout.addWidget(self.x_axis_box) 
        x_tick_layout.addWidget(self.x_label_label)
        x_tick_layout.addWidget(self.x_label_check)
        x_label_layout.addLayout(x_tick_layout)
        x_label_layout.addWidget(self.x_label_box) 
        x_conversion_layout.addWidget(self.x_conversion_label)
        x_conversion_layout.addWidget(self.x_conversion_box) 
        x_axis_total_layout.addLayout(x_axis_layout)
        x_axis_total_layout.addLayout(x_label_layout)
        x_axis_total_layout.addLayout(x_conversion_layout)
        self.x_axis_frame.setLayout(x_axis_total_layout)
        #self.xlabelsbox.addItems(axisoptions)

        '''Make a box to store the label and combobox in one line'''
        self.y_axis_label = QtWidgets.QLabel('y axis')
        self.y_axis_box = QtWidgets.QComboBox()
        self.y_axis_box.addItem('')
        self.y_label_label=QtWidgets.QLabel('y label')
        self.y_label_box=QtWidgets.QComboBox()
        self.y_label_box.addItems(labels)
        self.y_conversion_label=QtWidgets.QLabel('Conversion')
        self.y_conversion_box=QtWidgets.QLineEdit()
        self.y_conversion_box.setFixedWidth(50)
        self.normalize_y=QtWidgets.QLabel('Normalize by')
        self.normalize_y_box=QtWidgets.QComboBox()
        self.normalize_y_tick=QtWidgets.QCheckBox()
        
        self.y_axis_frame= QtWidgets.QGroupBox()
        y_axis_total_layout = QtWidgets.QHBoxLayout()
        y_axis_layout=QtWidgets.QVBoxLayout()
        y_label_layout=QtWidgets.QVBoxLayout()
        y_conversion_layout=QtWidgets.QVBoxLayout()
        y_axis_layout.addWidget(self.y_axis_label)
        y_axis_layout.addWidget(self.y_axis_box) 
        y_axis_layout.addWidget(self.normalize_y)
        y_label_layout.addWidget(self.y_label_label)
        y_label_layout.addWidget(self.y_label_box) 
        y_label_layout.addWidget(self.normalize_y_box)
        y_conversion_layout.addWidget(self.y_conversion_label)
        y_conversion_layout.addWidget(self.y_conversion_box) 
        y_conversion_layout.addWidget(self.normalize_y_tick)
        y_axis_total_layout.addLayout(y_axis_layout)
        y_axis_total_layout.addLayout(y_label_layout)
        y_axis_total_layout.addLayout(y_conversion_layout)
        self.y_axis_frame.setLayout(y_axis_total_layout)
        
        '''Make a box to store the label and combobox in one line'''
        
        self.z_axis_label = QtWidgets.QLabel('z axis')
        self.z_axis_box = QtWidgets.QComboBox()
        self.z_axis_box.addItem('')
        self.z_label_label=QtWidgets.QLabel('z label')
        self.z_label_box=QtWidgets.QComboBox()
        self.z_label_box.addItems(labels)
        self.z_conversion_label=QtWidgets.QLabel('Conversion')
        self.z_conversion_box=QtWidgets.QLineEdit()
        self.z_conversion_box.setFixedWidth(50)
        self.normalize_z=QtWidgets.QLabel('Normalize by')
        self.normalize_z_box=QtWidgets.QComboBox()
        self.normalize_z_tick=QtWidgets.QCheckBox()
        
        '''Full box'''
        self.z_axis_frame= QtWidgets.QGroupBox()
        '''How it will be divided'''
        z_axis_total_layout = QtWidgets.QHBoxLayout()
        z_axis_layout=QtWidgets.QVBoxLayout()
        z_label_layout=QtWidgets.QVBoxLayout()
        z_conversion_layout=QtWidgets.QVBoxLayout()
        '''Now each of the divisions''' 
        z_axis_layout.addWidget(self.z_axis_label)
        z_axis_layout.addWidget(self.z_axis_box)
        z_axis_layout.addWidget(self.normalize_z)
        '''Now each of the divisions''' 
        z_label_layout.addWidget(self.z_label_label)
        z_label_layout.addWidget(self.z_label_box) 
        z_label_layout.addWidget(self.normalize_z_box)
        
        '''Now each of the divisions''' 
        z_conversion_layout.addWidget(self.z_conversion_label)
        z_conversion_layout.addWidget(self.z_conversion_box) 
        z_conversion_layout.addWidget(self.normalize_z_tick)
        '''Put it all together'''
        z_axis_total_layout.addLayout(z_axis_layout)
        z_axis_total_layout.addLayout(z_label_layout)
        z_axis_total_layout.addLayout(z_conversion_layout)
        self.z_axis_frame.setLayout(z_axis_total_layout)
        
        
        self.titlelabel= QtWidgets.QLabel('Title')
        self.titlebox = QtWidgets.QLineEdit()
        self.title_frame= QtWidgets.QGroupBox()
        
        
        self.legendlabel=QtWidgets.QLabel('Legend')
        self.legendbox=QtWidgets.QCheckBox()
        
        
        titlebox_layout = QtWidgets.QHBoxLayout()
        titlebox_layout.addWidget(self.titlelabel)
        titlebox_layout.addWidget(self.titlebox) 
        titlebox_layout.addWidget(self.legendbox)
        self.title_frame.setLayout(titlebox_layout)
        
        '''The update button can be triggered by enter key'''
        
        self.updatebutton = QtWidgets.QPushButton('UPDATE')
        self.updatebutton.setShortcut('Return') 
        self.updatebutton.clicked.connect(self.update_plot)
        
        
        self.cmap_label= QtWidgets.QLabel('Colormap')
        self.cmapbox = QtWidgets.QLineEdit()
        self.cmapbox.setFixedWidth(80)
        
        #self.cmap_frame= QtWidgets.QGroupBox()
        cmap_layout = QtWidgets.QHBoxLayout()
        cmap_layout.addWidget(self.cmap_label)
        cmap_layout.addWidget(self.cmapbox) 
        #self.cmap_frame.setLayout(cmap_layout)
        
        self.extent_label = QtWidgets.QLabel('Extent')
        self.extentbox=QtWidgets.QCheckBox()
        self.separator_ext=QtWidgets.QFrame()
        
        self.makemap_label=QtWidgets.QLabel('Make map')
        self.makemap_box=QtWidgets.QCheckBox()
        self.extent_frame= QtWidgets.QGroupBox()
        extent_layout = QtWidgets.QHBoxLayout()
        extent_layout.addWidget(self.extent_label)
        extent_layout.addWidget(self.extentbox)
        extent_layout.addWidget(self.separator_ext)
        extent_layout.addWidget(self.cmap_label)
        extent_layout.addWidget(self.cmapbox)
        extent_layout.addWidget(self.makemap_label)
        extent_layout.addWidget(self.makemap_box)
        self.extent_frame.setLayout(extent_layout)
        
        '''Box with the maximum and minimum options'''
        
        self.min_x_label = QtWidgets.QLabel('Min x')
        self.max_x_label = QtWidgets.QLabel('Max x')
        self.min_y_label = QtWidgets.QLabel('Min y')
        self.max_y_label = QtWidgets.QLabel('Max y')
        self.min_z_label = QtWidgets.QLabel('Min z')
        self.max_z_label = QtWidgets.QLabel('Max z')
        
        self.min_x_box=QtWidgets.QLineEdit()
        self.max_x_box=QtWidgets.QLineEdit()
        self.min_y_box=QtWidgets.QLineEdit()
        self.max_y_box=QtWidgets.QLineEdit()
        self.min_z_box=QtWidgets.QLineEdit()
        self.max_z_box=QtWidgets.QLineEdit()
        
        self.min_x_box.setFixedWidth(50)
        self.max_x_box.setFixedWidth(50)
        self.min_y_box.setFixedWidth(50)
        self.max_y_box.setFixedWidth(50)
        self.min_z_box.setFixedWidth(50)
        self.max_z_box.setFixedWidth(50)
        
        self.min_x_box.setText(str(0))
        self.max_x_box.setText(str(0))
        self.min_y_box.setText(str(0))
        self.max_y_box.setText(str(0))
        self.min_z_box.setText(str(0))
        self.max_z_box.setText(str(0))
        
        
        '''Make the frame for it''' 
        self.minmax_frame=QtWidgets.QGroupBox()
        
        minmax_layout = QtWidgets.QHBoxLayout()
        
        minmax_x_layout=QtWidgets.QVBoxLayout()
        
        min_x_layout=QtWidgets.QHBoxLayout()
        min_x_layout.addWidget(self.min_x_label)
        min_x_layout.addWidget(self.min_x_box)
        
        max_x_layout=QtWidgets.QHBoxLayout()
        max_x_layout.addWidget(self.max_x_label)
        max_x_layout.addWidget(self.max_x_box)
        
        minmax_y_layout=QtWidgets.QVBoxLayout()
        
        min_y_layout=QtWidgets.QHBoxLayout()
        min_y_layout.addWidget(self.min_y_label)
        min_y_layout.addWidget(self.min_y_box)
        
        max_y_layout=QtWidgets.QHBoxLayout()
        max_y_layout.addWidget(self.max_y_label)
        max_y_layout.addWidget(self.max_y_box)
        
        minmax_z_layout=QtWidgets.QVBoxLayout()
        
        min_z_layout=QtWidgets.QHBoxLayout()
        min_z_layout.addWidget(self.min_z_label)
        min_z_layout.addWidget(self.min_z_box)
        
        max_z_layout=QtWidgets.QHBoxLayout()
        max_z_layout.addWidget(self.max_z_label)
        max_z_layout.addWidget(self.max_z_box)
        
        minmax_x_layout.addLayout(min_x_layout)
        minmax_x_layout.addLayout(max_x_layout)
        
        minmax_y_layout.addLayout(min_y_layout)
        minmax_y_layout.addLayout(max_y_layout)
        
        minmax_z_layout.addLayout(min_z_layout)
        minmax_z_layout.addLayout(max_z_layout)
        
        minmax_layout.addLayout(minmax_x_layout)
        minmax_layout.addLayout(minmax_y_layout)
        minmax_layout.addLayout(minmax_z_layout)
        
        self.minmax_frame.setLayout(minmax_layout)
        
        ''' Lower box with conductance and offset '''
        
        self.conduct_label = QtWidgets.QLabel('Conductance')
        self.conduct_box=QtWidgets.QCheckBox()
        self.eh_label=QtWidgets.QLabel('Conductance quantum')
        self.eh_box=QtWidgets.QCheckBox()
        self.separator_postproc=QtWidgets.QFrame()
        self.postproc_frame= QtWidgets.QGroupBox()
        self.offset_label=QtWidgets.QLabel('Offset')
        self.offset_box=QtWidgets.QLineEdit()
        self.offset_box.setFixedWidth(80)
        self.offset_box.setText(self.offset)
        
        self.postproc_frame=QtWidgets.QGroupBox()
        postproc_layout = QtWidgets.QHBoxLayout()
        conduct_layout=QtWidgets.QVBoxLayout()
        conduct_layout1=QtWidgets.QHBoxLayout()
        conduct_layout1.addWidget(self.conduct_label)
        conduct_layout1.addWidget(self.conduct_box)
        
        conduct_layout2=QtWidgets.QHBoxLayout()
        conduct_layout2.addWidget(self.eh_label)
        conduct_layout2.addWidget(self.eh_box)
        
        conduct_layout.addLayout(conduct_layout1)
        conduct_layout.addLayout(conduct_layout2)
        postproc_layout.addLayout(conduct_layout)
        postproc_layout.addWidget(self.separator_postproc)
        postproc_layout.addWidget(self.offset_label)
        postproc_layout.addWidget(self.offset_box)
        self.postproc_frame.setLayout(postproc_layout)
        
        
        '''Match the widgets to triggers'''
        self.x_axis_box.activated.connect(self.onChanged_x)
        self.y_axis_box.activated.connect(self.onChanged_y)
        self.normalize_y_box.activated.connect(self.onChanged_normalize_y)
        self.normalize_y_tick.clicked.connect(self.onChanged_normalize_y_bool)
        
        self.z_axis_box.activated.connect(self.onChanged_z)
        self.normalize_z_box.activated.connect(self.onChanged_normalize_z)
        self.normalize_z_tick.clicked.connect(self.onChanged_normalize_z_bool)
        
        self.extentbox.clicked.connect(self.onChanged_extent)
        self.x_label_check.clicked.connect(self.onChanged_labels)
        self.x_label_box.activated.connect(self.onChanged_lx)
        self.y_label_box.activated.connect(self.onChanged_ly)
        self.z_label_box.activated.connect(self.onChanged_lz)
        self.conduct_box.clicked.connect(self.onChanged_conduct)
        self.eh_box.clicked.connect(self.onChanged_eh)
        self.legendbox.clicked.connect(self.onChanged_legend)
        self.makemap_box.clicked.connect(self.onChanged_makemap)
        
        
        '''create a frame with a vertical layout to organize the widgets
        Add all the widgets above there'''
        
        self.fitcontrolframe = QtWidgets.QGroupBox()
        fitcontrollayout = QtWidgets.QVBoxLayout()
        fitcontrollayout.addLayout(self.data_layout)
        fitcontrollayout.addWidget(self.template_button)
        fitcontrollayout.addLayout(self.loading_layout)
        for widget in (self.popup_frame,
                       self.x_axis_frame,
                       self.y_axis_frame,
                       self.z_axis_frame,
                       self.title_frame,
                       self.extent_frame,
                       self.minmax_frame,
                       self.postproc_frame,
                       self.updatebutton):
            fitcontrollayout.addWidget(widget)
        self.fitcontrolframe.setLayout(fitcontrollayout)
        
        '''Split the window in left for the plot and right for all the other
        widgets'''
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.plotwidget)
        splitter.addWidget(self.fitcontrolframe)
        
        
        '''Things for tab 2. Widgets cannot be repeated
        otherwise the code only shows them in one of the tabs. Therefore
        this is just importing and creating things like above but for the 2nd
        tab. All the things that repeat from tab 1 just include a 2 after
        the name'''
        
        '''Import the plotting class for the 2D + linescans below and right'''
        self.otherplot = PlotSeparate()
        
        self.databutton2 = QtWidgets.QPushButton('Dataset')
        self.databutton2.clicked.connect(self.openFileName2)
        
        #self.loadpopup_button = QtWidgets.QPushButton('Popup load')
        #self.loadpopup_button.clicked.connect(self.import_popup)
        #self.loadpopup_button.setFixedWidth(200)
        
        self.updatebutton2 = QtWidgets.QPushButton('UPDATE')
        #self.updatebutton2.setShortcut('Ctrl+U')
        self.updatebutton2.clicked.connect(self.update_plot2)
        
        '''Pop up a window with the figure shown at the moment'''
        '''Pop up a window with the figure shown at the moment'''
        self.Popup_left=QtWidgets.QPushButton('Pop up Horizontal')
        self.Popup_left.clicked.connect(self.popup_hor_prof)
        self.Popup_right=QtWidgets.QPushButton('Pop up Vertical')
        self.Popup_right.clicked.connect(self.popup_ver_prof)
        self.popup_label2 = QtWidgets.QLabel('Pin')
        self.popupbox2=QtWidgets.QCheckBox()
        self.popup_frame2= QtWidgets.QGroupBox()
        self.popup_label_frame2= QtWidgets.QGroupBox()
        popup_layout2 = QtWidgets.QHBoxLayout()
        popup_layout2.addWidget(self.Popup_left)
        popup_layout2.addWidget(self.Popup_right)
        popup_layout2.addWidget(self.popup_label2)
        popup_layout2.addWidget(self.popupbox2) 
        self.popup_frame2.setLayout(popup_layout2)
        self.counter2=0
        self.counter3=0
        self.pop_dict2={}
        self.pop_dict3={}
        

        self.x_axis_label2 = QtWidgets.QLabel('x axis')
        self.x_axis_box2 = QtWidgets.QComboBox()
        self.x_axis_box2.addItem('')
        self.x_label_label2=QtWidgets.QLabel('x label')
        self.x_label_box2=QtWidgets.QComboBox()
        self.x_label_box2.addItems(labels)
        self.x_label_check2=QtWidgets.QCheckBox()
        self.x_conversion_label2=QtWidgets.QLabel('Conversion')
        self.x_conversion_box2=QtWidgets.QLineEdit()
        self.x_conversion_box2.setFixedWidth(50)
        '''Make a box to store the label and combobox in one line'''
        self.x_axis_frame2= QtWidgets.QGroupBox()
        x_axis_total_layout2 = QtWidgets.QHBoxLayout()
        x_axis_layout2=QtWidgets.QVBoxLayout()
        x_tick_layout2=QtWidgets.QHBoxLayout()
        x_label_layout2=QtWidgets.QVBoxLayout()
        x_conversion_layout2=QtWidgets.QVBoxLayout()
        
        x_axis_layout2.addWidget(self.x_axis_label2)
        x_axis_layout2.addWidget(self.x_axis_box2) 
        x_tick_layout2.addWidget(self.x_label_label2)
        x_tick_layout2.addWidget(self.x_label_check2)
        x_label_layout2.addLayout(x_tick_layout2)
        x_label_layout2.addWidget(self.x_label_box2) 
        x_conversion_layout2.addWidget(self.x_conversion_label2)
        x_conversion_layout2.addWidget(self.x_conversion_box2) 
        x_axis_total_layout2.addLayout(x_axis_layout2)
        x_axis_total_layout2.addLayout(x_label_layout2)
        x_axis_total_layout2.addLayout(x_conversion_layout2)
        self.x_axis_frame2.setLayout(x_axis_total_layout2)
        #self.xlabelsbox.addItems(axisoptions)

        
        self.y_axis_label2 = QtWidgets.QLabel('y axis')
        self.y_axis_box2 = QtWidgets.QComboBox()
        self.y_axis_box2.addItem('')
        self.y_label_label2=QtWidgets.QLabel('y label')
        self.y_label_box2=QtWidgets.QComboBox()
        self.y_label_box2.addItems(labels)
        self.y_conversion_label2=QtWidgets.QLabel('Conversion')
        self.y_conversion_box2=QtWidgets.QLineEdit()
        self.y_conversion_box2.setFixedWidth(50)
        
        '''Make a box to store the label and combobox in one line'''
        self.y_axis_frame2= QtWidgets.QGroupBox()
        y_axis_total_layout2 = QtWidgets.QHBoxLayout()
        y_axis_layout2=QtWidgets.QVBoxLayout()
        y_label_layout2=QtWidgets.QVBoxLayout()
        y_conversion_layout2=QtWidgets.QVBoxLayout()
        y_axis_layout2.addWidget(self.y_axis_label2)
        y_axis_layout2.addWidget(self.y_axis_box2) 
        y_label_layout2.addWidget(self.y_label_label2)
        y_label_layout2.addWidget(self.y_label_box2) 
        y_conversion_layout2.addWidget(self.y_conversion_label2)
        y_conversion_layout2.addWidget(self.y_conversion_box2) 
        y_axis_total_layout2.addLayout(y_axis_layout2)
        y_axis_total_layout2.addLayout(y_label_layout2)
        y_axis_total_layout2.addLayout(y_conversion_layout2)
        self.y_axis_frame2.setLayout(y_axis_total_layout2)

        self.z_axis_label2 = QtWidgets.QLabel('z axis')
        self.z_axis_box2 = QtWidgets.QComboBox()
        self.z_axis_box2.addItem('')
        self.z_label_label2=QtWidgets.QLabel('z label')
        self.z_label_box2=QtWidgets.QComboBox()
        self.z_label_box2.addItems(labels)
        self.z_conversion_label2=QtWidgets.QLabel('Conversion')
        self.z_conversion_box2=QtWidgets.QLineEdit()
        self.z_conversion_box2.setFixedWidth(50)
        
        '''Make a box to store the label and combobox in one line'''
        self.z_axis_frame2= QtWidgets.QGroupBox()
        z_axis_total_layout2 = QtWidgets.QHBoxLayout()
        z_axis_layout2=QtWidgets.QVBoxLayout()
        z_label_layout2=QtWidgets.QVBoxLayout()
        z_conversion_layout2=QtWidgets.QVBoxLayout()
        z_axis_layout2.addWidget(self.z_axis_label2)
        z_axis_layout2.addWidget(self.z_axis_box2) 
        z_label_layout2.addWidget(self.z_label_label2)
        z_label_layout2.addWidget(self.z_label_box2) 
        z_conversion_layout2.addWidget(self.z_conversion_label2)
        z_conversion_layout2.addWidget(self.z_conversion_box2) 
        z_axis_total_layout2.addLayout(z_axis_layout2)
        z_axis_total_layout2.addLayout(z_label_layout2)
        z_axis_total_layout2.addLayout(z_conversion_layout2)
        self.z_axis_frame2.setLayout(z_axis_total_layout2)
        
        self.titlelabel2= QtWidgets.QLabel('Title')
        self.titlebox2 = QtWidgets.QLineEdit()
        self.title_frame2= QtWidgets.QGroupBox()
        title_layout2 = QtWidgets.QHBoxLayout()
        title_layout2.addWidget(self.titlelabel2)
        title_layout2.addWidget(self.titlebox2) 
        self.title_frame2.setLayout(title_layout2)
        
        self.cmap_label2= QtWidgets.QLabel('Colormap')
        self.cmapbox2 = QtWidgets.QLineEdit()
        self.cmapbox2.setFixedWidth(80)

        
        self.extent_label2 = QtWidgets.QLabel('Extent')
        self.extentbox2=QtWidgets.QCheckBox()
        self.separator_ext2=QtWidgets.QFrame()
        self.extent_frame2= QtWidgets.QGroupBox()
        extent_layout2 = QtWidgets.QHBoxLayout()
        extent_layout2.addWidget(self.extent_label2)
        extent_layout2.addWidget(self.extentbox2)
        extent_layout2.addWidget(self.separator_ext2)
        extent_layout2.addWidget(self.cmap_label2)
        extent_layout2.addWidget(self.cmapbox2)
        self.extent_frame2.setLayout(extent_layout2)
        
        '''Postprocessing for conductivity and spacing offset between plots'''
        self.conduct_label2 = QtWidgets.QLabel('Conductance')
        self.conduct_box2=QtWidgets.QCheckBox()
        self.eh_label2=QtWidgets.QLabel('Conductance quantum')
        self.eh_box2=QtWidgets.QCheckBox()
        self.separator_postproc2=QtWidgets.QFrame()
        self.postproc_frame2= QtWidgets.QGroupBox()
        self.offset_hor_label=QtWidgets.QLabel('Offset x')
        self.offset_hor_box=QtWidgets.QLineEdit()
        self.offset_hor_box.setText(self.offset_hor)
        self.offset_hor_box.setFixedWidth(80)
        self.offset_ver_label=QtWidgets.QLabel('Offset y')
        self.offset_ver_box=QtWidgets.QLineEdit()
        self.offset_ver_box.setFixedWidth(80)
        self.offset_ver_box.setText(self.offset_ver)
        
        self.postproc_frame=QtWidgets.QGroupBox()
        postproc2_layout = QtWidgets.QHBoxLayout()
        conduct2_layout=QtWidgets.QVBoxLayout()
        conduct2_layout1=QtWidgets.QHBoxLayout()
        conduct2_layout2=QtWidgets.QHBoxLayout()
        offset_layout=QtWidgets.QVBoxLayout()
        offset_layout1=QtWidgets.QHBoxLayout()
        offset_layout2=QtWidgets.QHBoxLayout()
        
        conduct2_layout1.addWidget(self.conduct_label2)
        conduct2_layout1.addWidget(self.conduct_box2)
        conduct2_layout2.addWidget(self.eh_label2)
        conduct2_layout2.addWidget(self.eh_box2)
        offset_layout1.addWidget(self.offset_hor_label)
        offset_layout1.addWidget(self.offset_hor_box)
        offset_layout2.addWidget(self.offset_ver_label)
        offset_layout2.addWidget(self.offset_ver_box)
        
        conduct2_layout.addLayout(conduct2_layout1)
        conduct2_layout.addLayout(conduct2_layout2)
        offset_layout.addLayout(offset_layout1)
        offset_layout.addLayout(offset_layout2)
        postproc2_layout.addLayout(conduct2_layout)
        postproc2_layout.addWidget(self.separator_postproc2)
        postproc2_layout.addLayout(offset_layout)
        self.postproc_frame2.setLayout(postproc2_layout)
        
        
        '''Make a slider for the lines to be selected from the 2d plot'''
        self.hlinelabel = QtWidgets.QLabel('Horizontal line')
        self.horslider= QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.horslider.setMaximum(500)
        self.horslider.setMinimum(0)
        self.horslider.setTickInterval(1)
        self.horslider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horslider.valueChanged.connect(self.horslider_value_change)
        self.horslider_value=0
        self.horlabelbox=QtWidgets.QComboBox()
        self.horlabelbox.addItem('')
        
        self.vlinelabel = QtWidgets.QLabel('Vertical line')
        self.verslider= QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.verslider.setMaximum(500)
        self.verslider.setMinimum(0)
        self.verslider.setTickInterval(1)
        self.verslider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.verslider.valueChanged.connect(self.verslider_value_change)
        self.verslider_value=0
        self.verlabelbox=QtWidgets.QComboBox()
        self.verlabelbox.addItem('')

        self.x_axis_box2.activated.connect(self.onChanged_x2)
        self.y_axis_box2.activated.connect(self.onChanged_y2)
        self.z_axis_box2.activated.connect(self.onChanged_z2)
        self.horlabelbox.activated.connect(self.onChanged_horlabel)
        self.verlabelbox.activated.connect(self.onChanged_verlabel)
        self.extentbox2.clicked.connect(self.onChanged_extent2)
        self.popupbox2.clicked.connect(self.onChanged_popup2)
        self.x_label_check2.clicked.connect(self.onChanged_labels2)
        self.conduct_box2.clicked.connect(self.onChanged_conduct2)
        self.eh_box2.clicked.connect(self.onChanged_eh2)
        
        self.fitcontrolframe2 = QtWidgets.QGroupBox()
        fitcontrollayout2 = QtWidgets.QVBoxLayout()
        for widget2 in (self.databutton2,
                        #self.loadpopup_button,
                        self.popup_frame2,
                        self.x_axis_frame2,
                        self.y_axis_frame2,
                        self.z_axis_frame2,
                        self.title_frame2,
                        self.extent_frame2,
                        self.postproc_frame2,
                        self.vlinelabel,self.verlabelbox,self.verslider,
                       self.hlinelabel,self.horlabelbox,self.horslider,
                       self.updatebutton2):
            fitcontrollayout2.addWidget(widget2)
        self.fitcontrolframe2.setLayout(fitcontrollayout2)
        
        
        splitter2 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter2.addWidget(self.otherplot)
        splitter2.addWidget(self.fitcontrolframe2)
        
        '''Do the final layout including the tabs'''
        
        self.layout = QtWidgets.QVBoxLayout(self)
        
        '''Initialize the tab screen'''
        self.tabs = QtWidgets.QTabWidget()
        
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        #self.tab3 = QtWidgets.QWidget()
        
        self.tabs.resize(1000,800)
        
        '''Add the tabs'''
        self.tabs.addTab(self.tab1,"Tab 1")
        self.tabs.addTab(self.tab2,"Tab 2")
        #self.tabs.addTab(self.tab3,"Tab 3")
        
        '''Fill the tabs with the proper layouts'''

        self.tab1.layout = QtWidgets.QVBoxLayout(self)
        self.tab1.layout.addWidget(splitter)
        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout = QtWidgets.QHBoxLayout(self)
        self.tab2.layout.addWidget(splitter2)
        self.tab2.setLayout(self.tab2.layout)
        
        '''Third tab if needed'''


        '''Finalize the tab adding them to the widget. This is called by 
        the main funcion above'''
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
    
    '''Define all the functions the will answer to the different widgets
        This create the response of the actions that can be done in the window'''

    '''Open the file to load the data'''
    def openFileName(self):

        self.fixed=self.get_fix_label()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        if self.fixed==False:
            self.tot_data=[]
            self.tot_fileName=[]
            
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"Choose your file", self.data_direct,"All Files (*);;Python Files (*.py)", options=options)

        self.dataset=[]
        
        #self.raw_data=[]
        if self.fileName:
            for i in range(len(self.fileName)):
                self.dataset=self.fileName[i]
                try:
                    self.data, self.raw_data, self.variables = general_plotting_v2.parse_data(self.dataset)
                
                
                    '''Load the initial parameters for plotting'''
                    self.x_axis_box.clear()
                    self.y_axis_box.clear()
                    self.z_axis_box.clear()
                    self.x_axis_box.addItems(self.variables)
                    self.y_axis_box.addItems(self.variables)
                    self.normalize_y_box.addItems(self.variables)
                    self.z_axis_box.addItems(self.variables)
                    self.normalize_z_box.addItems(self.variables)
                    self.titlebox.setText(self.title)
                    self.cmapbox.setText(self.cmap)
                    self.x_conversion_box.setText(self.conversion_x)
                    self.y_conversion_box.setText(self.conversion_y)
                    self.z_conversion_box.setText(self.conversion_z)
                    
                    self.offset=self.get_offset()
                    '''Make sure the new plot has the attributes needed to plot
                    If it does not, the attribute just sets for a new value
                    of the variables in the new dataset'''
                    if self.x_axis in self.variables:
                        self.x_axis_box.setCurrentText(self.x_axis)
                    else: 
                        self.x_axis=self.get_x_axis()
                    if self.y_axis in self.variables:
                        self.y_axis_box.setCurrentText(self.y_axis)
                    else: 
                        self.y_axis=self.get_y_axis()
                    if self.z_axis in self.variables:
                        self.z_axis_box.setCurrentText(self.z_axis)
                    else: 
                        self.z_axis=self.get_z_axis()
                        
                    if self.normalize_y in self.variables:
                        self.normalize_y_box.setCurrentText(self.normalize_y)
                    else: 
                        self.normalize_y=self.get_normalize_y()
                        
                    if self.normalize_z in self.variables:
                        self.normalize_z_box.setCurrentText(self.normalize_z)
                    else: 
                        self.normalize_z=self.get_normalize_z()
                        
                    if len(self.fileName)==1 and self.fixed==False:
                        self.clear_ax_bool=True
                        
                    elif self.fixed==True:
                        
                        self.clear_ax_bool=False
                    else:
                        self.clear_ax_bool=False
                                    
                    '''Check if the data is 1D or 2D. Right now it just checks if the 
                        first variable is repeated several times and then it assumes it is 
                         a megasweep. This can probably be done in a better way'''
    
    
                    if getattr(self.data,self.variables[0])[0]!=getattr(self.data,self.variables[0])[5]:
                        self.z_axis_box.setEnabled(False)
                        self.dimension=1
                    else:
                        self.data,self.variables=general_plotting_v2.map_transform(self.dataset)
                        self.dimension=2
                        
                    '''Call the plotting Class'''

                    self.plotwidget.canvas.plot(self.dataset,self.data,self.raw_data,
                                                self.variables,self.dimension,
                                                self.x_axis,self.y_axis,self.z_axis,
                                                self.x_axis,self.y_axis,self.z_axis,
                                                self.normalize_y,self.normalize_z,
                                                self.conversion_x,self.conversion_y, self.conversion_z,
                                                title= self.title,
                                                cmap=self.cmap,extent_bool=self.extent_bool,
                                                normalize_y_bool=self.normalize_y_bool,normalize_z_bool=self.normalize_z_bool,
                                                clear_axis=self.clear_ax_bool,offset=self.offset)  

                    '''Stores the data for future operations'''
                    self.tot_data.append(self.data)
                    self.tot_fileName.append(self.fileName[i])
                
                except ValueError as e:
                    self.pop_error_wrongfile.pop_error()
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print(str(e)+' line '+str(exc_tb.tb_lineno))

        return self.dataset

    '''
    def dragEnterEvent(self, e):

        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()
            
    def dropEvent(self, e):

        self.fileName=e
        for i in range(len(self.fileName)):
            self.dataset=self.fileName[i]
            try:
                self.data, self.raw_data, self.variables = general_plotting_vICFO.parse_data(self.dataset)
                
                
                #Load the initial parameters for plotting
                self.x_axis_box.clear()
                self.y_axis_box.clear()
                self.z_axis_box.clear()
                self.x_axis_box.addItems(self.variables)
                self.y_axis_box.addItems(self.variables)
                self.z_axis_box.addItems(self.variables)
                self.titlebox.setText(self.title)
                self.cmapbox.setText(self.cmap)
                self.x_conversion_box.setText(self.conversion_x)
                self.y_conversion_box.setText(self.conversion_y)
                self.z_conversion_box.setText(self.conversion_z)
                    
                self.offset=self.get_offset()
                #Make sure the new plot has the attributes needed to plot
                #If it does not, the attribute just sets for a new value
                # of the variables in the new dataset
                if self.x_axis in self.variables:
                    self.x_axis_box.setCurrentText(self.x_axis)
                else: 
                    self.x_axis=self.get_x_axis()
                if self.y_axis in self.variables:
                    self.y_axis_box.setCurrentText(self.y_axis)
                else: 
                    self.y_axis=self.get_y_axis()
                if self.z_axis in self.variables:
                    self.z_axis_box.setCurrentText(self.z_axis)
                else: 
                    self.z_axis=self.get_z_axis()
        
                if len(self.fileName)==1 and self.fixed==False:
                    self.clear_ax_bool=True
                        
                elif self.fixed==True:
                        
                    self.clear_ax_bool=False
                else:
                    self.clear_ax_bool=False
                                    
               #Check if the data is 1D or 2D. Right now it just checks if the 
                # first variable is repeated several times and then it assumes it is 
               #  a megasweep. This can probably be done in a better way
    
    
                if getattr(self.data,self.variables[0])[0]!=getattr(self.data,self.variables[0])[5]:
                    self.z_axis_box.setEnabled(False)
                    self.dimension=1
                else:
                    self.data,self.variables=general_plotting_vICFO.map_transform(self.dataset)
                    self.dimension=2
                        
                #Call the plotting Class
                self.plotwidget.canvas.plot(self.dataset,self.data,self.raw_data,
                                            self.variables,self.dimension,
                                            self.x_axis,self.y_axis,self.z_axis,
                                            self.x_axis,self.y_axis,self.z_axis,
                                            self.normalize_y,self.normalize_z,
                                            self.conversion_x,self.conversion_y,
                                            self.conversion_z,
                                            self.title,
                                            self.cmap,self.extent_bool,
                                            self.normalize_y_bool,self.normalize_z_bool,
                                            clear_axis=self.clear_ax_bool,offset=self.offset)  
                #Stores the data for future operations
                self.tot_data.append(self.data)
                self.tot_fileName.append(self.fileName[i])
                
            except ValueError as e:
                self.pop_error_wrongfile.pop_error()
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(str(e)+' line '+str(exc_tb.tb_lineno))

        return self.dataset
        '''
        
    ###Triggers for the different widgets
    
    def onChanged_x(self):
        self.x_axis = self.x_axis_box.currentText()
        self.update_plot()
    
    def onChanged_y(self):
        self.y_axis = self.y_axis_box.currentText()
        self.update_plot()
    
    def onChanged_z(self):
        self.z_axis = self.z_axis_box.currentText()
        self.update_plot()
        
    def onChanged_normalize_y(self):
        self.normalize_y = self.normalize_y_box.currentText()
        self.update_plot()
    
    def onChanged_normalize_z(self):
        self.normalize_z = self.normalize_z_box.currentText()
        self.update_plot()
        
    def onChanged_normalize_y_bool(self):
        self.normalize_y_bool=self.get_normalize_y_bool_label()
        self.update_plot() 
        
    def onChanged_normalize_z_bool(self):
        self.normalize_z_bool=self.get_normalize_z_bool_label()
        self.update_plot() 
        
    def onChanged_lx(self):
        self.x_label = self.x_label_box.currentText()
        self.update_plot()
        
    def onChanged_ly(self):
        self.y_label = self.y_label_box.currentText()
        self.update_plot()
    
    def onChanged_lz(self):
        self.z_label = self.z_label_box.currentText()
        self.update_plot()
             
    def onChanged_extent(self):
        self.extent_bool=self.get_extent_label()
        self.update_plot()
        
    def onChanged_labels(self):
        self.labels_bool=self.get_axis_labels()
        self.update_plot()
    
    def onChanged_conduct(self):
        self.conduct_bool=self.get_conduct_label()
        #self.x_label_check.setCheckState(True)
        self.labels_bool=True
        self.extent_bool=True   
        self.update_plot()
        
    def onChanged_eh(self):
        self.eh_bool=self.get_eh_label()
        self.labels_bool=True
        self.extent=True
        self.update_plot()  
    
    def onChanged_legend(self):
        self.legend_bool=self.get_legend()
        self.update_plot()
        
    def onChanged_makemap(self):
        self.makemap_bool=self.get_makemap()
        self.update_plot()
        
        
    ###'''Return the value of the different labels'''
    
    def get_x_axis(self):
        self.xlabel=self.x_axis_box.currentText()        
        return self.xlabel
    
    def get_y_axis(self):
        return self.y_axis_box.currentText()
    
    def get_z_axis(self):
        return self.z_axis_box.currentText()
    
    def get_normalize_y(self):
        return self.normalize_y_box.currentText()
    
    def get_normalize_z(self):
        return self.normalize_z_box.currentText()
    
    def get_extent_label(self):
        if self.extentbox.isChecked():
            return True
        else:
            return False
    def get_axis_labels(self):
        if self.x_label_check.isChecked():
            return True
        else:
            return False
    
    def get_legend(self):
        if self.legendbox.isChecked():
            return True
        else:
            return False
    def get_pin_label(self):
        if self.popupbox.isChecked():
            return True
        else:
            return False
        
    def get_fix_label(self):
        if self.newdata_box.isChecked():
            return True
        else:
            return False
        
    def get_conduct_label(self):
        if self.conduct_box.isChecked():
            if self.dimension==1:
                self.y_label_box.setCurrentIndex(conduct_index)
            else:
                self.z_label_box.setCurrentIndex(conduct_index)
            
            return True
        else:
            self.y_label_box.setCurrentIndex(0)
            self.z_label_box.setCurrentIndex(0)
            return False

    def get_eh_label(self):
        if self.eh_box.isChecked():
            if self.dimension==1:
                self.y_label_box.setCurrentIndex(eh_index)
            else:
                self.z_label_box.setCurrentIndex(eh_index)
            return True
        else:
            self.y_label_box.setCurrentIndex(0)
            self.z_label_box.setCurrentIndex(0)
            return False
        
    def get_normalize_y_bool_label(self):
        if self.normalize_y_tick.isChecked():
            return True
        else:
            return False
        
    def get_normalize_z_bool_label(self):
        if self.normalize_z_tick.isChecked():
            return True
        else:
            return False
        
    def get_makemap(self):
        if self.makemap_box.isChecked():
            self.z_axis_box.setEnabled(True)
            return True
        else:
            self.z_axis_box.setEnabled(False)
            self.y_axis_box.setCurrentText(self.z_axis)
            self.y_axis=self.z_axis
            return False
        
    ### '''Conversion factors'''
    def get_conversion_x(self):
        self.conversion_x=self.x_conversion_box.text()
        return self.x_conversion_box.text()
    
    def get_conversion_y(self):
        self.conversion_y=self.y_conversion_box.text()
        return self.y_conversion_box.text()
    
    def get_conversion_z(self):
        self.conversion_z=self.z_conversion_box.text()
        return self.z_conversion_box.text()

    '''Return the title written'''
    def title_give(self):
        self.title=self.titlebox.text()
        return self.titlebox.text()
    
    '''Colormap for the plot of the maps'''
    def colourcode(self):
        self.cmap=self.cmapbox.text()
        return self.cmap
    def get_offset(self):
        self.offset=float(self.offset_box.text())
        return self.offset
    
    '''The min and max values'''
    def get_x_min(self):
        self.x_min=float(self.min_x_box.text())
        return self.x_min
    
    def get_x_max(self):
        self.x_max=float(self.max_x_box.text())
        return self.x_max
    
    def get_y_min(self):
        self.y_min=float(self.min_y_box.text())
        return self.y_min
    
    def get_y_max(self):
        self.y_max=float(self.max_y_box.text())
        return self.y_max
    
    def get_z_min(self):
        self.z_min=float(self.min_z_box.text())
        return self.z_min
    
    def get_z_max(self):
        self.z_max=float(self.max_z_box.text())
        return self.z_max
    
    '''Update the plot when hitting the update bottom or similar'''
    
    def update_plot(self):
        
        
        self.title=self.title_give()
        self.cmap=self.colourcode()
        self.offset=self.get_offset()
        self.conversion_x=self.get_conversion_x()
        self.conversion_y=self.get_conversion_y()
        self.conversion_z=self.get_conversion_z()
        self.normalize_y_bool=self.get_normalize_y_bool_label()
        if self.labels_bool:
            self.x_label=labels_dict[self.x_label_box.currentText()]
            self.y_label=labels_dict[self.y_label_box.currentText()]
            self.z_label=labels_dict[self.z_label_box.currentText()]
        else:
            self.x_label=self.x_axis
            self.y_label=self.y_axis
            self.z_label=self.z_axis
        
        self.x_min=self.get_x_min()
        self.x_max=self.get_x_max()
        self.y_min=self.get_y_min()
        self.y_max=self.get_y_max()
        self.z_min=self.get_z_min()
        self.z_max=self.get_z_max()

        try:
            if self.clear_ax_bool==True and self.makemap_bool==False:
                self.plotwidget.canvas.plot(self.dataset,
                                            self.data,self.raw_data,self.variables,
                                            self.dimension,
                                            self.x_axis,self.y_axis,self.z_axis,
                                            self.x_label,self.y_label,self.z_label,
                                            self.normalize_y,self.normalize_z,
                                            self.conversion_x,self.conversion_y,self.conversion_z,
                                            self.title,
                                            self.cmap,self.extent_bool,
                                            self.normalize_y_bool,self.normalize_z_bool,
                                            self.clear_ax_bool,
                                            self.conduct_bool,self.eh_bool,
                                            self.offset,self.legend_bool,
                                            self.x_min,self.x_max,self.y_min,self.y_max,self.z_min,self.z_max)
                
            elif self.clear_ax_bool==False and self.makemap_bool==False:
                self.plotwidget.canvas.clear()
                for i in range(len(self.tot_data)):
                    
                    self.plotwidget.canvas.plot(self.tot_fileName[i],self.tot_data[i],self.raw_data,
                                            self.variables,self.dimension,
                                            self.x_axis,self.y_axis,self.z_axis,
                                            self.x_label,self.y_label,self.z_label,
                                            self.normalize_y,self.normalize_z,
                                            self.conversion_x,self.conversion_y,self.conversion_z,
                                            self.title,
                                            self.cmap,self.extent_bool,
                                            self.normalize_y_bool,self.normalize_z_bool,
                                            self.clear_ax_bool,
                                            self.conduct_bool,self.eh_bool,
                                            self.offset, self.legend_bool,
                                            self.x_min,self.x_max,self.y_min,self.y_max,self.z_min,self.z_max)
            elif self.makemap_bool:
                self.plotwidget.canvas.clear()
                self.full_data_map=Object()

                for i in range(len(self.variables)):
                    full_data=[]
                    for j in range(len(self.tot_fileName)):
                        full_data.append(getattr(self.tot_data[j],self.variables[i]))
                    setattr(self.full_data_map,self.variables[i],full_data)
                self.plotwidget.canvas.plot(self.tot_fileName[0],self.full_data_map,self.raw_data,
                                            self.variables,2,
                                            self.x_axis,self.y_axis,self.z_axis,
                                            self.x_label,self.y_label,self.z_label,
                                            self.normalize_y,self.normalize_z,
                                            self.conversion_x,self.conversion_y,self.conversion_z,
                                            self.title,
                                            self.cmap,self.extent_bool,
                                            self.normalize_y_bool,self.normalize_z_bool,
                                            self.clear_ax_bool,
                                            self.conduct_bool,
                                            self.eh_bool,self.offset,
                                            self.legend_bool,
                                            self.x_min,self.x_max,self.y_min,self.y_max,self.z_min,self.z_max)
                    
        except AttributeError as e:
            self.pop_error_nofile.pop_error()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(str(e)+' line '+str(exc_tb.tb_lineno))

    def import_template(self):
        '''This works'''
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName_temp, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Load a Template", self.template_direct,"All Files (*);;Python Files (*.py)",options=options)
        if fileName_temp:
            template_loaded={}
            with open(fileName_temp) as fh:
                for line in fh:
                    command= line.strip().split("\t")
                    try:
                        template_loaded[command[0]] = command[1]
                    except IndexError:
                        template_loaded[command[0]] = ''
            try:
                self.x_axis=template_loaded['x_axis']
                self.y_axis=template_loaded['y_axis']
                self.z_axis=template_loaded['z_axis']
                self.title=template_loaded['title']
                self.cmap=template_loaded['cmap']
                if template_loaded['extent']=='True':
                    self.extent_bool=True
                else:
                    self.extent_bool=False
                
                self.x_axis2=template_loaded['x_axis2']
                self.y_axis2=template_loaded['y_axis2']
                self.z_axis2=template_loaded['z_axis2']
                self.cmap2=template_loaded['cmap2']
                self.title2=template_loaded['title2']
                if template_loaded['extent2']=='True':
                    self.extent_bool2=True
                else:
                    self.extent_bool2=False
                self.x_line=int(template_loaded['verline'])
                self.y_line=int(template_loaded['horline'])
                self.conversion_x=template_loaded['x_conversion']
                self.conversion_y=template_loaded['y_conversion']
                self.conversion_z=template_loaded['z_conversion']
                self.conversion_x2=template_loaded['x_conversion2']
                self.conversion_y2=template_loaded['y_conversion2']
                self.conversion_z2=template_loaded['z_conversion2']
                self.x_label=template_loaded['x_label']
                self.y_label=template_loaded['y_label']
                self.z_label=template_loaded['z_label']
                self.x_label2=template_loaded['x_label2']
        
                '''Set the boxes with the right names'''
                self.titlebox.setText(self.title)
                self.cmapbox.setText(self.cmap)
                self.offset_box.setText(str(self.offset))
                self.x_conversion_box.setText(self.conversion_x)
                self.y_conversion_box.setText(self.conversion_y)
                self.z_conversion_box.setText(self.conversion_z)
                self.x_axis_box.setCurrentText(self.x_axis)
                self.y_axis_box.setCurrentText(self.y_axis)
                self.z_axis_box.setCurrentText(self.z_axis)
                self.x_label_box.setCurrentText(self.x_label)
                self.y_label_box.setCurrentText(self.y_label)
                self.z_label_box.setCurrentText(self.z_label)
            except KeyError as e:
                self.pop_error_wrongtemplate.pop_error()
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(str(e)+' line '+str(exc_tb.tb_lineno))
            try:
                self.plotwidget.canvas.plot(self.dataset,
                            self.data,self.raw_data,self.variables,
                            self.dimension,
                            self.x_axis,self.y_axis,self.z_axis,
                            self.x_label,self.y_label,self.z_label,
                            self.conversion_x,self.conversion_y,self.conversion_z,
                            title=self.title,
                            cmap=self.cmap,extent_bool=self.extent_bool,
                            conduct_bool=self.conduct_bool,
                            eh_bool=self.eh_bool,offset=self.offset)
            except AttributeError as e:
                self.pop_error_nofile.pop_error()
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(str(e)+' line '+str(exc_tb.tb_lineno))
    def custom_load(self):
        '''Import a dataset and then the template'''
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName_custom, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Choose your file", self.custom_direct,"All Files (*);;Python Files (*.py)", options=options)
        if fileName_custom:
            template_custom={}
            with open(fileName_custom) as fh:
                for line in fh:
                    command= line.strip().split("\t")
                    try:
                        template_custom[command[0]] = command[1]
                    except IndexError:
                        template_custom[command[0]] = ''
            try:
                self.dataset_num=template_custom['dataset number']
                
                self.tot_fileName=[]
                self.tot_data=[]
                for i in range(int(self.dataset_num)):
                    self.tot_fileName.append(template_custom['dataset'+str(i)])
    
                    
                self.x_axis=template_custom['x_axis']
                self.y_axis=template_custom['y_axis']
                self.z_axis=template_custom['z_axis']
                self.title=template_custom['title']
                self.cmap=template_custom['cmap']
                
                self.conversion_x=float(template_custom['x_conversion'])
                self.conversion_y=float(template_custom['y_conversion'])
                self.conversion_z=float(template_custom['z_conversion'])
                            
                if template_custom['extent']=='True':
                    self.extent_bool=True
                else:
                    self.extent_bool=False
                if template_custom['conductance']=='True':
                    self.conduct_bool=True
                else:
                    self.conduct_bool=False
                if template_custom['eh']=='True':
                    self.eh_bool=True
                else:
                    self.eh_bool=False
                if template_custom['clear axis bool']=='True':
                    self.clear_ax_bool=True
                else:
                    self.clear_ax_bool=False
                if template_custom['offset']!='':
                    self.offset=float(template_custom['offset'])
                if template_custom['legend bool']=='True':
                    self.legend_bool=True
                else:
                    self.legend_bool=False   
                if template_custom['makemap bool']=='True':
                    self.makemap_bool=True
                else:
                    self.makemap_bool=False
                if template_custom['labels bool']=='True':
                    self.labels_bool=True
                else:
                    self.labels_bool=False    
                
                if self.labels_bool:
                    self.x_label=template_custom['x_label']
                    self.y_label=template_custom['y_label']
                    self.z_label=template_custom['z_label']    
                else:
                    self.x_label=self.x_axis
                    self.y_label=self.y_axis
                    self.z_label=self.z_axis  
                
                self.x_axis2=template_custom['x_axis2']
                self.y_axis2=template_custom['y_axis2']
                self.z_axis2=template_custom['z_axis2']
                self.cmap2=template_custom['cmap2']
                self.title2=template_custom['title2']
                if template_custom['extent2']=='True':
                    self.extent_bool2=True
                else:
                    self.extent_bool2=False
                if template_custom['conductance2']=='True':
                    self.conduct_bool2=True
                else:
                    self.conduct_bool2=False
                if template_custom['eh2']=='True':
                    self.eh_bool2=True
                else:
                    self.eh_bool2=False
                
                    
                self.x_line=int(template_custom['verline'])
                self.y_line=int(template_custom['horline'])
                
                self.conversion_x2=float(template_custom['x_conversion2'])
                self.conversion_y2=float(template_custom['y_conversion2'])
                self.conversion_z2=float(template_custom['z_conversion2'])
                
                self.x_label2=template_custom['x_label2']
                self.ylabel2=template_custom['y_label2']
                self.zlabel2=template_custom['z_label2']
                self.dimension=int(template_custom['dimension'])
    
                
                if template_custom['offset_hor']!='':
                    self.offset_hor=float(template_custom['offset_hor'])
                if template_custom['offset_ver']!='':
                    self.offset_ver=float(template_custom['offset_ver'])
                    
                    
                '''Get the data from the dataset'''
                for i in range(len(self.tot_fileName)):
                    self.dataset=self.tot_fileName[i]
                    self.data, self.raw_data, self.variables = general_plotting_v2.parse_data(self.dataset)
                    if self.dimension==2:
                        self.data,self.variables=general_plotting_v2.map_transform(self.dataset)  
                    self.tot_data.append(self.data)
    
    
                '''Load the initial parameters for plotting'''
                self.x_axis_box.clear()
                self.y_axis_box.clear()
                self.z_axis_box.clear()
                self.x_axis_box.addItems(self.variables)
                self.y_axis_box.addItems(self.variables)
                self.z_axis_box.addItems(self.variables)
                '''Set the boxes with the right names'''
                self.titlebox.setText(self.title)
                self.cmapbox.setText(self.cmap)
                self.offset_box.setText(str(self.offset))
                self.x_conversion_box.setText(str(self.conversion_x))
                self.y_conversion_box.setText(str(self.conversion_y))
                self.z_conversion_box.setText(str(self.conversion_z))
                self.x_axis_box.setCurrentText(self.x_axis)
                self.y_axis_box.setCurrentText(self.y_axis)
                self.z_axis_box.setCurrentText(self.z_axis)
                self.x_label_box.setCurrentText(self.x_label)
                self.y_label_box.setCurrentText(self.y_label)
                self.z_label_box.setCurrentText(self.z_label)
               
                
                self.plotwidget.canvas.clear()
    
                if self.makemap_bool==False:
    
                    for i in range(len(self.tot_data)):
                        
                        self.plotwidget.canvas.plot(self.tot_fileName[i],self.tot_data[i],self.raw_data,
                                                self.variables,self.dimension,
                                                self.x_axis,self.y_axis,self.z_axis,
                                                self.x_label,self.y_label,self.z_label,
                                                self.conversion_x,self.conversion_y,self.conversion_z,
                                                title=self.title,
                                                cmap=self.cmap,extent_bool=self.extent_bool,
                                                clear_axis=self.clear_ax_bool,
                                                conduct_bool=self.conduct_bool,
                                                eh_bool=self.eh_bool,offset=self.offset,
                                                legend_bool=self.legend_bool)
                elif self.makemap_bool:
    
                    self.full_data_map=Object()
    
                    for i in range(len(self.variables)):
                        full_data=[]
                        for j in range(len(self.tot_fileName)):
                            full_data.append(getattr(self.tot_data[j],self.variables[i]))
                        setattr(self.full_data_map,self.variables[i],full_data)
                    self.plotwidget.canvas.plot(self.tot_fileName[0],self.full_data_map,self.raw_data,
                                                self.variables,2,
                                                self.x_axis,self.y_axis,self.z_axis,
                                                self.x_label,self.y_label,self.z_label,
                                                self.conversion_x,self.conversion_y,self.conversion_z,
                                                title=self.title,
                                                cmap=self.cmap,extent_bool=self.extent_bool,
                                                clear_axis=self.clear_ax_bool,
                                                conduct_bool=self.conduct_bool,
                                                eh_bool=self.eh_bool,offset=self.offset,
                                                legend_bool=self.legend_bool)
            except KeyError as e:

                self.pop_error_wrongtemplate.pop_error()
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(str(e)+' line '+str(exc_tb.tb_lineno))
            

        
    def custom_save(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, filters = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()",custom_direct,"PNG(*.png);;PDF (*.pdf)", options=options)
        if filters=='PNG(*.png)':
            extension='.png'
        elif filters=='PDF (*.pdf)':
            extension='.pdf'
         
        if fileName:
            self.plotwidget.canvas.fig.savefig(fileName,dpi=300)
    
            '''Here somehow open a file to store the steps taken. Still needs 
            to be thought how to exactly do it'''
            #json_string=json.dumps(custom_save_dict)
            
            f=open(fileName+'.txt','w+')
            f.write('dataset number\t'+str(len(self.tot_fileName))+'\n')
            for i in range(len(self.tot_fileName)):
                f.write('dataset'+str(i)+'\t'+self.tot_fileName[i]+'\n')
    
            f.write('data_directory\t'+self.dataset+'\n'+
                    'template_directory\t'+self.template_direct+'\n'+
                    'customized_directory\t'+self.custom_direct+'\n'+
                    'x_axis\t'+self.x_axis+'\n'+
                    'y_axis\t'+self.y_axis+'\n'+
                    'z_axis\t'+self.z_axis+'\n'+
                    'labels bool\t'+str(self.labels_bool)+'\n'+
                    'x_label\t'+self.x_label+'\n'+
                    'y_label\t'+self.y_label+'\n'+
                    'z_label\t'+self.z_label+'\n'+
                    'x_conversion\t'+str(self.conversion_x)+'\n'+
                    'y_conversion\t'+str(self.conversion_y)+'\n'+
                    'z_conversion\t'+str(self.conversion_z)+'\n'+
                    'cmap\t'+self.cmap+'\n'+
                    'title\t'+self.title+'\n'+
                    'legend bool\t'+str(self.legend_bool)+'\n'+
                    'extent\t'+str(self.extent_bool)+'\n'+
                    'makemap bool\t'+str(self.makemap_bool)+'\n'+
                    'conductance\t'+str(self.conduct_bool)+'\n'+
                    'eh\t'+str(self.eh_bool)+'\n'+
                    'offset\t'+str(self.offset)+'\n'+
                    'dimension\t'+str(self.dimension)+'\n'
                    'clear axis bool\t'+str(self.clear_ax_bool)+'\n'
                    'x_axis2\t'+self.x_axis2+'\n'+
                    'y_axis2\t'+self.y_axis2+'\n'+
                    'z_axis2\t'+self.z_axis2+'\n'+
                    'labels2\t'+str(self.labels_bool2)+'\n'+
                    'x_label2\t'+self.x_label2+'\n'+
                    'y_label2\t'+self.y_label2+'\n'+
                    'z_label2\t'+self.z_label2+'\n'+
                    'x_conversion2\t'+str(self.conversion_x2)+'\n'+
                    'y_conversion2\t'+str(self.conversion_y2)+'\n'+
                    'z_conversion2\t'+str(self.conversion_z2)+'\n'+
                    'cmap2\t'+self.cmap2+'\n'+
                    'title2\t'+self.title2+'\n'+
                    'extent2\t'+str(self.extent_bool2)+'\n'+
                    'conductance2\t'+str(self.conduct_bool2)+'\n'+
                    'eh2\t'+str(self.eh_bool2)+'\n'+
                    'offset_hor\t'+str(self.offset_hor)+'\n'+
                    'offset_ver\t'+str(self.offset_ver)+'\n'+
                    'verline\t'+str(self.x_line)+'\n'+
                    'horline\t'+str(self.y_line)+'\n'
                    
                    )
    
            f.close()
        
    def popup_figure(self):
        '''Pop ups new windows with the plots. A dictionary is made
        so that each pop up is a new window. Otherwise it rewrites the 
        wimndows'''

        self.x_axis=self.get_x_axis()
        self.y_axis=self.get_y_axis()
        self.z_axis=self.get_z_axis()
        self.title=self.title_give()
        self.offset=self.get_offset()
        self.cmap=self.colourcode()
        self.extent_bool=self.get_extent_label()
        self.pinned=self.get_pin_label()
        self.legend=self.title_give()
        self.labels_bool=self.get_axis_labels()
        if self.pinned==False:
            self.pop_name='pop_figure'+str(self.counter)
            self.pop_dict[self.pop_name]=MyPopup_figure()
        if self.labels_bool:
            self.x_label=labels_dict[self.x_label_box.currentText()]
            self.y_label=labels_dict[self.y_label_box.currentText()]
            self.z_label=labels_dict[self.z_label_box.currentText()]
        else:
            self.x_label=self.x_axis
            self.y_label=self.y_axis
            self.z_label=self.z_axis
        try:
            '''try to implement the multiple graphs pop up, not so easy'''

            if self.clear_ax_bool==True and self.makemap_bool==False:
                self.pop_dict[self.pop_name].plotwidget.canvas.plot_general(self.dataset,
                                        self.data,self.raw_data,self.variables,
                                        self.dimension,
                                        self.x_axis,self.y_axis,self.z_axis,
                                        self.x_label,self.y_label,self.z_label,
                                        self.conversion_x,self.conversion_y,self.conversion_z,
                                        title=self.title,
                                        cmap=self.cmap,extent_bool=self.extent_bool,
                                        pin=self.pinned,
                                        conduct_bool=self.conduct_bool,
                                        eh_bool=self.eh_bool,offset=self.offset)
            elif self.clear_ax_bool==False and self.makemap_bool==False:
                #self.plotwidget.canvas.clear()
                for i in range(len(self.tot_fileName)):
                
                    self.pop_dict[self.pop_name].plotwidget.canvas.plot_general(self.tot_fileName[i],
                                        self.tot_data[i],self.raw_data,
                                        self.variables,self.dimension,
                                        self.x_axis,self.y_axis,self.z_axis,
                                        self.x_label,self.y_label,self.z_label,
                                        self.conversion_x,self.conversion_y,self.conversion_z,
                                        title=self.title,
                                        cmap=self.cmap,extent_bool=self.extent_bool,
                                        pin=True,
                                        conduct_bool=self.conduct_bool,
                                        eh_bool=self.eh_bool,offset=self.offset,legend_bool=self.legend_bool)
            elif self.makemap_bool:
                self.pop_dict[self.pop_name].plotwidget.canvas.plot_general(self.tot_fileName[0],
                                             self.full_data_map,self.raw_data,
                                            self.variables,2,
                                            self.x_axis,self.y_axis,self.z_axis,
                                            self.x_label,self.y_label,self.z_label,
                                            self.conversion_x,self.conversion_y,self.conversion_z,
                                            title=self.title,
                                            pin=self.pinned,
                                            cmap=self.cmap,extent_bool=self.extent_bool,
                                            conduct_bool=self.conduct_bool,
                                            eh_bool=self.eh_bool,offset=self.offset)
            
            if self.pinned==False:
                self.pop_dict[self.pop_name].show()
                self.counter=self.counter+1
        except AttributeError as e:
            self.pop_error_nofile.pop_error()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print('Cannot pop up because'+ str(e)+' line '+str(exc_tb.tb_lineno))
    def import_popup(self):
        '''Import a dataset and then the template'''
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName_custom, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Choose your file", self.custom_direct,"All Files (*);;Python Files (*.py)", options=options)
        if fileName_custom:
            template_custom={}
            with open(fileName_custom) as fh:
                for line in fh:
                    command= line.strip().split("\t")
                    try:
                        template_custom[command[0]] = command[1]
                    except IndexError:
                        template_custom[command[0]] = ''
        self.dataset=template_custom['dataset']
        self.x_axis=template_custom['x_axis']
        self.y_axis=template_custom['y_axis']
        self.z_axis=template_custom['z_axis']
        self.title=template_custom['title']

        self.cmap=template_custom['cmap']
        if template_custom['extent']=='True':
            self.extent_bool=True
        else:
            self.extent_bool=False
        if template_custom['conductance']=='True':
            self.conduct_bool=True
        else:
            self.conduct_bool=False
        if template_custom['eh']=='True':
            self.eh_bool=True
        else:
            self.eh_bool=False
        self.x_axis2=template_custom['x_axis2']
        self.y_axis2=template_custom['y_axis2']
        self.z_axis2=template_custom['z_axis2']
        self.cmap2=template_custom['cmap2']
        self.title2=template_custom['title2']
        if template_custom['extent2']=='True':
            self.extent_bool2=True
        else:
            self.extent_bool2=False
        if template_custom['conductance2']=='True':
            self.conduct_bool2=True
        else:
            self.conduct_bool2=False
        if template_custom['eh2']=='True':
            self.eh_bool2=True
        else:
            self.eh_bool2=False
            
        self.x_line=int(template_custom['verline'])
        self.y_line=int(template_custom['horline'])
        self.conversion_x=template_custom['x_conversion']
        self.conversion_y=template_custom['y_conversion']
        self.conversion_z=template_custom['z_conversion']
        self.conversion_x2=template_custom['x_conversion2']
        self.conversion_y2=template_custom['y_conversion2']
        self.conversion_z2=template_custom['z_conversion2']
        self.x_label=template_custom['x_label']
        self.y_label=template_custom['y_label']
        self.z_label=template_custom['z_label']
        self.x_label2=template_custom['x_label2']
        self.ylabel2=template_custom['y_label2']
        self.zlabel2=template_custom['z_label2']
        if template_custom['offset']!='':
            self.offset=float(template_custom['offset'])
        if template_custom['offset_hor']!='':
            self.offset_hor=float(template_custom['offset_hor'])
        if template_custom['offset_ver']!='':
            self.offset_ver=float(template_custom['offset_ver'])
        '''Get the data from the dataset'''
        
        self.data, self.raw_data, self.variables = general_plotting_v2.parse_data(self.dataset)
        
        '''Check if the data is 1D or 2D. Right now it just checks if the 
        first variable is repeated several times and then it assumes it is 
        a megasweep. This can probably be done in a better way'''
        
        if getattr(self.data,self.variables[0])[0]!=getattr(self.data,self.variables[0])[5]:
            self.z_axis_box.setEnabled(False)
            self.dimension=1
        else:
            self.data,self.variables2=general_plotting_v2.map_transform(self.dataset)
            self.dimension=2
        '''Load the initial parameters for plotting'''
        self.x_axis_box.clear()
        self.y_axis_box.clear()
        self.z_axis_box.clear()
        self.x_axis_box.addItems(self.variables)
        self.y_axis_box.addItems(self.variables)
        self.z_axis_box.addItems(self.variables)
        self.titlebox.setText(self.title)

        self.cmapbox.setText(self.cmap)
        self.x_conversion_box.setText(self.conversion_x)
        self.y_conversion_box.setText(self.conversion_y)
        self.z_conversion_box.setText(self.conversion_z)
        self.fixed=self.get_fix_label()
        self.offset_box.setText(str(self.offset))
        
        '''Make sure the new plot has the attributes needed to plot
        If it does not, the attribute just sets for a new value
        of the variables in the new dataset'''
        if self.x_axis in self.variables:
            self.x_axis_box.setCurrentText(self.x_axis)
        else: 
            self.x_axis=self.get_x_axis()
        if self.y_axis in self.variables:
            self.y_axis_box.setCurrentText(self.y_axis)
        else: 
            self.y_axis=self.get_y_axis()
        if self.z_axis in self.variables:
            self.z_axis_box.setCurrentText(self.z_axis)
        else: 
            self.z_axis=self.get_z_axis()
            
        self.x_label_box.setCurrentText(self.x_label)
        self.y_label_box.setCurrentText(self.y_label)
        self.z_label_box.setCurrentText(self.z_label)
        
        
        self.clear_ax_bool=True

        self.plotwidget.canvas.plot(self.dataset,
                        self.data,self.raw_data,self.variables,
                        self.dimension,
                        self.x_axis,self.y_axis,self.z_axis,
                        self.x_label,self.y_label,self.z_label,
                        self.conversion_x,self.conversion_y,self.conversion_z,
                        title=self.title,
                        cmap=self.cmap,extent_bool=self.extent_bool,
                        conduct_bool=self.conduct_bool,
                        eh_bool=self.eh_bool,offset=self.offset)
        
        
    def clear_graph(self):
        self.plotwidget.canvas.clear()
    
    
    
    '''Function which are only used for the second tab. Some are very similar
    to the previous functions just calling the other plot Class'''

    def openFileName2(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", self.data_direct,"All Files (*);;Python Files (*.py)", options=options)
        if fileName:
                #print(fileName)
            try:
                self.dataset2=fileName
                self.data2, self.variables2 = general_plotting_v2.map_transform(self.dataset2)
                
                self.x_axis_box2.clear()
                self.y_axis_box2.clear()
                self.z_axis_box2.clear()
                self.x_axis_box2.addItems(self.variables2)
                self.y_axis_box2.addItems(self.variables2)
                self.z_axis_box2.addItems(self.variables2)
                
                '''Make sure the new plot has the attributes needed to plot
                If it does not, the attribute just sets for a new value
                of the variables in the new dataset'''
                if self.x_axis2 in self.variables2:
                    self.x_axis_box2.setCurrentText(self.x_axis2)
                else: 
                    self.x_axis2=self.get_x_axis2()
                if self.y_axis2 in self.variables2:
                    self.y_axis_box2.setCurrentText(self.y_axis2)
                else: 
                    self.y_axis2=self.get_y_axis2()
                if self.z_axis2 in self.variables2:
                    self.z_axis_box2.setCurrentText(self.z_axis2)
                else: 
                    self.z_axis2=self.get_z_axis2()
                if self.labels_bool2==False:
                    self.x_label2=self.x_axis2
                    self.y_label2=self.y_axis2
                    self.z_label2=self.z_axis2
                self.titlebox2.setText(self.title2)
                self.cmapbox2.setText(self.cmap2)
                self.x_conversion_box2.setText(self.conversion_x2)
                self.y_conversion_box2.setText(self.conversion_y2)
                self.z_conversion_box2.setText(self.conversion_z2)
                
                        
                '''Give initial values'''
                
                self.otherplot.canvas.pseudoplot(self.x_line,self.y_line,self.dataset2,self.data2,
                                            self.variables2,
                                            self.x_axis2,self.y_axis2, self.z_axis2,
                                            self.x_axis2,self.y_axis2, self.z_axis2,
                                            self.conversion_x2,self.conversion_y2,
                                            self.conversion_z2,
                                            title=self.title2,
                                            cmap=self.cmap2,extent_bool=self.extent_bool2,
                                            conduct_bool=self.conduct_bool,
                                            eh_bool=self.eh_bool)
                
                self.verslider_max=len(getattr(self.otherplot.canvas.data,self.otherplot.canvas.x_axis)[0])-1
                self.verslider.setMaximum(self.verslider_max)
                self.verslider_values=np.arange(0,self.verslider_max,1)
                self.verslider_values_str=self.verslider_values.astype(str)
                self.verlabelbox.clear()
                self.verlabelbox.addItems(self.verslider_values_str)
                
                self.horslider_max=len(getattr(self.otherplot.canvas.data,self.otherplot.canvas.y_axis)[:,0])-1
                self.horslider.setMaximum(self.horslider_max)
                self.horslider_values=np.arange(0,self.horslider_max,1)
                self.horslider_values_str=self.horslider_values.astype(str)
                self.horlabelbox.clear()
                self.horlabelbox.addItems(self.horslider_values_str)
            except ValueError as e:
                self.pop_error_wrongfile.pop_error()
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(str(e)+' line '+str(exc_tb.tb_lineno))
        return self.dataset2
    
    
    
        
    '''Triggers for when the values of the boxes change'''
    
    def onChanged_x2(self):
        self.x_axis2 = self.get_x_axis2()
        self.update_plot2()
    
    def onChanged_y2(self):
        self.y_axis2 = self.get_y_axis2()
        self.update_plot2()
    
    def onChanged_z2(self):
        self.z_axis2 = self.get_z_axis2()
        self.update_plot2()
      
    def onChanged_verlabel(self):
        self.x_line=self.verlabelbox.currentIndex()
        self.verslider.value=self.x_line
        self.update_plot2()
        
    def onChanged_horlabel(self):
        self.y_line=self.horlabelbox.currentIndex()
        self.verslider.value=self.x_line
        self.update_plot2()
        
    def onChanged_extent2(self):
        self.extent_bool2=self.get_extent_label2()
        self.update_plot2()
        
    def onChanged_labels2(self):
        self.labels_bool2=self.get_axis_labels2()
        self.update_plot2()
    
    def onChanged_popup2(self):
        self.pinned2=self.get_pin_label2()

    def onChanged_conduct2(self):
        self.conduct_bool2=self.get_conduct_label2()
        #self.labels_bool2=True
        
        self.update_plot2()
        
    def onChanged_eh2(self):
        self.eh_bool2=self.get_eh_label2()
        self.labels_bool2=True
        self.extent2=True
        self.update_plot2() 

    '''Return the value of the slider'''
    def horslider_value_change(self,value):
        self.horslider_value=value
        self.horlabelbox.setCurrentText(str(value))
        self.y_line=value
        self.update_plot2()
        return self.horslider_value
    
    def verslider_value_change(self,value):
        self.verslider_value=value
        self.verlabelbox.setCurrentText(str(value))
        self.x_line=value
        self.update_plot2()
        return self.verslider_value
    
    '''Functions to get the values of the widgets'''
    def get_x_axis2(self):
        self.xlabel2=self.x_axis_box2.currentText() 
        return self.xlabel2
    
    def get_y_axis2(self):
        return self.y_axis_box2.currentText()
    
    def get_z_axis2(self):
        return self.z_axis_box2.currentText()
    
    def get_conversion_x2(self):
        self.conversion_x2=self.x_conversion_box2.text()
        return self.x_conversion_box2.text()
    
    def get_conversion_y2(self):
        self.conversion_y2=self.y_conversion_box2.text()
        return self.y_conversion_box2.text()
    
    def get_conversion_z2(self):
        self.conversion_z2=self.z_conversion_box2.text()
        return self.z_conversion_box2.text()
       
    def title_give2(self):
        return self.titlebox2.text()
    def get_verlabel(self):
        return self.verlabelbox.currentIndex()
    
    def get_horlabel(self):
        return self.horlabelbox.currentIndex()
    
    def get_offset_hor(self):
        return float(self.offset_hor_box.text())
    
    def get_offset_ver(self):
        return float(self.offset_ver_box.text())
    
    def get_extent_label2(self):
        if self.extentbox2.isChecked():
            return True
        else:
            return False
        
    def get_conduct_label2(self):
        if self.conduct_box2.isChecked():
            self.z_label_box2.setCurrentIndex(conduct_index)
            self.extent_bool2=True
            self.x_label2=labels_dict[self.x_label_box2.currentText()]
            self.y_label2=labels_dict[self.y_label_box2.currentText()]
            self.z_label2=labels_dict[self.z_label_box2.currentText()]
            return True
        else:
            self.z_label_box2.setCurrentIndex(0)
            self.x_label2=labels_dict[self.x_label_box2.currentText()]
            self.y_label2=labels_dict[self.y_label_box2.currentText()]
            self.z_label2=labels_dict[self.z_label_box2.currentText()]
            return False
        
    def get_eh_label2(self):
        if self.eh_box2.isChecked():
            self.z_label_box2.setCurrentIndex(eh_index)
            self.extent_bool2=True
            self.x_label2=labels_dict[self.x_label_box2.currentText()]
            self.y_label2=labels_dict[self.y_label_box2.currentText()]
            self.z_label2=labels_dict[self.z_label_box2.currentText()]
            return True
        else:
            self.z_label_box2.setCurrentIndex(0)
            self.x_label2=labels_dict[self.x_label_box2.currentText()]
            self.y_label2=labels_dict[self.y_label_box2.currentText()]
            self.z_label2=labels_dict[self.z_label_box2.currentText()]
            return False
    
    
    def get_axis_labels2(self):
        if self.x_label_check2.isChecked():
            self.x_label2=labels_dict[self.x_label_box2.currentText()]
            self.y_label2=labels_dict[self.y_label_box2.currentText()]
            self.z_label2=labels_dict[self.z_label_box2.currentText()]
            return True
        else:
            self.x_label2=self.x_axis2
            self.y_label2=self.y_axis2
            self.z_label2=self.z_axis2
            return False
        
    def get_pin_label2(self):
        if self.popupbox2.isChecked():
            return True
        else:
            return False
    
    def colourcode2(self):
        return self.cmapbox2.text()
          
    '''Make the new plot'''
    def update_plot2(self):
        '''Get the values of title and colourcode, These are the only 
        non-automatically updated values since it is text introduction'''
        self.title2=self.title_give2()
        self.cmap2=self.colourcode2()
        self.conversion_x2=self.get_conversion_x2()
        self.conversion_y2=self.get_conversion_y2()
        self.conversion_z2=self.get_conversion_z2()
        if self.labels_bool2:
            self.x_label2=labels_dict[self.x_label_box2.currentText()]
            self.y_label2=labels_dict[self.y_label_box2.currentText()]
            self.z_label2=labels_dict[self.z_label_box2.currentText()]
        else:
            self.x_label2=self.x_axis2
            self.y_label2=self.y_axis2
            self.z_label2=self.z_axis2
            
        '''Do the actual plotting'''
        try:
            self.otherplot.canvas.pseudoplot(self.x_line,self.y_line,self.dataset2,self.data2,
                                        self.variables2,
                                        self.x_axis2,self.y_axis2,self.z_axis2,
                                        self.x_label2,self.y_label2,self.z_label2,
                                        self.conversion_x2,self.conversion_y2,
                                        self.conversion_z2,
                                        title=self.title2,
                                        cmap=self.cmap2,extent_bool=self.extent_bool2,
                                        conduct_bool=self.conduct_bool2,eh_bool=self.eh_bool2)

        except AttributeError:
            self.pop_error_nofile.pop_error()
            
    def popup_hor_prof(self):
        '''Pop ups new windows with the plots. A dictionary is made
        so that each pop up is a new window. Otherwise it rewrites the 
        wimndows'''
        #pop_name='pop_figure'+str(self.counter2)

        #self.pop_dict2[pop_name]=MyPopup_horprofile()

        self.x_axis2=self.get_x_axis2()
        self.y_axis2=self.get_y_axis2()
        self.z_axis2=self.get_z_axis2()
        self.title2=self.title_give2()
        self.cmap2=self.colourcode2()
        self.extent_bool2=self.get_extent_label2()
        self.pinned2=self.get_pin_label2()
        self.offset_hor=self.get_offset_hor()
        if self.labels_bool2:
            self.x_label2=labels_dict[self.x_label_box2.currentText()]
            self.y_label2=labels_dict[self.y_label_box2.currentText()]
            self.z_label2=labels_dict[self.z_label_box2.currentText()]
        else:
            self.x_label2=self.x_axis2
            self.y_label2=self.y_axis2
            self.z_label2=self.z_axis2
            
        if self.pinned2==False:
            self.pop_name2='pop_figure'+str(self.counter2)
            self.pop_dict2[self.pop_name2]=MyPopup_horprofile()
        try:
            self.pop_dict2[self.pop_name2].plotwidget.canvas.plot_hor(self.y_line,self.dataset2,
                                         self.data2,self.variables2,
                                        self.x_axis2,self.y_axis2,self.z_axis2,
                                        self.x_label2,self.y_label2,self.z_label2,
                                        self.conversion_x2,self.conversion_y2,self.conversion_z2,
                                        title=self.title2,
                                        cmap=self.cmap2,extent_bool=self.extent_bool2,
                                        pin=self.pinned2,conduct_bool=self.conduct_bool2,
                                        eh_bool=self.eh_bool2,offset=self.offset_hor)

            if self.pinned2==False:
                self.pop_dict2[self.pop_name2].show()
                self.counter2=self.counter2+1
        except AttributeError as e:
            self.pop_error_nofile.pop_error()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print('Cannot pop up because'+str(e)+' line '+str(exc_tb.tb_lineno))

    def popup_ver_prof(self):
        '''Pop ups new windows with the plots. A dictionary is made
        so that each pop up is a new window. Otherwise it rewrites the 
        wimndows'''

        self.x_axis2=self.get_x_axis2()
        self.y_axis2=self.get_y_axis2()
        self.z_axis2=self.get_z_axis2()
        self.title2=self.title_give2()
        self.cmap2=self.colourcode2()
        self.extent_bool2=self.get_extent_label2()
        self.pinned2=self.get_pin_label2()
        self.offset_ver=self.get_offset_ver()
        if self.labels_bool2:
            self.x_label2=labels_dict[self.x_label_box2.currentText()]
            self.y_label2=labels_dict[self.y_label_box2.currentText()]
            self.z_label2=labels_dict[self.z_label_box2.currentText()]
        else:
            self.x_label2=self.x_axis2
            self.y_label2=self.y_axis2
            self.z_label2=self.z_axis2
            
        if self.pinned2==False:
            self.pop_name3='pop_figure'+str(self.counter3)
            self.pop_dict3[self.pop_name3]=MyPopup_verprofile()
        try:
            self.pop_dict3[self.pop_name3].plotwidget.canvas.plot_ver(self.x_line,self.dataset2,
                                        self.data2,
                                        self.variables2,self.x_axis2,self.y_axis2,
                                        self.z_axis2,
                                        self.x_label2,self.y_label2,self.z_label2,
                                        self.conversion_x2,self.conversion_y2,self.conversion_z2,
                                        title=self.title2,
                                        cmap=self.cmap2,extent_bool=self.extent_bool2,
                                        pin=self.pinned2,conduct_bool=self.conduct_bool2,
                                        eh_bool=self.eh_bool2,offset=self.offset_ver)
            if self.pinned2==False:
                self.pop_dict3[self.pop_name3].show()
                self.counter3=self.counter3+1
        except AttributeError as e:
            self.pop_error_nofile.pop_error()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print('Cannot pop up because'+str(e)+' line '+str(exc_tb.tb_lineno))
    
'''Here the definition of the plotting classes start'''

class PlotWidget(QtWidgets.QWidget):
    
    """ Sets up the environment for the canvas figure"""
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.canvas = PlotCanvas() 
        
        '''This I still dont know how to properly do it, but it will be a way
        to store the variables you are using and then save the steps for
        future plotting of the same graph'''
        self.taken_steps=['']
        
        '''adds the navigation toolbar'''
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setLayout(QtWidgets.QVBoxLayout())
        self.toolbar = NavigationToolbar(self.canvas,self)
        self.toolbar.addSeparator()

        '''Finally add the toolbar and canvas'''
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)

class PlotCanvas(FigureCanvas):
    
    '''This is where the canvas figure of the first tab is made'''
    def __init__(self, x_axis='sr1x',y_axis='Keithrdcv',parent=None, width=5, height=4, dpi=100):

        
        self.poperror=MyPopup_error()
        '''setup the figure'''
        self.fig = Figure(figsize=(width, height), dpi=dpi)       
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(None)
        

        FigureCanvas.setSizePolicy(self,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        '''The grid spec was added when trying to combine the tab1 and tab2
        Since it is no longer necessary it could be chaged, but it works fine
        Maybe in the future they could be combined'''
        self.ax=self.fig.add_gridspec(10, 10)  
        self.range_selector = None
        self.ax1 = self.fig.add_subplot(self.ax[0:10,0:10])
        self.count=0
        
    def plot(self,dataset,data,raw,variables,dimension,
             x_axis,y_axis,z_axis,
             x_label,y_label,z_label,
             normalize_y,normalize_z,
             conversion_x,conversion_y,conversion_z,
             title,cmap,extent_bool,
             normalize_y_bool=False,normalize_z_bool=False,clear_axis=True,
             conduct_bool=False,eh_bool=False,offset=0,
             legend_bool=False,
             min_x=0, max_x=0,min_y=0,max_y=0,min_z=0,max_z=0):
        
        '''Since it is only one plot, fill the full grid space'''
        
        self.data=data
        self.raw_data=raw
        self.variables=variables
        self.normalize_y=normalize_y
        self.normalize_z=normalize_z
        '''Clear the axis, this is neede to be able to refresh the data.
        The same applied for the colorbar (code below)'''

        if clear_axis:
            self.ax1.cla()
            self.count=0
        try:
            if self.cb!=None:
                self.cb.remove()
        except (AttributeError,UnboundLocalError,KeyError) as e:
            pass
        '''Give the right values to the variables and the plot context''' 
        self.x_axis=x_axis
        self.y_axis=y_axis
        self.z_axis=z_axis
        if title=='':
            title=dataset.split('/')[-1]+' '+x_axis+' vs '+y_axis
        if offset==0:
            self.ax1.set_title(title)
        else:
            self.ax1.set_title(title+' offseted by: '+str(offset))
        self.ax1.set_title(title)
        self.ax1.set_xlabel(x_label)
        self.ax1.set_ylabel(y_label)
        
        '''Empty line to store the data, it might not be necessary'''
        if clear_axis:
            self.data_line, = self.ax1.plot([],[])
        else:
            self.data_line, = self.ax1.plot([],[],label=dataset.split('/')[-1])

        '''Distinguish between linescan or 2D map, always start assuming is 1D'''
        self.dimension=dimension
        '''Check if the data is 1D or 2D. Right now it just checks if the 
        first variable is repeated several times and then it assumes it is 
        a megasweep. This can probably be done in a better way'''
        
        #first_var=self.variables[0]
        
        #if getattr(self.data,first_var)[0]==getattr(self.data,first_var)[10]:
            
        #    '''If the data is 2D, convert from normal array to the proper
        #    2D dimensions, this is done with the general_plotting script'''
        #   self.data=general_plotting.map_transform(dataset)
        #   self.dimension=2

        '''Transform with the converison factor, use np to be able
        to multiply'''
        x=np.asarray(getattr(self.data,self.x_axis))*float(conversion_x)
        y=np.asarray(getattr(self.data,self.y_axis))
        z=np.asarray(getattr(self.data,self.z_axis))
        normalize_data_y=np.asarray(getattr(self.data,self.normalize_y))
        normalize_data_z=np.asarray(getattr(self.data,self.normalize_z))
        
        #print(normalize_y_bool)
        
        
        if self.dimension==1:
            cond=np.zeros_like(y)
            cond_eh=np.zeros_like(y)
            norm_Rxx=np.zeros_like(y)
            norm_Rxx_he=np.zeros_like(y)
            
            for i in range(len(y)):
                norm_Rxx[i]=y[i]/normalize_data_y[i] # kOhms
                norm_Rxx_he[i]=norm_Rxx[i]/25812 #h/e2
                cond[i] = 1/y[i]
                #cond[i] = 1/(norm_Rxx[i])  #1/kOhm This one works if you record the current 
                cond_eh[i] = 1/7.75E-5
                
            if normalize_y_bool==True:
                y=norm_Rxx*float(conversion_y)
            elif conduct_bool==True and eh_bool==False:
                y=cond*float(conversion_y)
            elif eh_bool==True:
                y=cond_eh*float(conversion_y)
            else:
                y=y*float(conversion_y)

            try:
                
                self.data_line.set_data(x,y+offset*self.count)

            except AttributeError as e:
                self.poperror.pop_error(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(str(e)+' line '+str(exc_tb.tb_lineno))
            
            if max_x!=0:  
                self.ax1.set_xlim(min_x,max_x)
            if max_y!=0:
                self.ax1.set_ylim(min_y,max_y)
        
        else:
            cond=np.zeros_like(z)
            cond_eh=np.zeros_like(z)
            norm_Rxx=np.zeros_like(z)
            norm_Rxx_he=np.zeros_like(z)
            
            for i in range(len(z)):
                for j in range(len(z[i])):
                    norm_Rxx[i,j]=z[i,j]/normalize_data_z[i,j] # kOhms
                    #norm_Rxx_he[i,j]=norm_Rxx[i,j]/25.8128 #h/e2
                    cond[i,j] = 1/y[i,j]
                    cond_eh[i,j] = cond[i,j]/7.75E-5
                    #cond[i,j] = 1/(norm_Rxx[i,j])  #1/kOhm
                    #cond_eh[i,j] = 1/norm_Rxx_he[i,j] # e^2/h
            
            if normalize_z_bool==True:
                z=norm_Rxx*float(conversion_z)
            if conduct_bool==True:
                z=cond*float(conversion_z)
            elif eh_bool==True:
                z=cond_eh*float(conversion_z)
            else:
                z=z*float(conversion_z)
            '''Whether to use the real axis values or just the size of the data
            is given by extent'''
            if extent_bool==True:
                
                try:    
                    extent=[x[0,0],x[0,-1],
                        y[-1,0],y[0,0]]
                    if max_z==0.0:
                        im=self.ax1.imshow(z,aspect='auto',cmap=cmap,extent=extent)
                    else:
                        im=self.ax1.imshow(z,cmap=cmap,aspect='auto',extent=extent,vmin=min_z,vmax=max_z)
                        
                except AttributeError as e:
                    self.poperror.pop_error(e)
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print(str(e)+' line '+str(exc_tb.tb_lineno))
            else:
                try:
                    im=self.ax1.imshow(z,aspect='auto',cmap=cmap)
                except AttributeError as e:
                    self.poperror.pop_error(e)

            '''create the colorbar'''
            self.cb=self.fig.colorbar(im)
            self.cb.set_label(z_label,fontsize=15)
            self.cb.ax.tick_params(labelsize=15)    

        self.ax1.relim()
        self.ax1.autoscale()
        if clear_axis==False and legend_bool:
            self.ax1.legend(loc='upper center', bbox_to_anchor=(1, 1), shadow=True, ncol=1,fontsize=10)
               
        
        #self.fig.tight_layout()
        '''Finally make the figure'''
        self.count=self.count+1
        self.fig.canvas.draw()
    
    def clear(self):
        self.ax1.cla()
        self.fig.canvas.draw()


'''Make the environment for the plotting of the second tab with the separate
1D and 2D plots'''

class PlotSeparate(QtWidgets.QWidget):
    
    '''This first part is basically the same as PlotWidget'''
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.canvas = SeparatePlot() 
        
        '''adds the navigation toolbar'''
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setLayout(QtWidgets.QVBoxLayout())
        self.toolbar = NavigationToolbar(self.canvas,self)
        self.toolbar.addSeparator()

       
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)
        

class SeparatePlot(FigureCanvas):      
    
    """ Make the plot for the 2nd tab """
    def __init__(self, x_axis='sr1x',y_axis='Keithrdcv',parent=None, width=12, height=8, dpi=100):

        self.poperror=MyPopup_error()
        '''This first part is very similar to the PlotCanvas'''
        self.fig = Figure(figsize=(width, height), dpi=dpi)       
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(None)
        

        FigureCanvas.setSizePolicy(self,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        '''In this case the gridspec is very useful to create the subplots'''
        self.ax=self.fig.add_gridspec(10, 12)  
        self.ax1 = self.fig.add_subplot(self.ax[0:6,0:6])  
        self.ax2 = self.fig.add_subplot(self.ax[7:,0:6])  
        self.ax3 = self.fig.add_subplot(self.ax[1:7,8:])
           
    def pseudoplot(self,line_index1,line_index2,dataset,data,variables, x_axis,
                   y_axis,z_axis,x_label,y_label,z_label,
                   conversion_x,conversion_y,conversion_z,
                   title,cmap,extent_bool,conduct_bool=False,eh_bool=False):


        self.data=data
        self.variables=variables
        '''Create the three subplots, of a certain size. The plot on the 
        right of the map should be in a vertical fashion'''
        
        
        '''Empty the axis so plots can be reloaded'''
        self.ax1.cla()
        self.ax2.cla()
        self.ax3.cla()
        
        try:
            if self.cb!=None:
                self.cb.remove()
        except (AttributeError,UnboundLocalError,KeyError)as e:

            pass
        
        '''Provide the values of the plots and the setup. In this case the 
        plot is always assumed to be two dimensional'''
        self.x_axis=x_axis
        self.y_axis=y_axis
        self.z_axis=z_axis
        self.ax2.set_xlabel(x_label)
        self.ax2.set_ylabel(z_label)
        self.ax3.set_xlabel(z_label)
        self.ax3.set_ylabel(y_label)

        '''The default title is the name of the set with what is plotted,
        by filling the title text this is changed'''
        if title=='':
            title=dataset.split('/')[-1]+' '+z_axis+' msweep '+x_axis+' vs '+y_axis
        else:
            title=title

        x=np.asarray(getattr(self.data,self.x_axis))*float(conversion_x)
        y=np.asarray(getattr(self.data,self.y_axis))*float(conversion_y)
        z=np.asarray(getattr(self.data,self.z_axis))*float(conversion_z)
        
        if conduct_bool==True and eh_bool==False:
                z=1/z
        elif eh_bool==True:
            z=1/z*1E-3/(2*3.877E-5)
            
        if extent_bool==True:
            try: 
                extent=[x[0,0],x[0,-1],
                    y[-1,0],y[0,0]]
                im=self.ax1.imshow(z,aspect='auto',cmap=cmap,extent=extent)
            except AttributeError as e:
                self.poperror.pop_error(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(str(e)+' line '+str(exc_tb.tb_lineno))
            
            '''Give the value of the point where the visual guide line on the 
            2D map will be made. The code below adds the lines on the 2D map
            When extent is done the values have to be multiplied by their position
            on the real data, otherwise the lines are out of the plot, since they
            need to correspond to the axis'''
            
            self.ax1.axvline(x=x[0,line_index1],color='red')
            self.ax1.axhline(y=y[line_index2,0],color='red')

        else:
            try:
                im=self.ax1.imshow(z,aspect='auto',cmap=cmap)
            except AttributeError as e:
                self.poperror.pop_error(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(str(e)+' line '+str(exc_tb.tb_lineno))
            self.ax1.axvline(x=line_index1,color='red')
            self.ax1.axhline(y=line_index2,color='red')
            
        '''The colorbar appears next to the thrid figure, I still dont know how 
        to fix this'''
        cbaxes = self.fig.add_axes([0, 0.45, 0.015, 0.4]) 
        self.cb=self.fig.colorbar(im,cax=cbaxes,format='%.0e')
        #self.cb.ticklabel_format(position='left')
        #self.cb.ax.set_title(self.z_axis)
       # plt.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))
        #self.cb.set_ticks_position('left')

        '''Create the linescans corresponding to the positions on the 2D map'''
        try:
            self.ax2.plot(x[line_index2],z[line_index2])
            self.ax3.plot(z[:,line_index1],y[:,line_index1])
        except AttributeError as e:
            self.poperror.pop_error(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(str(e)+' line '+str(exc_tb.tb_lineno))
        except IndexError:
            self.ax2.plot(x[-1],z[-1])
            self.ax3.plot(z[:,-1],y[:,-1])
        self.ax3.xaxis.tick_top()

        self.ax1.set_title(title)
        self.fig.canvas.draw()
        
'''Profiles for pop up from tab2'''
class PlotProfiles(QtWidgets.QWidget):
    
    '''This first part is basically the same as PlotWidget'''
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.canvas = PlotWidgetProfiles() 
        
        '''adds the navigation toolbar'''
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setLayout(QtWidgets.QVBoxLayout())
        self.toolbar = NavigationToolbar(self.canvas,self)
        self.toolbar.addSeparator()
        
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)
        
        '''Custom save part'''
        self.customsave= QtWidgets.QAction('Activate customsave')
        self.customsave.setIconText('Custom save')
        self.customsave.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.customsave.triggered.connect(self.custom_save)
        
        self.toolbar.addAction(self.customsave)
        self.toolbar.addSeparator()
        
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)
        
    def custom_save(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, filters = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()",custom_direct,"PNG(*.png);;PDF (*.pdf)", options=options)
        if filters=='PNG(*.png)':
            extension='.png'
        elif filters=='PDF (*.pdf)':
            extension='.pdf'
            
        self.canvas.fig.savefig(fileName,dpi=300)


        f=open(fileName+'.txt','w+')
        f.write('dataset\t'+self.canvas.dataset+'\n'+
                'x_axis\t'+self.canvas.x_axis+'\n'+
                'y_axis\t'+self.canvas.y_axis+'\n'+
                'z_axis\t'+self.canvas.z_axis+'\n'+
                'x_label\t'+self.canvas.x_label+'\n'+
                'y_label\t'+self.canvas.y_label+'\n'+
                'z_label\t'+self.canvas.z_label+'\n'+
                'conversion_x\t'+str(self.canvas.conversion_x)+'\n'+
                'conversion_y\t'+str(self.canvas.conversion_y)+'\n'+
                'conversion_z\t'+str(self.canvas.conversion_z)+'\n'+
                'cmap\t'+self.canvas.cmap+'\n'+
                'title\t'+self.canvas.title+'\n'+
                'extent\t'+str(self.canvas.extent_bool)+'\n'+
                'pin\t'+str(self.canvas.pin)+'\n'+
                'conductance\t'+str(self.canvas.conduct_bool)+'\n'+
                'eh\t'+str(self.canvas.eh_bool)+'\n'+
                'offset\t'+str(self.canvas.offset)+'\n'
                )
        for i in range(len(self.canvas.store_index_hor)):
            f.write('line'+str(i)+'\t'+str(self.canvas.store_index_hor[i])+'\n')
        f.close()
        
        '''Here it would also have the step saving'''
    
    
class PlotWidgetProfiles(FigureCanvas):     

    """ Make plot from the map for the pop up window"""
    def __init__(self, x_axis='sr1x',y_axis='Keithrdcv',parent=None, width=12, height=8, dpi=100):

        self.poperror=MyPopup_error()
        '''One plot for the horizontal profiles'''
        self.fig = Figure(figsize=(width, height), dpi=dpi)       
        
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(None)
        

        FigureCanvas.setSizePolicy(self,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        '''In this case the gridspec is very useful to create the subplots'''
        self.ax=self.fig.add_gridspec(10, 10)  
        self.ax1 = self.fig.add_subplot(self.ax[0:10,0:10])
        self.count_lines=0
    def plot_general(self,dataset,data,raw,variables,dimension,
             x_axis,y_axis,z_axis,x_label,y_label,z_label,
             conversion_x,conversion_y,conversion_z,title,cmap,extent_bool,pin,
             conduct_bool=False,eh_bool=False,offset=0,legend_bool=False):
        
        '''Since it is only one plot, fill the full grid space'''
        
        
        self.data=data
        self.raw_data=raw
        self.variables=variables
        self.offset=offset
        '''Clear the axis, this is neede to be able to refresh the data.
        The same applied for the colorbar (code below)'''
        
        if pin==False:
            self.ax1.cla()
            self.count_lines=0
 
        try:
            if self.cb!=None:
                self.cb.remove()
        except (AttributeError,UnboundLocalError,KeyError) as e:

            pass
        '''Give the right values to the variables and the plot context''' 
        self.x_axis=x_axis
        self.y_axis=y_axis
        self.z_axis=z_axis
        if title=='':
            title=dataset.split('/')[-1]+' '+x_axis+' vs '+y_axis
        if self.offset==0:
            self.ax1.set_title(title)
        else:
            self.ax1.set_title(title+' offseted by: '+str(self.offset))

        self.ax1.set_title(title)
        self.ax1.set_xlabel(x_label)
        self.ax1.set_ylabel(y_label)
        
               
        '''Empty line to store the data, it might not be necessary'''
        self.data_line, = self.ax1.plot([],[],label=dataset.split('/')[-1])

        '''Distinguish between linescan or 2D map, always start assuming is 1D'''
        self.dimension=dimension
        

        x=np.asarray(getattr(self.data,self.x_axis))*float(conversion_x)
        y=np.asarray(getattr(self.data,self.y_axis))*float(conversion_y)
        z=np.asarray(getattr(self.data,self.z_axis))*float(conversion_z)
        
        
        if self.dimension==1:
        
            
            cond=np.zeros_like(y)
            cond_eh=np.zeros_like(y)
            #norm_Rxx=np.zeros_like(y)
            #norm_Rxx_he=np.zeros_like(y)
            
            for i in range(len(z)):
                #norm_Rxx[i]=y[i]/normalize_data_y[i] # kOhms
                #norm_Rxx_he[i]=norm_Rxx[i]/25812 #h/e2
                cond[i] = 1/y[i]
                #cond[i] = 1/(norm_Rxx[i])  #1/kOhm This one works if you record the current 
                cond_eh[i] = 1/7.75E-5
                

            if conduct_bool==True and eh_bool==False:
                y=cond*float(conversion_y)
            elif eh_bool==True:
                y=cond_eh*float(conversion_y)
            else:
                y=y*float(conversion_y)
                
            try:
                self.data_line.set_data(x,y+self.offset*self.count_lines)
            except AttributeError as e:
                self.poperror.pop_error(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(str(e)+' line '+str(exc_tb.tb_lineno))
                
        else:

            
            cond=np.zeros_like(z)
            cond_eh=np.zeros_like(z)
            #norm_Rxx=np.zeros_like(z)
           #norm_Rxx_he=np.zeros_like(z)
            
            for i in range(len(z)):
                for j in range(len(z[i])):
                    #norm_Rxx[i,j]=z[i,j]/normalize_data_z[i,j] # kOhms
                    #norm_Rxx_he[i,j]=norm_Rxx[i,j]/25.8128 #h/e2
                    cond[i,j] = 1/y[i,j]
                    cond_eh[i,j] = cond[i,j]/7.75E-5
                    #cond[i,j] = 1/(norm_Rxx[i,j])  #1/kOhm
                    #cond_eh[i,j] = 1/norm_Rxx_he[i,j] # e^2/h
            
            #if normalize_z_bool==True:
            #    z=norm_Rxx*float(conversion_z)
            if conduct_bool==True:
                z=cond*float(conversion_z)
            elif eh_bool==True:
                z=cond_eh*float(conversion_z)
            else:
                z=z*float(conversion_z)
                
            '''Whether to use the real axis values or just the size of the data
            is given by extent'''
            if extent_bool==True:
                    
                try:
                    extent=[x[0,0],x[0,-1],
                    y[-1,0],y[0,0]]
                        
                    im=self.ax1.imshow(z,aspect='auto',cmap=cmap,extent=extent)
                except AttributeError as e:
                    self.poperror.pop_error(e)
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print(str(e)+' line '+str(exc_tb.tb_lineno))
            else:
                try:
 
                    im=self.ax1.imshow(z,aspect='auto',cmap=cmap)
                except AttributeError as e:
                    self.poperror.pop_error(e)
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print(str(e)+' line '+str(exc_tb.tb_lineno))
            '''create the colorbar'''
            self.cb=self.fig.colorbar(im)
            self.cb.set_label(z_label,fontsize=15)
            self.cb.ax.tick_params(labelsize=15)    

        self.ax1.relim()
        self.ax1.autoscale()
        if legend_bool:
            self.ax1.legend()
        #self.fig.tight_layout()
        '''Finally make the figure'''
        self.count_lines=self.count_lines+1
        self.fig.canvas.draw()

            
        
    def plot_hor(self,line_index2,dataset,data,variables,x_axis,
                   y_axis,z_axis,x_label,y_label,z_label,
                   conversion_x,conversion_y,conversion_z,
                   title,cmap,extent_bool,pin,
                   conduct_bool=False,eh_bool=False,offset=0):
        
        '''Since it is only one plot, fill the full grid space'''
        self.dataset=dataset
        self.data=data
        self.variables=variables
        self.pin=pin
        '''Clear the axis, this is neede to be able to refresh the data.
        The same applied for the colorbar (code below)'''
        if pin==False:
            self.ax1.cla()
            self.count_hor=0
            self.store_index_hor=[]

        '''Give the right values to the variables and the plot context''' 
        self.x_axis=x_axis
        self.y_axis=y_axis
        self.z_axis=z_axis
        self.x_label=x_label
        self.y_label=y_label
        self.z_label=z_label
        self.conversion_x=conversion_x
        self.conversion_y=conversion_y
        self.conversion_z=conversion_z
        self.conduct_bool=conduct_bool
        self.eh_bool=eh_bool
        self.cmap=cmap
        self.extent_bool=extent_bool
        self.offset=offset
        if title=='':
            self.title=self.dataset.split('/')[-1]+' '+x_axis+' profile'
        else:
            self.title=title
            self.ax1.set_title(title)
        if offset!=0:
            self.ax1.set_title(self.title+' offseted by: '+str(offset) )
        self.ax1.set_xlabel(x_label)
        self.ax1.set_ylabel(z_label)
        if extent_bool==True:
            legend=y_label+': {0:.4f}'.format(getattr(self.data,self.y_axis)[line_index2,0])
        else:
            legend='Line: '+str(line_index2)    
        '''Empty line to store the data, it might not be necessary'''
        try:
            x=np.asarray(getattr(self.data,self.x_axis)[line_index2])*float(conversion_x)
            y=np.asarray(getattr(self.data,self.z_axis)[line_index2])*float(conversion_z)
            
            if conduct_bool==True and eh_bool==False:
                y=1/y
            elif eh_bool==True:
                y=1/y*1E-3/(2*3.877E-5)
            self.ax1.plot(x,y+offset*self.count_hor, label=legend)
               
        except AttributeError as e:
            self.poperror.pop_error(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(str(e)+' line '+str(exc_tb.tb_lineno))
        self.count_hor=self.count_hor+1    

        #self.ax1.relim()
        #self.ax1.autoscale()
        self.ax1.legend(loc='upper center', bbox_to_anchor=(1, 1), shadow=True, ncol=1,fontsize=10)

        self.store_index_hor.append(line_index2)

        '''Finally make the figure'''
        self.fig.canvas.draw()

    def plot_ver(self,line_index1,dataset,data,variables,x_axis,
                   y_axis,z_axis,x_label,y_label,z_label,
                   conversion_x,conversion_y,conversion_z,
                   title,cmap,extent_bool,pin,
             conduct_bool=False,eh_bool=False,offset=0):
        
        '''Since it is only one plot, fill the full grid space'''
        self.dataset=dataset
        self.data=data
        self.variables=variables
        self.offset=offset
        self.pin=pin
        '''Clear the axis, this is neede to be able to refresh the data.
        The same applied for the colorbar (code below)'''
        if pin==False:
            self.ax1.cla()
            self.count_ver=0
            self.store_index_ver=[]
        '''Give the right values to the variables and the plot context''' 
        self.x_axis=x_axis
        self.y_axis=y_axis
        self.z_axis=z_axis
        self.x_label=x_label
        self.y_label=y_label
        self.z_label=z_label
        self.conversion_x=conversion_x
        self.conversion_y=conversion_y
        self.conversion_z=conversion_z
        self.conduct_bool=conduct_bool
        self.cmap=cmap
        self.extent_bool=extent_bool
        self.eh_bool=eh_bool
        if title=='':
            self.title=self.dataset.split('/')[-1]+' '+y_axis+'profile'
        if offset!=0:
            self.ax1.set_title(title+' offseted by: '+str(offset))
        else:
            self.title=title
            self.ax1.set_title(title)
        self.ax1.set_xlabel(y_label)
        self.ax1.set_ylabel(z_label)
        if extent_bool==True:
            legend=x_label+': {0:.4f}'.format(getattr(self.data,self.x_axis)[0,line_index1])
        else:
            legend='Line: '+str(line_index1)           
        try:
            x=np.asarray(getattr(self.data,self.y_axis)[:,line_index1])*float(conversion_y)
            y=np.asarray(getattr(self.data,self.z_axis)[:,line_index1])*float(conversion_x)
            if conduct_bool==True and eh_bool==False:
                y=1/y
            elif eh_bool==True:
                y=1/y*1E-3/(2*3.877E-5)
                
            self.ax1.plot(x,y+self.count_ver*offset, label=legend)
               
        except AttributeError as e:
            self.poperror.pop_error(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(str(e)+' line '+str(exc_tb.tb_lineno))
            

        self.ax1.relim()
        self.ax1.autoscale()
        self.ax1.legend(loc='upper center', bbox_to_anchor=(1, 1), shadow=True, ncol=1,fontsize=10)

        self.count_ver=self.count_ver+1
        #self.fig.tight_layout()
        '''Finally make the figure'''
        self.store_index_ver.append(line_index1)
        self.fig.canvas.draw()

              
class MyPopup_error(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.width=300
        self.height=200
        self.setGeometry(600,400,self.width,self.height)
        self.setWindowTitle('Wrong axis error')
        #self.setWindowIcon(QtGui.QIcon('danger_sign.png'))
        
        
    def pop_error(self,error_message):
        
        background=QtGui.QImage('QTM_images/x_y_sign.png')
        sImage=background.scaled(QtCore.QSize(self.width,self.height))
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(sImage))                     # 10 = Windowrole
        self.setPalette(palette)
        self.label=QtWidgets.QLabel()
        self.label.setText(str(error_message))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet('QTM_images/error_sign.png')
        
        self.error_layout=QtWidgets.QVBoxLayout()
        
        self.error_layout.addWidget(self.label)
        
        self.setLayout(self.error_layout)
        self.show()
        
class PopError_nofile(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.width=300
        self.height=200
        self.setGeometry(600,400,self.width,self.height)
        self.setWindowTitle('No file selected error')
        self.setWindowIcon(QtGui.QIcon('QTM_images/danger_sign.png'))
        
        
    def pop_error(self):
        
        background=QtGui.QImage('QTM_images/popup_error_sign.png')
        sImage=background.scaled(QtCore.QSize(self.width,self.height))
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(sImage))                     # 10 = Windowrole
        self.setPalette(palette)
        
        self.show()
        
class PopError_wrongfile(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.width=300
        self.height=200
        self.setGeometry(600,400,self.width,self.height)
        self.setWindowTitle('Wrong type of file error')
        self.setWindowIcon(QtGui.QIcon('QTM_images/danger_sign.png'))
        
        
    def pop_error(self):
        
        background=QtGui.QImage('QTM_images/wrong_file_error.png')
        sImage=background.scaled(QtCore.QSize(self.width,self.height))
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(sImage))                     # 10 = Windowrole
        self.setPalette(palette)
        
        self.show()
       
class PopError_wrongtemplate(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.width=300
        self.height=200
        self.setGeometry(600,400,self.width,self.height)
        self.setWindowTitle('Not a template file error')
        self.setWindowIcon(QtGui.QIcon('QTM_images/danger_sign.png'))
        
        
    def pop_error(self):
        
        background=QtGui.QImage('QTM_images/wrong_template_error.png')
        sImage=background.scaled(QtCore.QSize(self.width,self.height))
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(sImage))                     # 10 = Windowrole
        self.setPalette(palette)
        
        self.show()

class MyPopup_figure(QtWidgets.QWidget):
    def __init__(self):
            QtWidgets.QWidget.__init__(self)
            self.width=800
            self.height=500
            self.setGeometry(600,400,self.width,self.height)
            self.setWindowTitle('Pop up figure')
            window_icon=QtGui.QIcon()
            window_icon.addFile('QTM_images/spin_logo.png')

            self.setWindowIcon(window_icon)
            #self.setWindowIcon(QtGui.QIcon('danger_sign.png'))
            
            self.plotwidget=PlotProfiles()
            self.popwindow_layout=QtWidgets.QVBoxLayout()
            self.popwindow_layout.addWidget(self.plotwidget)
            self.setLayout(self.popwindow_layout)

class MyPopup_horprofile(QtWidgets.QWidget):
    def __init__(self):
            QtWidgets.QWidget.__init__(self)
            self.width=800
            self.height=500
            self.setGeometry(600,400,self.width,self.height)
            self.setWindowTitle('Horizontal profiles')
            window_icon=QtGui.QIcon()
            window_icon.addFile('QTM_images/spin_logo.png')

            self.setWindowIcon(window_icon)
            
            self.plotwidget=PlotProfiles()
            self.popwindow_layout=QtWidgets.QVBoxLayout()
            self.popwindow_layout.addWidget(self.plotwidget)
            self.setLayout(self.popwindow_layout)
class MyPopup_verprofile(QtWidgets.QWidget):
    def __init__(self):
            QtWidgets.QWidget.__init__(self)
            self.width=800
            self.height=500
            self.setGeometry(600,400,self.width,self.height)
            self.setWindowTitle('Vertical profiles')  
            window_icon=QtGui.QIcon()
            window_icon.addFile('QTM_images/spin_logo.png')

            self.setWindowIcon(window_icon)
            self.plotwidget=PlotProfiles()
            self.popwindow_layout=QtWidgets.QVBoxLayout()
            self.popwindow_layout.addWidget(self.plotwidget)
            self.setLayout(self.popwindow_layout)
        
        
       
'''Below is codeslightly modified from the code used by Kanger JS in the gui
plotting script o try to apply it to our case. The code is used 
to select lines on the plots and use that data. 
In our case is harder because we use imshow instead of plot, since 
we have the 2D data. Therefore I finally have not used it. It could be implemented
eventually, but it does not seem easy to do. '''
'''     
class DraggableHLine:
    """ class to create a draggable horizontal line in a plot 
    Based on the code by KangerJS"""
    def __init__(self, line, ydata):
        self.line = line
        self.press = None
        self.ydata = ydata

    def find_nearest(self, y):
        idy = (np.abs(self.ydata - y)).argmin()
        return self.ydata[idy]

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.line.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.line.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.line.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.line.axes: return
        contains, _ = self.line.contains(event)
        if not contains: return
        y,_ = self.line.get_ydata()
        self.press = y, event.ydata

    def on_motion(self, event):
        if self.press is None: return
        if event.inaxes != self.line.axes: return
        y, ypress = self.press
        dy = event.ydata - ypress
        y_clip = self.find_nearest(y+dy)
        self.line.set_ydata([y_clip, y_clip])
        self.line.figure.canvas.draw()

    def on_release(self, event):
        self.press = None
        self.line.figure.canvas.draw()

    def disconnect(self):
        self.line.figure.canvas.mpl_disconnect(self.cidpress)
        self.line.figure.canvas.mpl_disconnect(self.cidrelease)
        self.line.figure.canvas.mpl_disconnect(self.cidmotion)

class RangeSelector:
    """ class that creates a rangeselector in a plot consisting of two draggable vertical lines 
        Based on the code by KangerJS"""

    def __init__(self, ax, ydata):
        
        
        self.ax = ax
        self.ydata = ydata
        print(ydata)
        self.ymin = np.min(ydata)
        self.ymax = np.max(ydata)
        self.hline1 = self.ax.axhline(y=self.ymin, linewidth=1, linestyle='--', color='gray')
        #self.vline2 = self.ax.axvline(x=self.xmax, linewidth=4, linestyle='--', color='gray')
        self.dhl = DraggableHLine(self.hline1, ydata)
        self.dhl.connect()
        #self.dv2 = DraggableHLine(self.vline2, xdata)
        #self.dv2.connect()

    def get_value(self):
        y1,_ = self.hline1.get_ydata()
        #x2,_ = self.vline2.get_xdata()
        #if x1>x2:
        #    x1, x2 = x2, x1
        return y1

    def __remove__(self):
        self.hline1.remove()
        #self.vline2.remove()   

'''

#%%    
'''Runs the programme'''
if __name__ == '__main__':
#    '''To avoid the kernel from dying'''
#    #app = QApplication(sys.argv)
    #app = QtWidgets.QApplication([])
    app = QtWidgets.QApplication.instance()
    '''The three lines above are key to avoid the kernel from dying. 
    If not used the code runs once and then it rerstarts the Kernel. 
    I dont know why, but I found this solution online and it works very well'''
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    ex=App()

    sys.exit(app.exec_())

    
    
