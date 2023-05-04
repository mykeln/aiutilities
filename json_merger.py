import json

# Read JSON data from the files
with open('climate_file1.js', 'r') as f1:
    data1 = json.load(f1)

with open('climate_file2.js', 'r') as f2:
    data2 = json.load(f2)

# Combine the two JSON files based on the 'id' field
combined_data = {}
for item in data1:
    combined_data[item['id']] = item

for item in data2:
    if item['id'] in combined_data:
        combined_data[item['id']].update(item)

# Convert the combined data back to a list
combined_list = list(combined_data.values())

# Write the combined JSON data to a new file
with open('climate_data.js', 'w') as outfile:
    json.dump(combined_list, outfile, indent=2)
