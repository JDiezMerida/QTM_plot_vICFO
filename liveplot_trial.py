# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 16:29:38 2019

@author: Jaime Diez Merida
"""


import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib

plt.style.use('fivethirtyeight')

x_vals=[]
y_vals=[]

#plt.plot(x_vals,y_vals)



def meas_range(start, end,interv):
    x = np.arange(start, end, interv)
    return x

# Set the range of the sweeping and steps 
x=meas_range(0,6,0.1)

# How many variables do you measure and want to plot? 

variables=2

# Set which variable to plot 
''' This will actually be defined by your instrument values''' 
function={}

def y_plot(x):
    y=np.sin(x)
    return y
def y_plot2(x):
    y=np.cos(x)
    return y

'''up to here'''
''' now this is where you plot, which would be the real part'''

# Start a plot
''' size always the same'''
fig=plt.figure(figsize=(18,9))
gridx=44
gridy=88
gs=matplotlib.gridspec.GridSpec(gridx,gridy)

'''The number of figures is what will change'''
ax={}
line={}
for i in range(variables):
    ax['i']=fig.add_subplot(gs[0+i*int(gridx/variables):int(gridx/variables),0+i*int(gridy/variables):int(gridy/variables)])
#ax=fig.add_subplot(gs[0:18,:16])
#ax2=fig.add_subplot(gs[20:40,20:40])
line['0']=ax['i'].plot(x, y_plot(x),'o')
line['1']=ax['i'].plot(x, y_plot(x),'o')
#line, = ax.plot(x, y_plot(x),'o')
#line2, = ax2.plot(x, y_plot(x),'o')

# This would be the animation plot
def animate(i):
    line['o'].set_ydata(y_plot(x + i / 10))  # update the data.
    return line['0'],
def animate2(i):
    line['1'].set_ydata(y_plot2(x + i / 10))  # update the data.
    return line['1'],

ani = FuncAnimation(
    fig, animate, interval=100, blit=True, save_count=50)

ani2 = FuncAnimation(
    fig, animate2, interval=100, blit=True, save_count=50)

plt.show()
# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#
# writer = animation.FFMpegWriter(
#     fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)

