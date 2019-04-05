import os
##import platform
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QFrame, QApplication)

import pyqtgraph as pg
import pyqtgraph.opengl as gl

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.cm as cm
import camera as cam

import time
import datetime
from ctypes import *
import random

from PyAPT import APTMotor

class widgetAPT(QWidget):
    
    def __init__(self, parent = None, serial=00000000, verbose=False):  ##, verbose=False
        super(widgetAPT, self).__init__(parent)
        self.resize(1300, 650)
        self.setWindowTitle('FROG')
        self.setWindowIcon(QIcon('iiserb.png'))
        
        layout = QGridLayout()
##        self.setLayout(layout)
        

        
        self.data = np.genfromtxt('N1648.txt',skip_header=12,skip_footer=7308)

        # Layout objects
        sStag = QLabel("Stage",self)
        sStag.setStyleSheet("font: 22pt;")
        layout.addWidget(sStag,2,2)
        
        sAuthor = QLabel("Frequency Resolved Optical Gating", self)
        sAuthor.setStyleSheet("font: 40pt; color:green")        
        layout.addWidget(sAuthor,1,3,1,15)
        
        # Motor Serial Number
        
        sSer = QLabel("Serial:", self)
        sSer.setStyleSheet("font: 16pt;")
        layout.addWidget(sSer,3,1)
    
        self.txtSerial = QSpinBox(self)    
        self.txtSerial.setRange(0, 99999999)
        self.txtSerial.setSingleStep(1)
        self.txtSerial.setValue(27503288)
        
    
        layout.addWidget(self.txtSerial,3,2)
        self._Motor_ = APTMotor(verbose=verbose)

        # Motor Connect button
        self.btnConnect = QPushButton("Connect", self)
        self.btnConnect.setStyleSheet("background-color: grey")
        self.btnConnect.setText("Connect")
        self.btnConnect.setCheckable(True)
        self.btnConnect.setToolTip("Connect to Motor")
        self.btnConnect.clicked[bool].connect(self.connectAPT)

        layout.addWidget(self.btnConnect,3,3)
        
        sPos = QLabel("Pos:", self)
        sPos.setStyleSheet("font: 16pt;")
        self.txtPos = QDoubleSpinBox(self)
        self.txtPos.setRange(-5, 13)
        self.txtPos.setSingleStep(.1)
        self.txtPos.setDecimals(5)
        self.txtPos.setValue(0.0000000)
        self.txtPos.setToolTip("Current Motor Position")
        self.txtPos.setEnabled(False)
        layout.addWidget(sPos,4,1)
        layout.addWidget(self.txtPos,4,2)
        
        # Go to position
        self.btnGOp = QPushButton("Go", self)
        self.btnGOp.clicked.connect(lambda: self.motAbs(float(self.txtPos.text())))

        layout.addWidget(self.btnGOp,4,3)

        
        #Home button
        self.btnHome = QPushButton("Home", self)
        self.btnHome.setToolTip("This will take the stage to 6.50")
        layout.addWidget(self.btnHome,5,1,1,1.5)
        self.btnHome.clicked.connect(lambda: self.motAbs(6.50000))

        #go to zero        
        self.btnZero = QPushButton("Go to Zero", self)
        self.btnZero.setToolTip("This will take the stage to absolute 0")
        layout.addWidget(self.btnZero,5,2,1,1.5)
        self.btnZero.clicked[bool].connect(lambda: self._Motor_.go_home())

        
        #Velocity buttons       
       
        sVel = QLabel("Velocity:", self)
        sVel.setStyleSheet("font: 14pt;")        
        
        self.txtVel = QDoubleSpinBox(self)
        self.txtVel.setRange(0, 2.2)
        self.txtVel.setSingleStep(.1)
        self.txtVel.setValue(1.5)
        self.txtVel.setToolTip("set the velocity here")
        self.txtVel.setEnabled(False)

        layout.addWidget(sVel,6,1)
        layout.addWidget(self.txtVel,6,2)
        

        self.btnGOv = QPushButton("Set", self)
        self.btnGOv.clicked.connect(lambda: self._Motor_.setVel(float(self.txtVel.text())))

        layout.addWidget(self.btnGOv,6,3)
        
        sBack = QLabel("Backlash:", self)
        sBack.setStyleSheet("font: 14pt;")
                               
        
        self.cbBacklash = QCheckBox(self)
        layout.addWidget(sBack,7,1)
        layout.addWidget(self.cbBacklash,7,2)
        sSpect = QLabel("Spectrometer",self)
        sSpect.setStyleSheet("font: 22pt;")
        sSpect.setFont(QFont('Arial', 20))
        layout.addWidget(sSpect,8,2)

                
        texp = QLabel("Time of Exp.:", self)
        texp.setStyleSheet("font: 14pt;")
        layout.addWidget(texp,9,1)
        
        self.timexp = QDoubleSpinBox(self)
        self.timexp.setRange(0, 100000)
        self.timexp.setSingleStep(1)
        self.timexp.setDecimals(0)
        self.timexp.setValue(10)
        layout.addWidget(self.timexp,9,2)
        self.btnCh = QPushButton("Set", self)
        layout.addWidget(self.btnCh,9,3)

        nscan = QLabel("Num. of scan:", self)
        nscan.setStyleSheet("font: 14pt;")
        layout.addWidget(nscan,10,1)
        self.nscantxt = QDoubleSpinBox(self)
        self.nscantxt.setRange(0,137)
        self.nscantxt.setSingleStep(1)
        self.nscantxt.setDecimals(0)
        self.nscantxt.setValue(10)
        layout.addWidget(self.nscantxt,10,2)
        self.nscan = QPushButton("Set", self)      
        layout.addWidget(self.nscan,10,3)
        
        #self.timexp.setEnabled(False)

      

        
    
