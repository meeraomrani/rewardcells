#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#creating a dictionary for stored data (again can be changed dependent on how many files you are reading in)#

## creating dictionary ##
Animal='H2202'
sessions=['N01', 'N02', 'I01', 'I02', 'A01', 'A02', 'P01', 'P02']
stages=['PRE', 'SAM', 'CHO']
stagesp=['PRE', 'SAM', 'CHO', 'PRO']

xydict={}
for i in sessions:
    xydict[i]={}
z=list(xydict.keys())[:6]
for l in z:
    for j in stages:
        xydict[l][j]={}
p=list(xydict.keys())[6:]
for r in p:
    for i in stagesp:
        xydict[r][i]={}



#### CORRECT PERCENTILE IDENTIFICATION ####


#dictionary of all dataframes - pc_dict['A01_MI'] calls all A01 mutual informtion values, pc_dict['A01_SD']=A01_SD calls all the shuffled values etc

pc_dict={'A01_MI':A01_MI, 'A01_SD':A01_SD, 'A02_MI':A02_MI, 'A02_SD':A02_SD,'P01_MI':P01_MI, 'P01_SD':P01_SD,  'P02_MI':P02_MI, 'P02_SD':P02_SD }

pcsessions=['A01', 'A02', 'P01', 'P02']

for s in pcsessions: 
    #selects MI and SD files for a stage 
    MI_vals=pc_dict[s+'_MI']
    SD_vals=pc_dict[s+'_SD']
    #runs through each cell and finds its percentile against the shuffled values/stores to perc
    i=0
    perc=[]
    while i<len(MI_vals['MI']):
        SD=SD_vals['dist_vals'][i*1000:(i+1)*1000]
        perc.append(stats.percentileofscore(SD, MI_vals['MI'][i]))
        i+=1
    #stores to a dictionary (this can be created dependent on your needs)
    xydict[s]['PRE']['percs']=perc
    #stores each cells id in the original dataframe as opposed to i (reset index following sorting)
    xydict[s]['PRE']['mi_id']=MI_vals['cell_id'].tolist()
    #finds place cells - i.e. finds cells which have a percentile score greater than 95 then finds its respective cell_id
    # and stores to the dictionary 
    pc_ids=[]
    j=0
    while j<len(perc):
        if perc[j]>=95:
            pc_ids.append(MI_vals['cell_id'][j])
            j+=1
        else:
            j+=1
    xydict[s]['PRE']['pc_id']=pc_ids
    

