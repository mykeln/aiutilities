import json

# Read JSON data from climate_data.js
with open("climate_data.js", "r") as file:
    content = file.read()
    # Strip 'const climateData = ' and the final semicolon to get the JSON string
    json_str = content.strip("const climateData = ").strip(";")

# Parse JSON data
json_data = json.loads(json_str)

def update_sources(data):
    for entry in data:
        sources_text = entry['sources'][0]
        sources = [source.split(",") for source in sources_text.split("\n")]
        entry['sources'] = sources

    return data

# Update sources in JSON data
updated_data = update_sources(json_data)

# Convert updated JSON data back to a string
updated_json_str = json.dumps(updated_data, indent=2)

# Write the updated JSON data back to climate_data.js
with open("climate_data.js", "w") as file:
    file.write(f"const climateData = {updated_json_str};")
