import pandas as pd
import sys

# Check script was run correctly
if len(sys.argv) != 2:
    print('Error: Script takes 2 arguments: ConvertScores.py <Year>')
    sys.exit()

# Read in csv
data = pd.read_csv('old-scores.csv')
year = sys.argv[1]

# Add year column
data.insert(3, 'Year', year)

# Write to new-scores.csv
data.to_csv('new-scores.csv', index=False)

print('Successfully written to new-scores.csv!')