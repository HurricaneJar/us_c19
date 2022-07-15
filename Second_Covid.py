#       #
# Setup #
#       #

from csv import reader
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
data_2021_by_state = data_cropped.loc[(data_cropped['Group'] == 'By Year' ) &
                                      (data_cropped['Year'] == 2021 )]

#null values are represented as '', so I replace any instances of '' with 0.
fix_me = data_2021_by_state['COVID-19 Deaths'] 
for f in range(0, len(fix_me)):
    if fix_me.iloc[f] == '':
        fix_me.iloc[f] = 0
    elif pd.isna(fix_me.iloc[f]) == True:
        fix_me.iloc[f] = 0
data_2021_by_state['COVID-19 Deaths'] = fix_me

#        #
# Rename #
#        #
working_columns = ['group','year','state','condition','age','deaths']
data_2021_by_state.columns = working_columns

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

all_ages = data_2021_by_state[data_2021_by_state['age'] == 'All Ages'].copy()
filtered_all_ages = all_ages[['deaths','state']]
grouped_states = filtered_all_ages.groupby(['state'])['deaths'].sum().reset_index()
sorted_states_table = grouped_states.sort_values(by = 'deaths', ascending = False)
sorted_states = sorted_states_table['state']
 
#      #
# Plot #
#      #

columns = 9
rows = 6

fig, ax = plt.subplots(nrows = rows, ncols = columns, figsize = (14,8))

state_index = 0
for rs in range (0,rows):
    for cs in range (0,columns):
        print(sorted_states.iloc[state_index])
        state_data = data_2021_by_state.loc[(data_2021_by_state['state'] == sorted_states.iloc[state_index]) &
                                            (data_2021_by_state['age'] != 'All Ages')]

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
        ax[rs,cs].tick_params(axis = 'x', labelsize = 3, rotation = 90)
        ax[rs,cs].tick_params(axis = 'y', labelsize = 6)
        ax[rs,cs].set_title(sorted_states.iloc[state_index], fontsize = 6)
        
        if sorted_states.iloc[state_index] == 'United States':
            ax[rs,cs].set_ylim([0,500000])
            ax[rs,cs].set_yticks([500000])
            ax[rs,cs].set_yticklabels(['500000'])
            ax[rs,cs].legend(['0-24','25-34','35-44','45-54','55-64','65-74','75-84','85+','Unspecified'])
            ax[rs,cs].set_title('Death Count of Covid-related Conditions, Provincially (CDC)')

        elif sorted_states.iloc[state_index] == 'California':    # Standardized Ylimits
            ax[rs,cs].set_ylim([0,40000])
            ax[rs,cs].set_yticks([40000])
            ax[rs,cs].set_yticklabels(['40k'])       

        else:
#            lim = bar_base.max()                                 # Custom Ylimits
#            ylabel_long = str(lim)
#            ylabel_short = ylabel_long[0:-2]
#            ax[rs,cs].set_ylim([0,(lim+(.1*lim))])
#            ax[rs,cs].set_yticks([lim])
#            ax[rs,cs].set_yticklabels([ylabel_short])

            ax[rs,cs].set_ylim([0,40000])                      # Standardized Ylimits
            ax[rs,cs].set_yticks([])
            ax[rs,cs].set_yticklabels([])       
     
        state_index += 1 

plt.tight_layout()
plt.show()

