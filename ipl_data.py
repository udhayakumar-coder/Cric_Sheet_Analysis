import pandas as pd
import json
import zipfile
import os


# Step 1: ZIP file extract
zip_path = "F:\Cricksheet_project\ipl_cric.zip"                # zip file path
extract_dir = "F:\Cricksheet_project\extract_ipl_files"        # extract file path pre-define
os.makedirs(extract_dir, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r',) as zip_ref:
    zip_ref.extractall(extract_dir)

# Step 2: json data file collect using loop based
all_deliveries = []

for file_name in os.listdir(extract_dir):
    if file_name.endswith(".json"):
        file_path = os.path.join(extract_dir, file_name)
        with open(file_path, 'r') as f:
            data = json.load(f)
            file_name = file_name.replace('.json','')  # remove .json extension for file name
            
            for inning in data.get('innings', []):
                team = inning.get('team')
                for over_data in inning.get('overs', []):
                    over = over_data.get('over')
                    for delivery in over_data.get('deliveries', []):
                        delivery_info = {
                            'file': file_name,
                            'team': team,
                            'over': over,
                            'batter': delivery.get('batter'),
                            'bowler': delivery.get('bowler'),
                            'non_striker': delivery.get('non_striker'),
                            'runs_batter': delivery['runs'].get('batter', 0),
                            'runs_extras': delivery['runs'].get('extras', 0),
                            'runs_total': delivery['runs'].get('total', 0),
                            'extra_wides': delivery.get('extras', {}).get('wides', 0),
                            'extra_legbyes': delivery.get('extras', {}).get('legbyes', 0),
                            'extra_byes': delivery.get('extras', {}).get('byes', 0),
                            'extra_noballs': delivery.get('extras', {}).get('noballs', 0),
                            'extra_penalty': delivery.get('extras', {}).get('penalty', 0),
                            'wicket_kind': delivery.get('wickets', [{}])[0].get('kind') if 'wickets' in delivery else 'N_A',
                            'player_out': delivery.get('wickets', [{}])[0].get('player_out') if 'wickets' in delivery else 'N_A',
                            'fielders': delivery.get('wickets', [{}])[0].get('fielders') if 'wickets' in delivery else 'N_A'
                        }
                        all_deliveries.append(delivery_info)

# create DataFrame 
df_detailed = pd.DataFrame(all_deliveries)

# save csv file
df_detailed.to_csv("ipl.csv", index=False)

# print
print(df_detailed)
