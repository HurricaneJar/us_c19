
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
 'Influenza and pneumonia': 12420,
 'Chronic lower respiratory diseases': 12420,
 'Adult respiratory distress syndrome': 12420,
 'Respiratory failure': 12420,
 'Respiratory arrest': 12420,
 'Other diseases of the respiratory system': 12420,
 'Hypertensive diseases': 12420,
 'Ischemic heart disease': 12420,
 'Cardiac arrest': 12420,
 'Cardiac arrhythmia': 12420,
 'Heart failure': 12420,
 'Cerebrovascular diseases': 12420,
 'Other diseases of the circulatory system': 12420,
 'Sepsis': 12420,
 'Malignant neoplasms': 12420,
 'Diabetes': 12420,
 'Obesity': 12420,
 'Alzheimer disease': 12420,
 'Vascular and unspecified dementia': 12420,
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
aliases = ['I','II','III','IV','V','VI','VII','VIII','IX','X',
           'XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX',
           'XX','XXI','XXII','XXIII','XXIV']
cndtn_alias = {}
names = col_uniques['conditions']
for i in range (0,len(names)):
    j = names[i]
    cndtn_alias[j] = aliases[i]


### sort states by volume ###

ranked_states = {}
state_list = []
for row_state in col_uniques['states']:
    state_to_sort = Covid.loc[(Covid['State'] == row_state) &
                              (Covid['State'] != 'United States') &
                              (Covid['Age Group'] == 'All Ages') &
                              (Covid['Year'] == '2020') &  
                              (Covid['Group'] == 'By Year') &
                              (Covid['Flag'] == '')]
    death_int = state_to_sort['COVID-19 Deaths'].copy().astype(int)
    sum_death = sum(death_int)
    state_list.append([row_state,sum_death])
    ranked_states[row_state] = sum_death

state_list = pd.DataFrame(state_list)
state_list = state_list.sort_values(by = 1, ascending = False)


### PLOT LOOP ###

cols=9
rows= 6
ordered_states = state_list[0]

fig, ax = plt.subplots(nrows=rows, ncols=cols, figsize = (12,10))
i = 0

for k in range(0,rows):
    for j in range (0,cols):     
        age_stack = []
        state = Covid.loc[(Covid['State'] == ordered_states.iloc[i]) &  
                          (Covid['Age Group'] != 'All Ages') &
                          (Covid['Year'] == '2020') &
                          (Covid['Group'] == 'By Year')]        


        h = 10 
        w = 1

        graph_me = {}
        for age in col_uniques['ages']: 
            age_bar = state[state['Age Group'] == age]
            age_bar = age_bar['COVID-19 Deaths']
            g_me = []
            for u in range (0,len(age_bar)):
                if age_bar.iloc[u] == '':
                    g_me.append(0)
                else:
                    g_me.append(age_bar.iloc[u])
            g_me = pd.Series(g_me).astype(int)
            graph_me[age] = g_me


        x = state['Condition'].copy()
        x = [cndtn_alias[row] for row in x]    
        x = pd.Series(x).unique()

        g = 0
        bot = 0

# bottom needs to be a value; i need, for every condition, to add up the previous
# values in order to establish the base of the next bar.

        old_vals = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for row in col_uniques['ages']:
            vals = graph_me[row]
            if g == 0:    
                ax[k,j].bar(x, data = vals, height = h, width = w)
            else: 
                ax[k,j].bar(x, data = vals, height = h, width = w, bottom = old_vals) 
            old_vals += vals
            g += 1

        ax[k,j].set_yticks([]) 
        ax[k,j].tick_params(axis ='x',labelsize = 3,labelrotation = 90)
        ax[k,j].set_title(ordered_states.iloc[i], fontsize=6)
        ax[k,j].set_ylim([0,35000])
        i += 1

plt.tight_layout()
plt.show()
