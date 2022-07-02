
# -*- coding: utf-8 -*-

# Created on Tue Mar 22 07:59:46 2022
# @author: zachpolitz
 
'''
Counts for ICD10 codes and Age Group counts yield:    
   Ages:
'0-24': 28566,
'25-34': 28566,
'35-44': 28566,
'45-54': 28566,
'55-64': 28566,
'65-74': 28566,
'75-84': 28566,
'85+': 28566,
'Not stated': 28566,
'All Ages': 28566 

Conditions:
 'Influenza and pneumonia': I,
 'Chronic lower respiratory diseases':II,
 'Adult respiratory distress syndrome': III,
 'Respiratory failure': IV,
 'Respiratory arrest': V,
 'Other diseases of the respiratory system': VI,
 'Hypertensive diseases': VII,
 'Ischemic heart disease': VIII,
 'Cardiac arrest': IX,
 'Cardiac arrhythmia': X,
 'Heart failure': XI,
 'Cerebrovascular diseases': XII,
 'Other diseases of the circulatory system': XIII,
 'Sepsis': XIV,
 'Malignant neoplasms': XV,
 'Diabetes': XVI,
 'Obesity': XVII,
 'Alzheimer disease': XVIII,
 'Vascular and unspecified dementia': XIX,
 'Renal failure': 12420,
 'Intentional and unintentional injury, poisoning, and other adverse events': 12420,
 'All other conditions and causes (residual)': 12420,
 'COVID-19': 12420

     Columns:
'Data As Of', 'Start Date', 'End Date', 'Group',
'Year', 'Month', 'State', 'Condition Group',
'Condition', 'ICD10_codes', 'Age Group', 'COVID-19 Deaths',
'Number of Mentions', 'Flag'
'''

### SETUP ###

import seaborn as sns
import numpy as np
from csv import reader
import matplotlib.pyplot as plt
import pandas as pd

file_path = "/Users/zachpolitz/Desktop/Conditions_Contributing_to_COVID-19_Deaths__by_State_and_Age__Provisional_2020-2021.csv"
opened_file = open(file_path)
read_file = reader(opened_file)

COVID_RAW = list(read_file)
Covid = pd.DataFrame(COVID_RAW[1:])
headers = COVID_RAW[0]
Covid.columns = headers


### Misc. Exploratory variables
all_ages = Covid.loc[(Covid['Age Group'] == 'All Ages') &
                 (Covid['Year'] == '2020') &
                 (Covid['Group'] == 'By Year') &
                 (Covid['Flag'] == '')]
all_death = all_ages['COVID-19 Deaths']
for row in all_death:
    if row == '':
        row = 0
all_death = sum(all_death.astype(int)) 
        
sum_ages = Covid.loc[(Covid['Age Group'] != 'All Ages') &
                 (Covid['Year'] == '2020') &
                 (Covid['Group'] == 'By Year') &
                 (Covid['Flag'] == '')]
sum_death = sum_ages['COVID-19 Deaths'].astype(int)
for row in sum_death:
    if row == '':
        row = 0
sum_death = sum(sum_death.astype(int))


### generate column uniques

col_uniques = {}
col_uniques['ages'] = Covid['Age Group'].unique()
col_uniques['states'] = Covid['State'].unique()
col_uniques['conditions'] = Covid['Condition'].unique()
col_uniques['icd_10'] = Covid['ICD10_codes'].unique()
col_uniques['data_as_of'] = Covid['Data As Of'].unique()
col_uniques['start_date'] = Covid['Start Date'].unique()
col_uniques['end_date'] = Covid['End Date'].unique()
col_uniques['group'] = Covid['Group'].unique()
col_uniques['year'] = Covid['Year'].unique()
col_uniques['month'] = Covid['Month'].unique()

### null values are input as ''
blanks =  Covid[Covid['COVID-19 Deaths'] == '']
nulls = Covid[Covid['COVID-19 Deaths'].isnull()]


### shrink condition names ###
aliases = ['IP','CLRD','ARDS','RF','RA','ODRS','HD','IHD','CA1','CA2',
           'HF','CD','ODCS','S','MN','D','O','AD','VUD',
           'RF','IUI','AOCC','C19']
cndtn_alias = {}
names = col_uniques['conditions']
for i in range (0,len(names)):
    j = names[i]
    cndtn_alias[j] = aliases[i]

### sort states by volume ###


