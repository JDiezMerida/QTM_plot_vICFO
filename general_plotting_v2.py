# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 10:24:11 2019

@authors: Daan Wielens, Chuan Li, Jaime Diez 
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import time
import glob
import os
directory=''

#%%
'''
Dummy class. Necessary to be able to add attributes to the class object later
on.
'''
class Object():
    pass


'''PREAMBLE FOR PLOTTING LINESCANS AND MAPS IN RIGHT UNITS'''
'''
ac_excitation put the values of lockin 1 and 2 (sr1 and sr2 excitation)
ac_convert is what the TRITON summing module does to the ac signal,again in both
lockins if plotting the 7TESLA this can just be an array with [1,1]
dc_convert also relates to the TRITON conversion box
cmap is the colour of the maps to be plotted
font is the font of the axis and title in the graphs
'''
ac_excit=[0.1,0.02] #For lockin 1 and lockin 2 (sr1 and sr2, respectively)
ac_convert= np.array([100*10/ac_excit[0],100*10/ac_excit[1]],dtype='float') 
#ac_convert=np.array([1,1],dtype='float')
dc_convert=[10,10]
cmap='RdBu'
font=15

'''LINESCANS'''
'''PREAMBLE, make matrices for the labels and multipliers, 
    which are the same size as names
   The names should include all the possible variables of the measurements
   The multiplier tells which value to multiply the original data from to get
   the right units
   The labels relate to this multiplier to give the units wanted
   For example in the KeithHdci every Amp correspond to 688 Gauss
   Labels and multipliers are then added to the mult, lab objects and the 
   proper one can just be called as mult_1D.sr1x for example'''
   
names= ['KeithHdci',
           'KeithBdcv',
           'DFdac1', 
           'DFdac1b', 
           'DFdac2',
           'DFdac2b',
           'KeithRdcv', 
           'KeithR2dcv', 
           'sr1x',
           'sr1y', 
           'sr1r', 
           'sr1amp', 
           'sr1freq', 
           'sr2x', 
           'sr2y',
           'sr2r', 
           'oxMfvalue', 
           'Tritontemp5', 
           'Tritontemp8', 
           'Tritontemp11']
multiplier=[688,1,1,1,1,1,dc_convert[0],dc_convert[1],ac_convert[0],
            ac_convert[0],ac_convert[0],1,1,ac_convert[1],ac_convert[1],
            ac_convert[1],1,1,1,1,1,1]
labels=['Field [G]','Gate [V]','Current [nA]','Current [nA]','Current [nA]',
           'Current [nA]','Bias [mV]','Bias [mV]',
        'R [k'+r'$\Omega]$','R [k'+r'$\Omega]$','R [k'+r'$\Omega]$',
        'sr1amp','sr1Freq','R [k'+r'$\Omega]$','R [k'+r'$\Omega]$',
        'R [k'+r'$\Omega]$','Field [T]', 
        'Temperature [K]','Temperature [K]','Temperature [K]']

'''Set the correct multiplier for later'''
mult=Object()
for i in range(len(names)):
    setattr(mult,names[i],multiplier[i])
'''Right labels for the axis'''
lab=Object()
for i in range(len(names)):
    setattr(lab,names[i],labels[i])
    
'''2D MAPS'''   
'''PREAMBLE, make matrices for the labels and multipliers, 
    which are the same size as names. Names, multipliers and labels same idea
    as for the linescans'''
'''
    names_2D=['KeithHdci',
 'KeithBdcv',
 'DFdac1',
 'DFdac1b',
 'DFdac2',
 'DFdac2b',
 'KeithRdcv',
 'KeithR2dcv',
 'sr1x',
 'sr1y',
 'sr1r',
 'sr1amp',
 'sr1freq',
 'sr2x',
 'sr2y',
 'sr2r',
 'sr2amp',
 'sr2freq',
 'oxMfvalue',
 'Tritontemp5',
 'Tritontemp8',
 'Tritontemp11']


#multiplier_2D=[688,1,1,1,1,1,dc_convert[0],dc_convert[1],ac_convert[0],
               ac_convert[0],ac_convert[0],1,1,ac_convert[1],ac_convert[1],
               ac_convert[1],1,1,1,1,1,1]
#labels_2D=['Field [G]','Gate (V)','Current [nA]','Current [nA]',
           'Current [nA]','Current [nA]','Bias [mV]','Bias [mV]',
           'R [k'+r'$\Omega]$','R [k'+r'$\Omega]$','R [k'+r'$\Omega]$',
           'sr1amp','sr1Freq','R [k'+r'$\Omega]$','R [k'+r'$\Omega]$',
           'R [k'+r'$\Omega]$','sr1amp','sr1freq','Field [T]', 
           'Temperature [K]','Temperature [K]','Temperature [K]']
mult_2D=Object()
for i in range(len(names_2D)):
    setattr(mult_2D,names_2D[i],multiplier_2D[i])
    
lab_2D=Object()
for i in range(len(names_2D)):
    setattr(lab_2D,names_2D[i],labels_2D[i])
    '''
