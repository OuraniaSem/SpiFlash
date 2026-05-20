import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QTabWidget,QVBoxLayout, QFileDialog
from PyQt5.QtGui import QIcon
from pandas.core import base
from barplot import main_barplot, plot_things
from trainingTrace import main_training, plot_things_training
from psycho import main_psycho, plot_things_psycho
from weibull_S import main_weibull, plot_things_weibull
from sensitivity import main_sensitivity, plot_sensitivity
from wrap_json import main_wrap, main_wrap_2afc
from concatenation import barplot_concatenation, barplot_concatenation_only, psycho_concatenation_only, training_concatenation, psycho_concatenation, weibull_concatenation
from synchronization import synchronization_test
#from two_afc import barplot_2afc, psycho_2afc, heatmap_2afc, training_2afc, priors_analysis_2afc
from two_afc import barplot_2afc, psycho_2afc, training_2afc, priors_analysis_2afc
from alternative_heatmap import alternative_heatmap_2afc
from Heatmap_GNG import Heatmap_GNG
from concatenation_2afc import psycho_2afc_concat, barplot_2afc_concat, priors_2afc_concat

'''
The App class inherits from QMainWindow, which is a base class for the main windows of the application. 
In the constructor of the App class, several GUI variables are initialized, including the window title, window position and window size.
The main window contains an instance of the MyTableWidget class, which inherits from QWidget. 
MyTableWidget is the class that defines the tabs, buttons and functions of the GUI.
In the constructor of the MyTableWidget class, several tabs are created using the QTabWidget class.
The tabs "Experiments", "Concatenation", "Synchronization" & "2AFC"  are added with addTab.
Each tab contains buttons that trigger functions that perform specific operations.
'''
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'SpiFlash'
        self.left = 10
        self.top = 10
        self.width = 430
        self.height = 300
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()

