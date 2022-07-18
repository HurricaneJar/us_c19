#       #
# Setup #
#       #

from csv import reader
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as plotme

covid =pd.read_csv("/Users/zachpolitz/Desktop/Conditions_Contributing_to_COVID-19_Deaths__by_State_and_Age__Provisional_2020-2021.csv")
headers = covid.columns


#       #
# Clean #
#       #
column_unique_values = {}
for row in headers:
    column_unique_values[row] = covid[row].unique()

null_counts = covid[covid['COVID-19 Deaths']== '']
 
data_cropped = covid[['Group','Year','State','Condition','Age Group','COVID-19 Deaths']]
data_2020_by_state = data_cropped.loc[(data_cropped['Group'] == 'By Year' ) &
                                      (data_cropped['Year'] == 2020 )]

#null values are represented as '', so I replace any instances of '' with 0.
fix_me = data_2020_by_state['COVID-19 Deaths'] 
for f in range(0, len(fix_me)):
    if fix_me.iloc[f] == '':
        fix_me.iloc[f] = 0
    elif pd.isna(fix_me.iloc[f]) == True:
        fix_me.iloc[f] = 0
data_2020_by_state['COVID-19 Deaths'] = fix_me

#        #
# Rename #
#        #
working_columns = ['group','year','state','condition','age','deaths']
data_2020_by_state.columns = working_columns

condition_dict = {'Influenza and pneumonia': 'I&P',
                  'Chronic lower respiratory diseases': 'CLRD',
                  'Adult respiratory distress syndrome':'ARDS',
                  'Respiratory failure':'RspF',
                  'Respiratory arrest':'RA',
                  'Other diseases of the respiratory system':'ODRS',
                  'Hypertensive diseases':'HD',
                  'Ischemic heart disease':'IHD',
                  'Cardiac arrest':'CArst',
                  'Cardiac arrhythmia':'CAthm',
                  'Heart failure':'HF',
                  'Cerebrovascular diseases':'CD',
                  'Other diseases of the circulatory system':'ODCS',
                  'Sepsis':'S',
                  'Malignant neoplasms':'MN',
                  'Diabetes':'D',
                  'Obesity':'O',
                  'Alzheimer disease':'AD',
                  'Vascular and unspecified dementia':'VUD',
                  'Renal failure':'RenF',
                  'Intentional and unintentional injury, poisoning, and other adverse events':'IUIPOAE',
                  'All other conditions and causes (residual)':'AOCC',
                  'COVID-19':'C19'}


#                  #
# Restructure Data #
#                  #

sum_ages = data_2020_by_state[data_2020_by_state['age'] != 'All Ages'].copy()
filtered_sum_ages = sum_ages[['deaths','state']]
grouped_states = filtered_sum_ages.groupby(['state'])['deaths'].sum().reset_index()
sorted_states_table = grouped_states.sort_values(by = 'deaths', ascending = False)
sorted_states = sorted_states_table['state']

#      #
# Plot #
#      #

columns = 9
rows = 6

fig, ax = plt.subplots(nrows = rows, ncols = columns, figsize = (14,8))
fig.suptitle('Conditions_Contributing_to_COVID-19_Deaths__by_State_and_Age__Provisional_2020-2021.csv (Source: CDC, August 2021)')
fig.text(x= .2, y= .94, s= 'Plots show total annual deaths by condition and age group(color-coded) for 2020 (states are in order of total deaths)')


state_index = 0
for rs in range (0,rows):
    for cs in range (0,columns):
        print(sorted_states.iloc[state_index])
        state_data = data_2020_by_state.loc[(data_2020_by_state['state'] == sorted_states.iloc[state_index]) &
                                            (data_2020_by_state['age'] != 'All Ages')]

        filtered_list_to_sort = {'cond':[],'deaths':[]}
        filtered_list_to_sort = pd.DataFrame(filtered_list_to_sort)	

        for element in column_unique_values['Condition']:	
             filtered = state_data[state_data['condition'] == element].copy()	
             x = sum(filtered['deaths'])					
             filtered_list_to_sort = filtered_list_to_sort.append({'cond':element,
                                                                   'deaths':x}, ignore_index = True) 	

        sort_conditions = filtered_list_to_sort.sort_values(by = 'deaths')
        sorted_conditions = sort_conditions['cond'].copy()
        sorted_condition_deaths_by_age = {}
        age_groups = column_unique_values['Age Group'].copy()   
        ag_sans_AA = age_groups[0:-1]
        for age in ag_sans_AA:
            state_age = state_data[state_data['age'] == age].copy()
            age_deaths = pd.Series(dtype = 'Float64')
            for condition in sorted_conditions:
                extracted_row = state_age[state_age['condition'] == condition].copy()
                extracted_value = extracted_row['deaths']
                age_deaths = age_deaths.append(extracted_value)
            sorted_condition_deaths_by_age[age] = age_deaths			

        for b in range (0,len(sorted_conditions)):
            swap = sorted_conditions.iloc[b]
            sorted_conditions.iloc[b] = condition_dict[swap] 
            
        bar_base = pd.Series(0, index = range(23))
        for row in sorted_condition_deaths_by_age:
            xs = sorted_condition_deaths_by_age[row]       
            ax[rs,cs].bar(x = sorted_conditions, height = xs, width = .5, bottom = bar_base, linewidth = 0)
            for t in range (0,len(bar_base)):
                bar_base.iloc[t] += xs.iloc[t]

        ylimits = []
        ylabels = []
        ax[rs,cs].tick_params(axis = 'x', labelsize = 4, rotation = 90)
        ax[rs,cs].tick_params(axis = 'y', labelsize = 6)
        ax[rs,cs].yaxis.tick_right()
        ax[rs,cs].set_title(sorted_states.iloc[state_index], y=.6, fontsize = 7)
        ax[rs,cs].spines['right'].set_visible(False)
        ax[rs,cs].spines['left'].set_visible(False)
        ax[rs,cs].spines['top'].set_visible(False)
        
        if sorted_states.iloc[state_index] == 'United States':
            lim = bar_base.max()
            lim_string = str(lim)
            ax[rs,cs].set_ylim([0,lim])
            ax[rs,cs].set_yticks([lim])
            ax[rs,cs].set_yticklabels([lim_string[0:-2]])


        elif sorted_states.iloc[state_index] == 'California':     # Standardized Ylimits
            lim = bar_base.max()
            lim_string = str(lim)
            ax[rs,cs].set_ylim([0,40000])
            ax[rs,cs].set_yticks([lim])
            ax[rs,cs].set_yticklabels([lim_string[0:-2]])       

        else:
#            lim = bar_base.max()                                 # Custom Ylimits 
#            ylabel_long = str(lim)
#            ylabel_short = ylabel_long[0:-2]
#            ax[rs,cs].set_ylim([0,(lim+(.1*lim))])
#            ax[rs,cs].set_yticks([lim])
#            ax[rs,cs].set_yticklabels([ylabel_short])

            lim = bar_base.max()                                  # Standardized Ylimits
            lim_string = str(lim)
            ax[rs,cs].set_ylim([0,40000])                     
            ax[rs,cs].set_yticks([lim])
            ax[rs,cs].set_yticklabels([lim_string[0:-2]])  
            

        state_index += 1 


plt.tight_layout()
plt.show()