##        self.timeofexposure = c_uint32(1000)           
        
        
        self.btnCh.clicked[bool].connect(self.assignexp)

        self.nscan.clicked[bool].connect(self.assignnscan)

        sSpos = QLabel("Signal pos.(mm):")
        sSpos.setStyleSheet("font: 14pt;")
        self.txtSpos = QDoubleSpinBox(self)
        self.txtSpos.setRange(0, 12.0000)
        self.txtSpos.setDecimals(5)
        self.txtSpos.setSingleStep(0.00001)
        self.txtSpos.setValue(6.50000)
        layout.addWidget(sSpos,12,1)
        layout.addWidget(self.txtSpos,12,2)

        self.btnSpos = QPushButton("Set",self)
        layout.addWidget(self.btnSpos,12,3)
        self.btnSpos.clicked[bool].connect(lambda: self.txtSpos.setValue(float(self.txtSpos.text())))

        sSpectra = QLabel("Spectrum",self)
        sSpectra.setStyleSheet("font: 14pt;")
        sSpectra.setFont(QFont('Arial', 20))
        layout.addWidget(sSpectra,13,1)





#----------------------------Spectromter Plot----------------------------------------------------------------------------------------------------

        
        #time of exposure box
        self.spectra = create_string_buffer(7500)
        pg.setConfigOption('background', 'w')
        self.plot1 = pg.PlotWidget()
        layout.addWidget(self.plot1,3,7,8,8)
        self.timer = pg.QtCore.QTimer()

        self.liveb = QPushButton('Live', self)
        layout.addWidget(self.liveb,13,2)
        self.liveb.setCheckable(True)
        
        self.liveb.clicked[bool].connect(self.live)
        self.lbox=QCheckBox(self)

##        self.timer.timeout.connect(self.updater)
        
        
##        self.static = QCheckBox(self)
        
        layout.addWidget(self.lbox,13,3)
               

        self.fname = QLineEdit(self)
        self.fname.setToolTip("ENTER FILENAME.TXT")
        layout.addWidget(self.fname,14,1,1,2)
        self.sScan = QPushButton("Start Scan",self)
        layout.addWidget(self.sScan,14,3,1,1)
        self.sScan.clicked[bool].connect(self.scan)
        self.pbar = QProgressBar(self)

        layout.addWidget(self.pbar,15,1,1,2)

##        self.spectra = create_string_buffer(7500)
##        cam.sptdll.getFrame(byref(self.spectra),0xFFFF)
##        self.b = np.frombuffer(self.spectra, dtype=np.uint16)
##        self.plot1.plot(self.data,self.b[0:3653],pen='b', clear=True)
##        pg.QtGui.QApplication.processEvents()




                


##-----------------------------------------------------------------------------------------        

        
        self.figure = Figure()

        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.graph)

        # set the layout

        layout.addWidget(self.toolbar,11,7,1,8)
        layout.addWidget(self.canvas,12,7,5,8)
        layout.addWidget(self.button,15,3,1,1)
        self.setLayout(layout)


        self.ex=QPushButton('EXIT',self)
        layout.addWidget(self.ex,16,2,2,1)
        self.ex.clicked.connect(lambda:self._Motor_.cleanUpAPT())

        

