import pandas as pd
import json
import zipfile
import os
import mysql.connector

# data extract
zip_path = r"F:\Cricksheet_project\tests_cric.zip"  # zip path
extract = r"F:\Cricksheet_project\tests_cric_files" #extract path
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract)
        os.makedirs(extract, exist_ok=True)

# json data read and data create
all_deliveries = []



for file_name in os.listdir(extract):
    if file_name.endswith(".json"):
        file_path = os.path.join(extract, file_name)
        with open(file_path, 'r') as f:
            data = json.load(f)
            file_name = file_name.replace('.json', '')  # remove .json extension for match id
            for inning in data.get('innings', []):
                team = inning.get('team')
                for over_data in inning.get('overs', []):
                    over = over_data.get('over')
                    for delivery in over_data.get('deliveries', []):
                        delivery_info = {
                            'match id': file_name,
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
df_detailed.to_csv("tests.csv", index=False)

# print
print(df_detailed)
