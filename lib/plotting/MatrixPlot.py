# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:51:43 2015

@author: sigurd
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputPlot',
                    help = 'input stucture for onclick',
                    default = "Delta")
                    
args = parser.parse_args()
plot = args.inputPlot



#Load values created by Matrix.py
x_axisLength = np.load("axisLength.npy")
y_axisLength = x_axisLength
x_axis = np.load("x_axis.npy")
y_axis = np.load("y_axis.npy")
data = np.load("Matrix_"+plot+".npy")

#overlay = []
#for i in data:
#    if 4.8 <= i <= 5:
        


plt.figure(figsize=(36, 2), dpi=80)
plt.imshow(data, interpolation='nearest', cmap=plt.cm.jet, aspect = 'auto',origin="lower")
im = plt.imshow(data, interpolation='nearest', cmap=plt.cm.jet, aspect = 'auto',origin="lower")
fig = plt.gcf()
ax = plt.gca()

class EventHandler:
    def __init__(self):
        fig.canvas.mpl_connect('button_press_event', self.onpress)
        
    def onpress(self, event):
        if event.inaxes!=ax:
            return
        xi, yi = (int(round(n)) for n in (event.xdata, event.ydata))
        value = im.get_array()[xi,yi]
        color = im.cmap(im.norm(value))
        print xi,yi,value,color


#if plot == "2ABH":
#    im.cmap.set_over('k')
#    im.cmap.set_under('b')
#    im.set_clim(14, 19)
#if plot == "1OIB":
#    im.cmap.set_over('k')
#    im.cmap.set_under('b')
#    im.set_clim(8, 15)
#if plot == "Delta":
#    im.cmap.set_over('k')
#    im.cmap.set_under('b')
#    im.set_clim(3.0, 6)


handler = EventHandler()
cb = plt.colorbar()
cb.set_label('Displacement [$\AA$]')
plt.title("Displacement of "+plot+"")
plt.xticks(x_axisLength,x_axis, rotation = 90)
plt.yticks(y_axisLength,y_axis)
plt.savefig("matrix_selected_"+plot+".png")
plt.show()