#--------------------------------------------------------------------------------------------------------------------------------
##
    def live(self):
        
        if self.lbox.isChecked() :
            self.timer.timeout.connect(self.updater)
            self.timer.start(5)

        else:
            self.timer.stop()

    def updater(self):        
        cam.sptdll.getFrame(byref(self.spectra),0xFFFF)
        self.b = np.frombuffer(self.spectra, dtype=np.uint16)
        self.plot1.plot(self.data,self.b[0:3653],pen='b',clear=True)


        
    def scan(self,pressed):

        self.completed = 0       
            
        self.pbar.setValue(self.completed)            
        #writing in file
        starting=float(self.txtSpos.text())-0.045
        self.motAbs(starting)

        if(self.fname.text()==""):
            now=datetime.datetime.now()
            self.name=now.strftime("%Y %m %d %H %M")

        else:
            self.name=self.fname.text()
        speed=3e8
        for i in range(60):        #replaced 60 by 100
            
            self.completed += 1.66667
            
            self.pbar.setValue(self.completed)
            
            self.motRel(0.00150)


            
            
            fo = open(r"C:\Users\creates\Desktop\Frog\FROG_soft\DATA_ACQUISITION\\"+self.name+".txt", "a+")
            
            cam.sptdll.getFrame(byref(self.spectra),0xFFFF)
            self.b = np.frombuffer(self.spectra, dtype=np.uint16)
            fo.write("\t")
            
            for j in range (3653):
                fo.write(str((i+1-30)*(0.000015)*(1/speed)))
                fo.write("\t")
                fo.write(str(self.data[j]))
                fo.write("\t")
                fo.write(str(self.b[j]))
                fo.write("\n")
                fo.write("\t")
            fo.close()
        self.completed = 100
        self.pbar.setValue(self.completed)
        return True



    def assignexp(self,pressed):
        e = c_uint32(int(self.timexp.text()))
        cam.sptdll.setExposure(cam.timeofexposure)
        cam.sptdll.setAcquisitionParameters(cam.numScans,cam.numblankscans,cam.scanmode,e)
        pg.QtGui.QApplication.processEvents()
        return True

    def assignnscan(self,pressed):
        n = c_uint16(int(self.nscantxt.text()))
        cam.sptdll.setAcquisitionParameters(n,cam.numblankscans,cam.scanmode,cam.timeofexposure)
        pg.QtGui.QApplication.processEvents()
        return True
    
    def connectAPT(self, pressed):
        if pressed:
            #APT Motor connect
            Serial = int(self.txtSerial.text())
            self._Motor_.setSerialNumber(Serial)
            self._Motor_.initializeHardwareDevice()

            # Success
            self.btnConnect.setStyleSheet("background-color: green")
            self.btnConnect.setText("Connected")

            self.txtSerial.setEnabled(False)
            self.txtPos.setEnabled(True)
            # Update text to show position
            self.txtPos.setValue( self._Motor_.getPos() )

            self.txtVel.setEnabled(True)
            _, _, maxVel = self._Motor_.getVelocityParameters()
            self.txtVel.setValue( maxVel )
            self._Motor_.go_home()

            return True
        else:
            self.btnConnect.setStyleSheet("background-color: grey")
            self.btnConnect.setText("Connect")

            self.txtSerial.setEnabled(True)
            self.txtPos.setEnabled(False)
            self.txtVel.setEnabled(False)
            self.txtPos.setValue(0.0000)
            self.txtPos.setToolTip("Current Motor Position")
            return True

    def motRel(self, relDistance):
        self._Motor_.setVel(float(self.txtVel.text()))
        if self.cbBacklash.isChecked() :
            self._Motor_.mbRel(relDistance)
        else:
            self._Motor_.mcRel(relDistance)

        self.txtPos.setValue( self._Motor_.getPos() )


        
    def motAbs(self, absDistance):
        self._Motor_.setVel(float(self.txtVel.text()))
        if self.cbBacklash.isChecked() :
            self._Motor_.mbAbs(absDistance)
        else:
            self._Motor_.mAbs(absDistance)
        # Update text to show position
        self.txtPos.setValue( self._Motor_.getPos() )


    


    def graph(self):
        ''' plot some random stuff '''
        filename = str("max2_F.txt")
        
        data = np.loadtxt(filename)
        x = data[:,0] #Scan number
        y = data[:,1]
        z = data[:,2] #Intensity
        zmat = z.reshape(60,3653)
##        print("here")
        # create an axis
        
        ax = self.figure.add_subplot(111)
        ax2 = self.figure.add_subplot(112)
        # discards the old graph
        ax.clear()

        ax.imshow(np.transpose(zmat),cmap = cm.jet,aspect=10,extent=(-150,150,370,430),interpolation='nearest') ##,aspect=10,extent=(0,300,370,430)

        self.canvas.draw()
        

        
        

    

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    form = widgetAPT(verbose=True)
    form.setWindowState(Qt.WindowMaximized)
    form.show()  
    #sys.exit(app.exec_())
    sys.exit(segmentation.exec_())

