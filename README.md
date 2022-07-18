# us_c19
Visualizing US Covid Deaths for 2020 and 2021

The aim of this project is to provide a data-rich perspective on Covid-related deaths, labeled by state, age group, condition, and year.

My design-intention was to display as many dimensions of the raw dataset as possible. I have also attached four graphs that explore 2020's vs 2021's numbers, and the difference between a standardized y-axis and a state-specific y-axis.

The data was pulled from the CDC website, which was uploaded August 1st, 2021.
https://data.cdc.gov/NCHS/Conditions-Contributing-to-COVID-19-Deaths-by-Stat/hk9y-quqm


Age Groups are plotted in order:
Base: 0-24 (Orange)
25-34
35-44
45-54
55-64
65-74
75-84
85+
Top: Not stated (Grey)


X-axis Legend:
'Influenza and pneumonia': 'I&P', 
'Chronic lower respiratory diseases': 'CLRD', 
'Adult respiratory distress syndrome': 'ARDS', 
'Respiratory failure': 'RspF', 
'Respiratory arrest': 'RA', 
'Other diseases of the respiratory system': 'ODRS', 
'Hypertensive diseases': 'HD', 
'Ischemic heart disease': 'IHD', 
'Cardiac arrest': 'CArst', 
'Cardiac arrhythmia': 'CAthm', 
'Heart failure': 'HF', 
'Cerebrovascular diseases': 'CD', 
'Other diseases of the circulatory system': 'ODCS', 
'Sepsis': 'S', 
'Malignant neoplasms': 'MN', 
'Diabetes': 'D', 
'Obesity': 'O', 
'Alzheimer disease': 'AD', 
'Vascular and unspecified dementia': 'VUD', 
'Renal failure': 'RenF', 
'Intentional and unintentional injury, poisoning, and other adverse events': 'IUIPOAE', 
'All other conditions and causes (residual)': 'AOCC', 
'COVID-19': 'C19'


Upon Completion, some notable questions arose:
- Is there greater truth in the graphs with shared y-axis limits versus state-specific y-axis limits?
- How could I make long descriptions easier to understand (ex: "Intentional and unintentional injury, poisoning, and other adverse events" ('IUIPOAE')) without forcing the reader to wade through the legend listed above?
- How would it feel to have the bar colors correspond to their proportion of the deaths within that condition?
- Does a death correspond to only one person, or could one person take up multiple counts on the graph, because their death was labeled with Sepsis, ARDS, and Covid-19?
- How did states differ in their reporting methods?
- Do the conditions' per capita deaths have a different distribution from their totals?
- How many ICU beds did each state have?


Thank you for your time,
Zach Politz
