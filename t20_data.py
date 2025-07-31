import os
import zipfile
import json
import mysql.connector
import pandas as pd

#path to the ZIP file and extraction directory
file_path = r'F:\Cricksheet_project\t20s_cric.zip'
extract_path= r'F:\Cricksheet_project\t20s_cric'
# Step 2: Extract ZIP file
with zipfile.ZipFile(file_path,'r') as zip_ref:
    zip_ref.extractall(extract_path)
    os.makedirs(extract_path, exist_ok=True)

# Step 3: Create an empty list to collect all delivery data
all_data = []

# Step 4: Loop through each JSON file and extract delivery info
for file_name in os.listdir(extract_path):
    if file_name.endswith('.json'):
        file_path = os.path.join(extract_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        file_name = file_name.replace('.json', '')  # Remove .json extension for match id
        for inning in data.get('innings', []):
            team = inning.get('team')
            for over_data in inning.get('overs', []):
                over_number = over_data.get('over')
                for delivery in over_data.get('deliveries', []):
                    delivery_info = {
                        'match id': file_name,
                        'team': team,
                        'over': over_number,
                        'batter': delivery.get('batter'),
                        'bowler': delivery.get('bowler'),
                        'non_striker': delivery.get('non_striker'),
                        'runs_batter': delivery.get('runs', {}).get('batter', 0),
                        'runs_extras': delivery.get('runs', {}).get('extras', 0),
                        'runs_total': delivery.get('runs', {}).get('total', 0),
                        'extra_wides': delivery.get('extras', {}).get('wides', 0),
                        'extra_legbyes': delivery.get('extras', {}).get('legbyes', 0),
                        'extra_byes': delivery.get('extras', {}).get('byes', 0),
                        'extra_noballs': delivery.get('extras', {}).get('noballs', 0),
                        'extra_penalty': delivery.get('extras', {}).get('penalty', 0),
                        'wicket_kind': delivery.get('wickets', [{}])[0].get('kind') if 'wickets' in delivery else 'N_A',
                        'player_out': delivery.get('wickets', [{}])[0].get('player_out') if 'wickets' in delivery else 'N_A',
                        'fielders': delivery.get('wickets', [{}])[0].get('fielders') if 'wickets' in delivery else 'N_A'
                    }

                    # Append the delivery info to the list
                    all_data.append(delivery_info)

# Step 5: Convert to DataFrame
df = pd.DataFrame(all_data)

# Save DataFrame to CSV
df.to_csv('t20.csv', index=False)
# Step 6: Show the first 5 rows
print(df)