'''
The class has a constructor with parent parameter which is used to set the parent widget.
In the constructor, the parent class is called with the super method, and a vertical layout is created with QVBoxLayout.
The class has four tabs - tab1, tab2, tab3, and tab4 - and a QTabWidget is created. The tabs are added to the QTabWidget using the addTab method.
For each tab, a vertical layout is created, and several QPushButton widgets are added to the layout using the addWidget method.
Each button is connected to a corresponding method.
'''  
class MyTableWidget(QWidget):

    def __init__(self, parent):

        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1, "Experiments")
        self.tabs.addTab(self.tab2, "Concatenation")
        self.tabs.addTab(self.tab3, "Synchronization")
        self.tabs.addTab(self.tab4, "2AFC")
        self.tabs.addTab(self.tab5, "2AFC concatenation")
        
        # Experiments Part
        self.tab1.layout = QVBoxLayout(self) # Creation of a layout 

        '''
        These lines of code create a button, connect it to a method, add it to a layout, and set the layout for a tab in the current QWidget.
        '''
        # Create a QPushButton with the text "Choose Path" and set it as a child of the current QWidget
        self.pybutton_path = QPushButton('Choose Path', self)

        # Connect the "clicked" signal of the QPushButton to the "click_choose" method of the current QWidget
        self.pybutton_path.clicked.connect(self.click_choose)

        # Add the QPushButton to the layout of the current QWidget's first tab
        self.tab1.layout.addWidget(self.pybutton_path)

        # Set the layout of the current QWidget's first tab to the previously modified layout
        self.tab1.setLayout(self.tab1.layout)

        #same way for the other buttons 
        self.pybutton_barplot = QPushButton('Barplot', self)
        self.pybutton_barplot.clicked.connect(self.click_barplot)
        self.tab1.layout.addWidget(self.pybutton_barplot)
        self.tab1.setLayout(self.tab1.layout)

        self.pybutton_training = QPushButton('Training', self)
        self.pybutton_training.clicked.connect(self.click_training)
        self.tab1.layout.addWidget(self.pybutton_training)
        self.tab1.setLayout(self.tab1.layout)

        self.pybutton_psycho = QPushButton('Psychometric', self)
        self.pybutton_psycho.clicked.connect(self.click_psycho)
        self.tab1.layout.addWidget(self.pybutton_psycho)
        self.tab1.setLayout(self.tab1.layout)

        self.pybutton_sensitivity = QPushButton('Sensitivity', self)
        self.pybutton_sensitivity.clicked.connect(self.click_sensitivity)
        self.tab1.layout.addWidget(self.pybutton_sensitivity)
        self.tab1.setLayout(self.tab1.layout)

        self.pybutton_weibull = QPushButton('Weibull', self)
        self.pybutton_weibull.clicked.connect(self.click_weibull)
        self.tab1.layout.addWidget(self.pybutton_weibull)
        self.tab1.setLayout(self.tab1.layout)

        self.pybutton_weibull = QPushButton('Wrap Json', self)
        self.pybutton_weibull.clicked.connect(self.click_wrap)
        self.tab1.layout.addWidget(self.pybutton_weibull)
        self.tab1.setLayout(self.tab1.layout)

        self.pybutton_Heatmap_GNG = QPushButton('Heat map', self)
        self.pybutton_Heatmap_GNG.clicked.connect(self.click_Heatmap_GNG)
        self.tab1.layout.addWidget(self.pybutton_Heatmap_GNG)
        self.tab1.setLayout(self.tab1.layout)

        # CONCATENATION PART
        self.tab2.layout = QVBoxLayout(self)

        self.pybutton_directory = QPushButton('Choose directory', self)
        self.pybutton_directory.clicked.connect(self.click_choose_directory)
        self.tab2.layout.addWidget(self.pybutton_directory)
        self.tab2.setLayout(self.tab2.layout)

        self.pybutton_barplot_concatenation = QPushButton('Barplot', self)
        self.pybutton_barplot_concatenation.clicked.connect(self.click_barplot_concatenation)
        self.tab2.layout.addWidget(self.pybutton_barplot_concatenation)
        self.tab2.setLayout(self.tab2.layout)

        self.pybutton_barplot_concatenation_only = QPushButton('Barplot (Concatenation only)', self)
        self.pybutton_barplot_concatenation_only.clicked.connect(self.click_barplot_concatenation_only)
        self.tab2.layout.addWidget(self.pybutton_barplot_concatenation_only)
        self.tab2.setLayout(self.tab2.layout)

        self.pybutton_training_concatenation = QPushButton('Training', self)
        self.pybutton_training_concatenation.clicked.connect(self.click_training_concatenation)
        self.tab2.layout.addWidget(self.pybutton_training_concatenation)
        self.tab2.setLayout(self.tab2.layout)

        self.pybutton_psycho = QPushButton('Psychometric', self)
        self.pybutton_psycho.clicked.connect(self.click_psycho_concatenation)
        self.tab2.layout.addWidget(self.pybutton_psycho)
        self.tab2.setLayout(self.tab2.layout)

        self.pybutton_psycho_only = QPushButton('Psychometric only', self)
        self.pybutton_psycho_only.clicked.connect(self.click_psycho_concatenation_only)
        self.tab2.layout.addWidget(self.pybutton_psycho_only)
        self.tab2.setLayout(self.tab2.layout)

        self.pybutton_weibull = QPushButton('Weibull', self)
        self.pybutton_weibull.clicked.connect(self.click_weibull_concatenation)
        self.tab2.layout.addWidget(self.pybutton_weibull)
        self.tab2.setLayout(self.tab2.layout)

        # SYNCHRONIZATION PART
        self.tab3.layout = QVBoxLayout(self)

        self.pybutton_directory_sync = QPushButton('Choose directory', self)
        self.pybutton_directory_sync.clicked.connect(self.click_choose_directory)
        self.tab3.layout.addWidget(self.pybutton_directory_sync)
        self.tab3.setLayout(self.tab3.layout)

        self.pybutton_synchronization = QPushButton('Synchronization', self)
        self.pybutton_synchronization.clicked.connect(self.click_synchronization)
        self.tab3.layout.addWidget(self.pybutton_synchronization)
        self.tab3.setLayout(self.tab3.layout)

        # 2AFC PART
        self.tab4.layout = QVBoxLayout(self)

        self.pybutton_path = QPushButton('Choose Path', self)
        self.pybutton_path.clicked.connect(self.click_choose)
        self.tab4.layout.addWidget(self.pybutton_path)
        self.tab4.setLayout(self.tab4.layout)

        self.pybutton_barplot = QPushButton('Barplot', self)
        self.pybutton_barplot.clicked.connect(self.click_barplot_2AFC)
        self.tab4.layout.addWidget(self.pybutton_barplot)
        self.tab4.setLayout(self.tab4.layout)

        self.pybutton_Training_2AFC = QPushButton('Training', self)
        self.pybutton_Training_2AFC.clicked.connect(self.click_training_2AFC)
        self.tab4.layout.addWidget(self.pybutton_Training_2AFC)
        self.tab4.setLayout(self.tab4.layout)

        self.pybutton_Psycho_2AFC = QPushButton('Psychometric Curve', self)
        self.pybutton_Psycho_2AFC.clicked.connect(self.click_psycho_2AFC)
        self.tab4.layout.addWidget(self.pybutton_Psycho_2AFC)
        self.tab4.setLayout(self.tab4.layout)

        self.pybutton_Heatmap_2AFC = QPushButton('HeatMap', self)
        self.pybutton_Heatmap_2AFC.clicked.connect(self.click_Heatmap_2AFC)
        self.tab4.layout.addWidget(self.pybutton_Heatmap_2AFC)
        self.tab4.setLayout(self.tab4.layout)

        self.pybutton_priors_2AFC = QPushButton('Priors analysis', self)
        self.pybutton_priors_2AFC.clicked.connect(self.click_priors_2AFC)
        self.tab4.layout.addWidget(self.pybutton_priors_2AFC)
        self.tab4.setLayout(self.tab4.layout)

        self.pybutton_wrapJson_2AFC = QPushButton('Wrap Json', self)
        self.pybutton_wrapJson_2AFC.clicked.connect(self.click_wrap_2AFC)
        self.tab4.layout.addWidget(self.pybutton_wrapJson_2AFC)
        self.tab4.setLayout(self.tab4.layout)

        # Concatenation part 2AFC
        self.tab5.layout = QVBoxLayout(self)

        self.pybutton_directory = QPushButton('Choose directory', self)
        self.pybutton_directory.clicked.connect(self.click_choose_directory)
        self.tab5.layout.addWidget(self.pybutton_directory)
        self.tab5.setLayout(self.tab5.layout)

        self.pybutton_barplot_2afc_concatenation = QPushButton('Barplot 2AFC', self)
        self.pybutton_barplot_2afc_concatenation.clicked.connect(self.click_barplot_2afc_concatenation)
        self.tab5.layout.addWidget(self.pybutton_barplot_2afc_concatenation)
        self.tab5.setLayout(self.tab5.layout)

        self.pybutton_psycho_2afc_concatenation = QPushButton('Psychometric 2AFC', self)
        self.pybutton_psycho_2afc_concatenation.clicked.connect(self.click_psycho_2afc_concatenation)
        self.tab5.layout.addWidget(self.pybutton_psycho_2afc_concatenation)
        self.tab5.setLayout(self.tab5.layout)

        self.pybutton_priors_2afc_concatenation = QPushButton('Priors 2AFC', self)
        self.pybutton_priors_2afc_concatenation.clicked.connect(self.click_priors_2afc_concatenation)
        self.tab5.layout.addWidget(self.pybutton_priors_2afc_concatenation)
        self.tab5.setLayout(self.tab5.layout)


        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    '''
    Here you can find all the methods associated to each button
    '''
    def click_choose(self):
        file_path = QFileDialog.getOpenFileName(self, "Please select the folder path", "D:\vibrotactile task") #D:\vibrotactile task
        print(file_path)
        self.xl_path = str(file_path[0])
        dirname, self.basename = os.path.split(file_path[0]) 
        self.pybutton_path.setText(self.basename)
        print(file_path[0])
    
    def click_barplot(self):
        dico, value_x, sensitivity, pourcent_value, title_plot, dir_name = main_barplot(self.xl_path)
        self.pybutton_barplot.setText(sensitivity)
        plot_things(value_x,pourcent_value, title_plot, dir_name)
        
    def click_training(self):
        value_x_trainig, hit_value_training, timeout_value_training, title_plot, dir_name = main_training(self.xl_path)
        plot_things_training(value_x_trainig, hit_value_training, timeout_value_training, title_plot, dir_name)
    
    def click_psycho(self):
        liste_hit, liste_amp, dico_hit, dico_full, title_plot, dir_name  = main_psycho(self.xl_path)

        if len(liste_amp) <= 1 :
            return
        else:
            plot_things_psycho(liste_hit, liste_amp, title_plot, dir_name)
    
    def click_sensitivity(self):
        liste_sensitivity, liste_AF = main_sensitivity(self.xl_path)
        plot_sensitivity(liste_sensitivity, liste_AF)

    def click_weibull(self):
        liste_hit, liste_amp, dico_hit, dico_full = main_weibull(self.xl_path)

        if len(liste_amp) <= 1 :
            return
        else:
            plot_things_weibull(liste_hit, liste_amp)
    def click_Heatmap_GNG(self):
        Heatmap_GNG(self.xl_path)

    def click_wrap(self):
        main_wrap(self.xl_path, self.basename)
    
    def click_choose_directory(self):
        self.file_path = QFileDialog.getOpenFileNames(self, "Please select the folder path", "D:\vibrotactile task") #D:\vibrotactile task
        print('folderpath', self.file_path)
        self.pybutton_directory.setText("Folder ok !")
    
    def click_barplot_concatenation(self):
        barplot_concatenation(self.file_path)
    
    def click_barplot_concatenation_only(self):
        barplot_concatenation_only(self.file_path)
    
    def click_training_concatenation(self):
        training_concatenation(self.file_path)
    
    def click_psycho_concatenation(self):
        psycho_concatenation(self.file_path)

    def click_psycho_concatenation_only(self):
        psycho_concatenation_only(self.file_path)
    
    def click_weibull_concatenation(self):
        weibull_concatenation(self.file_path)
    
    def click_weibull_concatenation(self):
        weibull_concatenation(self.file_path)
    
    def click_synchronization(self):
        synchronization_test(self.file_path)
    
    def click_barplot_2AFC(self):
        barplot_2afc(self.xl_path)
    
    def click_training_2AFC(self):
        training_2afc(self.xl_path)

    def click_psycho_2AFC(self):
        psycho_2afc(self.xl_path)

    def click_Heatmap_2AFC(self):
        alternative_heatmap_2afc(self.xl_path)

    def click_priors_2AFC(self):
        priors_analysis_2afc(self.xl_path)

    def click_wrap_2AFC(self):
        main_wrap_2afc(self.xl_path, self.basename)

    def click_barplot_2afc_concatenation(self):
        barplot_2afc_concat(self.file_path)

    def click_psycho_2afc_concatenation(self):
        psycho_2afc_concat(self.file_path)

    def click_priors_2afc_concatenation(self):
        priors_2afc_concat(self.file_path)
    
# Allows to launch the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())