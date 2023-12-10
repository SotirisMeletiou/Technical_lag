import matplotlib.pyplot as plt

# Read data from the file
with open('max_lag.txt', 'r') as file:
    lines = file.readlines()

# Parse data into lists
version_numbers = []
technical_lag = []

for line in lines:
    parts = line.strip().split(',')
    version_numbers.append(parts[0])
    technical_lag.append(int(parts[2]))

# Create a line graph
plt.figure(figsize=(10, 6))
plt.plot(version_numbers, technical_lag, marker='o', linestyle='-')
plt.title('Technical Lag Over Versions')
plt.xlabel('Version Number')
plt.ylabel('Technical Lag (days)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the graph
plt.show()