state_list = []
for row_state in col_uniques['states']:
    state_to_sort = Covid.loc[(Covid['State'] == row_state) &
                              (Covid['Age Group'] == 'All Ages') &
                              (Covid['Year'] == '2020') &  
                              (Covid['Group'] == 'By Year') &
                              (Covid['Flag'] == '')]
    death_int = state_to_sort['COVID-19 Deaths'].copy().astype(int)
    sum_death = sum(death_int)
    state_list.append([row_state,sum_death])
state_list = pd.DataFrame(state_list)
state_list = state_list.sort_values(by = 1, ascending = False)

### PLOT LOOP ###

cols=9
rows= 6
ordered_states = state_list[0]

fig, ax = plt.subplots(nrows=rows, ncols=cols, figsize = (14,8))

i = 0
for k in range(0,rows):
    for j in range (0,cols):     
        state = Covid.loc[(Covid['State'] == ordered_states.iloc[i]) &  
                          (Covid['Year'] == '2020') &
                          (Covid['Group'] == 'By Year')]       

        print(state['State'].unique()) 


      # Fill in C-19 deaths '' with '0'
      # Convert values to int       
      # Sort rows by C-19 deaths
        for row in range (0,len(state['COVID-19 Deaths'])):
            if state['COVID-19 Deaths'].iloc[row] == '':
                state['COVID-19 Deaths'].iloc[row] = '0'
        state['COVID-19 Deaths'] = state['COVID-19 Deaths'].astype(int) 
        state = state.sort_values(by = 'COVID-19 Deaths')
    
        pd.options.display.expand_frame_repr = False 
        bababa = state[['Condition','COVID-19 Deaths']]
        print(bababa.groupby(['Condition']).sum())
         #  pd.options.display.expand_frame_repr = True


      # Generate dictionary of age group death vectors 
      # Remove 'All Ages' from dictionary
      # Add age group to dictionary
        graph_me = {}
        age_sans_AA = col_uniques['ages']
        age_sans_AA = age_sans_AA[0:-1]
        for age in age_sans_AA: 
            age_bar = state[state['Age Group'] == age]
            age_bar = age_bar['COVID-19 Deaths'] 
            graph_me[age] = age_bar
        

      # rename conditions for bar labels:
      # copy condition column
      # apply aliases
      # filter series down to uniques

        x = state['Condition'].copy()
        x = x.unique()
        for a in range(0,len(x)): 
            var = x[a]
            x[a] = cndtn_alias[var] 

      # plot stacked bars by age group
      # for each group, plot the bottom of the bar at the sum of the previous bars
        w = .5
        g = 0
        old_vals = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for row in age_sans_AA:
            vals = graph_me[row].astype(int)
            vals = list(vals)
            ax[k,j].bar(x, vals, width = w, bottom = old_vals)
            for t in range (0, len(old_vals)):
                old_vals[t] += vals[t]


      # plot params
      # graph limits decrement by row going down      
      # graph limit labeled at leftmost graph of each row
      # removes superfluous tickmarks
      # sets graph title to state
      # x axis labeled by description aliases

        ylimits = [50000,40000,30000,20000,10000,5000]
        ylabels = ['40k','30k','20k','10k','5k']
        ax[k,j].tick_params(axis ='x', labelsize = 3,labelrotation = 90, bottom = False)
        ax[k,j].tick_params(axis ='y', labelsize = 6)
        ax[k,j].set_title(ordered_states.iloc[i], fontsize=6)
        if ordered_states.iloc[i] == 'United States':
            ax[k,j].set_ylim([0,500000])
            ax[k,j].set_yticks([500000])
            ax[k,j].set_yticklabels(['1M'])
        elif ordered_states.iloc[i] == 'California':
            ax[k,j].set_ylim([0,50000])
            ax[k,j].set_yticks([50000]) 
            ax[k,j].set_yticklabels(['50k'])
        else:
            ax[k,j].set_ylim([0,ylimits[k]])
            ax[k,j].set_yticks([ylimits[k]]) 
            if j == 0:
                ax[k,j].set_yticklabels([ylabels[k-1]])
            else:
                ax[k,j].set_yticklabels([])
        
        i+=1

plt.tight_layout()
plt.show()



### The Conditions do not present in 
### order of death volume. 
# THE BARS ARE NOT ALWAYS RANKED IN ORDER
# THE CONDITIONS DO NOT MAP TO THE BAR VALUES


# Condition legend

# I am learning the value of having a well-planned architecture (mental map)
# I am learning a lesson about not being able to query the impacts of a code change
# I am learning a lesson about variable names
# I am enjoying the increasing familiarity that I have with the structure I've created
# I am excited to feel competant
# I am excited to feel ready to move on to new, complexifying tools