#%%

def parse_data(fname,skiprows=3):
    # Prepare the data: remove the dots
    with open(fname) as myfile:
        head = [next(myfile) for x in range(skiprows)]
        #head_command = head[1].replace('.','')
        head_names = head[2].replace(' ','')
        head_names = head_names.replace('-','')
        head_names = head_names.replace('.','')
        #head_unit = head_names.replace('\n','')

        data = np.loadtxt(fname,delimiter = ',',skiprows=skiprows)
        names = head_names.split(",");
    
    # Parse the data into a class with attributes    
    fdata = Object()  
    for i in range(len(names)-1):
        setattr(fdata, names[i], data[:,i])
    
    return fdata,data,names

def load_manyfiles(keyword='**',directory='',sort_par='Tritontemp8'):
    file_list = glob.glob(os.path.join(os.getcwd(),directory, keyword))
    #store the data

    data=[]
    for file_path in file_list:
        fdata,raw_data,names=parse_data(file_path)
        data.append(fdata)
    
    #now sort the data from min to max value of the data you want
    #if temperature, then col 18 is the sorting parameter
 
    minim_data=np.zeros((len(data),1))
    for i in range(len(data)):
        minim_data[i]=getattr(data[i],sort_par)[0]
    ordered_data=np.sort(minim_data,0)
    positions=np.zeros_like(ordered_data,dtype='int')
    'Puts all the files in the right order'
    full_order=[]
    files_order=[]
    for i in range((len(data))):
        for j in range((len(data))):
            if getattr(data[j],sort_par)[0]==ordered_data[i]:
                positions [i]=j
                full_order.append(data[positions[i,0]])
                files_order.append(file_list[positions[i,0]])

    return full_order,files_order


def plot_linescans_raw(dataset,x_axis='',y_axis='',directory=directory):
    file =directory+dataset
    fdata,data,names=parse_data(file)
    title='' 
    split_title=dataset.split('/')[-1].split('_')
    for i in range(len(split_title)-1):
        title=title+' '+split_title[i]
    plt.figure(figsize=(6,4))
    plt.plot(getattr(fdata, x_axis),getattr(fdata, y_axis),'b')
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.grid() 
    plt.ticklabel_format(axis='both', style='sci', scilimits=(-3,3))
    plt.tight_layout()
    plt.show()
    return fdata

def map_transform(dataset):
    
    file=directory+dataset
    fdata,raw2d,variables=parse_data(file)
    '''Make the data in the shape of arrays for 2d maps'''
    data = np.zeros((len(raw2d[0]),len(raw2d[:,0])))
    for j in range(len(raw2d[0])):
        data[j]=raw2d[:,j]
    '''Breakpoint is the sweep size inside the megasweep
        We will use it to cut the 1D array to convert it 
        into a 2D array for the map'''
    breakpoint=[]
    value=0
    for i in range(len(data[0])):
        '''This checks when the slow variable of the megasweep changes
            meaning we are in the next sweep. The positions of the 
            cutpoints will be stored in breakpoint'''
        value=value+1
        try:
            a=data[0,value]-data[0,value-1]
        except(IndexError):
            a=1
        if a != 0.0:
            breakpoint.append(value)
    '''Create an object to store the data for later use
    In the last line the setattr will fill the object with the 
    values for the different attributes'''
    final_data=Object()
    for i in range(len(data)):    
        '''Image shape is an array with the 2D correct size
        We fill it with the data with the cuts given by breakpoint'''
        image_shape=np.zeros((len(breakpoint),(breakpoint[0])))     
        image_shape[0]=data[i,0:breakpoint[0]]
        for j in range(len(image_shape)-1):
            ''''Some datasets are broken because the scan is externally
            finished before it should leaving the last set of data with 
            a differrent sweep value (i.e. the sweep is not fully finnished. 
            The next few lines aim to correct for this'''
            if j!=0:
                sweep_size=breakpoint[j+1]-breakpoint[j]
                #print(sweep_size)
                '''Break the loop if the size of the last sweep does 
                not correspond to the size of all the other sweeps,
                meaning that it is broken. Then it removes the zeros
                of image_shape corresponding to the last sweep, 
                otherwise we will have an array of zeros as the last
                set of data'''
                if sweep_size!=breakpoint[j]-breakpoint[j-1]:
                    image_shape=image_shape[:j+1]
                    break 
            image_shape[j+1]=data[i,breakpoint[j]:breakpoint[j+1]]
        setattr(final_data,variables[i],image_shape)
    return final_data,variables

