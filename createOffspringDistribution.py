import pandas as pd


# Getting the data

birth_rates = []

data= pd.read_csv("children-born-per-woman.csv")
birth_rates = data[data['Entity'] == 'Iceland']

# Deleting the columns that are not needed
del birth_rates['Code']
del birth_rates['Entity']

print(birth_rates)