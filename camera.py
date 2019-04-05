import os
import platform
from ctypes import *
from numpy import *
        
sllname = 'spectrlib64.dll'
sptdll = windll.LoadLibrary( sllname)
numScans = c_uint16(2)
numblankscans = c_uint8(0)
scanmode = c_uint8(3)
timeofexposure = c_uint32(500)
numstartelement = c_uint16(0)
numendelement = c_uint(3647)
reductionmode = c_uint8(0)
numofpixelsinframe = c_uint16(3694)
sptdll.setExposure( timeofexposure)
sptdll.setAcquisitionParameters( numScans, numblankscans, scanmode, timeofexposure)
sptdll.setFrameFormat(numstartelement,  numendelement, reductionmode,byref( numofpixelsinframe))
sptdll.triggerAcquisition()

##def assignnscan(self,pressed,t):
##    n = c_uint16(int(self.nscantxt.text()))
##    sptdll.setAcquisitionParameters(n,cam.numblankscans,cam.scanmode,cam.timeofexposure)
##    pg.QtGui.QApplication.processEvents()
##    return True
##
##def assignexp(self,pressed):
##    e = c_uint32(int(self.timexp.text()))
##    cam.sptdll.setExposure(cam.timeofexposure)
##    cam.sptdll.setAcquisitionParameters(cam.numScans,cam.numblankscans,cam.scanmode,e)
##    pg.QtGui.QApplication.processEvents()
##    return True
##
##def graph(self):
##        ''' plot some random stuff '''
##    filename = str(r"C:\Users\creates\Desktop\Frog\FROG_soft\DATA_ACQUISITION\\")+str(self.name)+str(".txt")
##    
##    data = np.loadtxt(filename)
##    x = data[:,0] #Scan number
##    y = data[:,1]
##    z = data[:,2] #Intensity
##    zmat = z.reshape(60,3653)
##    print("here")
##    # create an axis
##    ax = self.figure.add_subplot(111)
##    
##    # discards the old graph
##    ax.clear()
##
##    ax.imshow(np.transpose(zmat),cmap = cm.jet,aspect=10,extent=(0,300,370,430),interpolation='nearest')
##
##    self.canvas.draw()
