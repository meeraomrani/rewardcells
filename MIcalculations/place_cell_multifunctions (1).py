#!/usr/bin/env python
# coding: utf-8

# In[18]:



import matlab.engine
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import os
from scipy import stats


eng = matlab.engine.start_matlab()
eng.addpath(r'C:\Users\fgobbo\Meera Thesis\CDMentropy\src',nargout=0)
eng.addpath(r'C:\Users\fgobbo\Meera Thesis\CDMentropy\lib\PYMentropy\src',nargout=0)
eng.addpath(r'C:\Users\fgobbo\Meera Thesis\CDMentropy', nargout=0)




#calculated entropy of one individual cell via events - formats correctly for CDM entropy estimation
#input: cell_event_individ - one column of events 
#CHECK EVENTS THRESHOLD
def event_entropy(bina_events):

    event_input=[]
    for j in bina_events:
        single_event=[]
        single_event.append(int(float(j)))
        event_input.append(single_event)                    
        
    event_words=matlab.double(event_input)
        
    HE=eng.computeH_CDM(event_words)

    return HE
    




def spatial_occupancy(x, y):
    
    x_bins=np.linspace(4.8, 94.8, 9, endpoint=False)
    x_bins = np.insert(x_bins, 0, -5.2, axis=0)
    x_bins = np.insert(x_bins, 10, 94.8, axis=0)
    x_bins = np.insert(x_bins, 11, 104.8, axis=0)
    y_bins=np.linspace(3.6, 93.6, 9, endpoint=False)
    y_bins = np.insert(y_bins, 0, -6.4, axis=0)
    y_bins = np.insert(y_bins, 10, 93.6, axis=0)
    y_bins = np.insert(y_bins, 11, 103.6, axis=0)
    y_bins = np.insert(y_bins, 12, 113.6, axis=0)
    y_bins = np.insert(y_bins, 13, 123.6, axis=0)

    #formatting
    newx=[]
    newy=[]
    for i in x:
        newx.append(int(float(i)))
    for j in y:
        newy.append(int(float(j)))

    #binning
    occupancy_map_x=[]
    occupancy_map_y=[]
    for x_c, y_c in zip(newx,newy):
        for val in range(len(y_bins)):
            if val<=len(y_bins)-1:
                if y_bins[val]<=y_c<=y_bins[val+1]:
                    for valx in range(len(x_bins)):
                        if x_bins[valx]<=x_c<=x_bins[valx+1]:
                            occupancy_map_x.append(valx)
                            occupancy_map_y.append(val)

    occupied=list(zip(occupancy_map_x, occupancy_map_y))
    return occupied





#spatial entropy
#(x,y):=path of animal in the given stage, session

def spatial_entropy(occupied):
    #spatial_bins#
    x_bins=np.linspace(4.8, 94.8, 9, endpoint=False)
    x_bins = np.insert(x_bins, 0, -5.2, axis=0)
    x_bins = np.insert(x_bins, 10, 94.8, axis=0)
    x_bins = np.insert(x_bins, 11, 104.8, axis=0)
    y_bins=np.linspace(3.6, 93.6, 9, endpoint=False)
    y_bins = np.insert(y_bins, 0, -6.4, axis=0)
    y_bins = np.insert(y_bins, 10, 93.6, axis=0)
    y_bins = np.insert(y_bins, 11, 103.6, axis=0)
    y_bins = np.insert(y_bins, 12, 113.6, axis=0)
    y_bins = np.insert(y_bins, 13, 123.6, axis=0)

    #converting to word format (each entry represents a spatial bin - 1 represents the occupied bin)
    all_y_bins=list(range(len(y_bins)))
    all_x_bins=list(range(len(x_bins)))
    bin_locs=[(x,y) for x in all_x_bins for y in all_y_bins]
    i=0
    input_format=[]
    while i < len(occupied):
        individ_time=[]
        j=0
        while j < len(bin_locs):
            if occupied[i] == bin_locs[j]:
                individ_time.append(1)
                j+=1
            else:
                individ_time.append(0)
                j+=1
        input_format.append(individ_time)
        i+=1
    
    #CDM estimation

    spatial_words=matlab.double(input_format)
    HL=eng.computeH_CDM(spatial_words)
    
    return HL 





#spatial/event joint entropy#
#spatial event joint entropy
#binning events into spatial bins
#99999 is a dummy value - subbed for positions where total zero spike word is 
def spatial_event_joint_entropy(bina_events, occupied):
    #spatial_bins#
    x_bins=  np.linspace(4.8, 94.8, 9, endpoint=False)
    x_bins= np.insert(x_bins, 0, -5.2, axis=0)
    x_bins = np.insert(x_bins, 10, 94.8, axis=0)
    x_bins = np.insert(x_bins, 11, 104.8, axis=0)
    y_bins=  np.linspace(3.6, 93.6, 9, endpoint=False)
    y_bins = np.insert(y_bins, 0, -6.4, axis=0)
    y_bins = np.insert(y_bins, 10, 93.6, axis=0)
    y_bins = np.insert(y_bins, 11, 103.6, axis=0)
    y_bins = np.insert(y_bins, 12, 113.6, axis=0)
    y_bins = np.insert(y_bins, 13, 123.6, axis=0)

    #converting to word format
    all_y_bins=list(range(len(y_bins)))
    all_x_bins=list(range(len(x_bins)))
    bin_locss=[(x,y) for x in all_x_bins for y in all_y_bins]
    
    event_pos_bins=[]
    k=0
    while k<len(bina_events):
        if bina_events[k]>0:
            event_pos_bins.append(occupied[k])
            k+=1
        else:
            event_pos_bins.append(99999)
            k+=1
    
    p=0
    input_format=[]
    zero_events=[0]*168
    while p < len(event_pos_bins):
        if event_pos_bins[p] == 99999:
            input_format.append(zero_events)
            p+=1
        else:
            single_word=[]
            j=0
            while j < len(bin_locss):
                if event_pos_bins[p] == bin_locss[j]:
                    single_word.append(1)
                    j+=1
                else:
                    single_word.append(0)
                    j+=1
            input_format.append(single_word)
            p+=1
        
    spatial_events_words=matlab.double(input_format)
    HEL=eng.computeH_CDM(spatial_events_words)
    
    return HEL
    
## mutual information function ## 
def mutual_information(cell_event, occupied, spatial_ent):
    cell_ent=event_entropy(cell_event)
    JE=spatial_event_joint_entropy(cell_event, occupied)
    mi=cell_ent+spatial_ent-JE
    return mi

def percentile(mi_shuffled_dist, mutual_information):
    perc = []
    for i in mutual_information:
        perc.append(stats.percentileofscore(mi_shuffled_dist, i))
    return perc