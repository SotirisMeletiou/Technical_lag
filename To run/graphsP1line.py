import pandas as pd
import matplotlib.pyplot as plt
from packaging import version as packaging_version

# Step 1: Read the TXT file (assuming it's tab-delimited with a header row)
data = pd.read_table('evolve.txt', delimiter=' ')

# Step 2: Sort the data by version
data['version'] = data['version'].apply(packaging_version.parse)
data = data.sort_values('version')
data['version'] = data['version'].astype(str)

# Step 3: Create a table to display the data
table = data.groupby('version')[['num_of_files', 'loc']].sum()

# Step 4: Create and display the table
print(table)

# Step 5: Create line graphs
# Graph 1: Number of files vs. Versions (Line Chart)
plt.figure(figsize=(10, 6))
plt.plot(data['version'], data['num_of_files'], marker='o', linestyle='-')
plt.xlabel('Versions')
plt.ylabel('Number of Files')
plt.title('Number of Files vs. Versions')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Graph 2: LOC vs. Versions (Line Chart)
plt.figure(figsize=(10, 6))
plt.plot(data['version'], data['loc'], marker='o', linestyle='-')
plt.xlabel('Versions')
plt.ylabel('Lines of Code (LOC)')
plt.title('LOC vs. Versions')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
