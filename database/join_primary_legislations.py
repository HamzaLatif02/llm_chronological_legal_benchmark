import json

# Define file paths
ukpga_file_path = '/Users/apple/Desktop/uni/kings/project/database/all_ukpga_legislation.json'
legislations_file_path = '/Users/apple/Desktop/uni/kings/project/database/all_uk_primary_legislation.json'
output_path = '/Users/apple/Desktop/uni/kings/project/database/uk_primary_legislation.json'

# Load ukpga legislations file
with open(ukpga_file_path, 'r', encoding='utf-8') as f:
    data_ukpga = json.load(f)

# Ensure each item in 'data_ukpga' has 'type' = 'ukpga'
for item in data_ukpga:
   item['type'] = 'ukpga'

# Load all legislatiions file
with open(legislations_file_path, 'r', encoding='utf-8') as f:
    data_leg = json.load(f)

# If 'data_leg' is a dict, convert to list
if isinstance(data_leg, dict):
    data_leg = [data_leg]

# Merge both lists
merged_data = data_leg + data_ukpga

# Save in a new file
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, indent=4, ensure_ascii=False)

print(f"Merged {len(merged_data)} acts in total and saved to '{output_path}'.")