import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill

file_path = 'drug_data.xlsx'

# Read the Excel file
data_frame = pd.read_excel(file_path)

# Iterate through rows
# for index, row in df.iterrows():
#     print(row)

# Or if you want to access specific columns
for index, row in data_frame.iterrows():
    name = row['Unnamed: 0']
    phenotype = row['Unnamed: 2']
    genotypes = row["Unnamed: 4"]
    # if(not pd.isnull(row['Unnamed: 0'])):
    print(genotypes.split(','))
# Or iterate through specific columns only
# for index, row in df[['Column1', 'Column2']].iterrows():
#     print(row['Column1'], row['Column2'])