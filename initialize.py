# initialize_data.py
import pandas as pd

# Initial sample data with time in hours and minutes
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'Hours': [1, 2, 1, 3, 1],
    'Minutes': [30, 15, 45, 0, 20]
}

df = pd.DataFrame(data)

# Convert time to total minutes
df['Total_Minutes'] = df['Hours'] * 60 + df['Minutes']
df = df.sort_values(by='Total_Minutes').reset_index(drop=True)

# Save the initial data to a CSV file
df.to_csv('leaderboard.csv', index=False)