def plot_map_raw(dataset,plot_data='sr1x',x_axis='',y_axis='',font=12,
                 colormap='RdBu',directory=directory):
    file =directory+dataset
    fdata,variables=map_transform(file)

    plt.figure(figsize=(10,7))
    if x_axis=='':
        plt.imshow(getattr(fdata,plot_data),colormap,aspect='auto')
    else:
        extent=[getattr(fdata,x_axis)[0,0],getattr(fdata,x_axis)[0,-1],
                getattr(fdata,y_axis)[-1,0],getattr(fdata,y_axis)[0,0]]
        plt.imshow(getattr(fdata,plot_data),colormap,extent=extent,aspect='auto')
    plt.xlabel(x_axis,fontsize=font)
    plt.ylabel(y_axis,fontsize=font)    
    plt.tick_params(axis='both',which='major',labelsize=font)
    cb=plt.colorbar()
    cb.set_label(plot_data,fontsize=font)
    cb.ax.tick_params(labelsize=font)
    plt.title(dataset,fontsize=font)
    plt.show()
    return fdata

'''PLOTTING WITH RIGHT PARAMETERS'''


'''Final code for the plotting'''    
def plot_linescans(dataset,x_axis,y_axis,name='',hd=False,save=False):
    data,raw,names=parse_data(dataset)
    plot_x=getattr(data,x_axis)*getattr(mult,x_axis)
    plot_y=getattr(data,y_axis)*getattr(mult,y_axis)
    
    plt.figure(figsize=(6,4))
    plt.plot(plot_x,plot_y,'b')
    plt.xlabel(getattr(lab,x_axis),fontsize=12)
    plt.ylabel(getattr(lab,y_axis),fontsize=12)
    if name=='':
        plt.title(dataset+' '+x_axis+' vs '+y_axis)
    else:
        plt.title(name)
    plt.grid()
    if save:
        if hd:
            plt.savefig(dataset+'_'+x_axis+'_vs_'+y_axis+time.strftime("%H%M%d%m%y")+'.pdf')   
        else:
            plt.savefig(dataset+'_'+x_axis+'_vs_'+y_axis+time.strftime("%H%M%d%m%y")+'.png',dpi=300)    
    plt.show()
    return data


def plot_maps(dataset,z_axis,x_axis,y_axis,name='',hd=False,save=False):
    
    data=map_transform(dataset)   
    plot_data=getattr(data,z_axis)*getattr(mult,z_axis)
    plot_x=getattr(data,x_axis)*getattr(mult,x_axis)
    plot_y=getattr(data,y_axis)*getattr(mult,y_axis)
    
    extent=[plot_x[0,0],plot_x[0,-1],
                plot_y[-1,0],plot_y[0,0]]
    
    plt.figure(figsize=(10,7))
    plt.imshow(plot_data,cmap=cmap,extent=extent,aspect='auto')
    #plt.imshow(plot_data,cmap=cmap,aspect='auto')

    plt.xlabel(getattr(lab,x_axis),fontsize=font)
    plt.ylabel(getattr(lab,y_axis),fontsize=font)
    if name=='':
        plt.title(dataset+' '+x_axis+' vs '+y_axis,fontsize=font)
    else:
        plt.title(name,fontsize=font)
        
    plt.tick_params(axis='both',which='major',labelsize=font)
    cb=plt.colorbar()
    cb.set_label(getattr(lab,z_axis),fontsize=font)
    cb.ax.tick_params(labelsize=font)
    if save:
        if hd:
            plt.savefig(dataset+'_'+x_axis+'_vs_'+y_axis+time.strftime("%H%M%d%m%y")+'.pdf')   
        else:
            plt.savefig(dataset+'_'+x_axis+'_vs_'+y_axis+time.strftime("%H%M%d%m%y")+'.png',dpi=300)    
    plt.show()
    return data

#%%
# Test code:
#plot_linescans('A_IV_15021033.dn', 'KeithRdcv', 'sr1x')
#mult_1D.sr1x
#plot_map_raw('mBTri2_dvdiB.up','sr1x','KeithRdcv','KeithHdci')