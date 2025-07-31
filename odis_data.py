import pandas as pd
import json
import zipfile
import os

# Step 1: Extract the ZIP file
odis_files=r'F:\Cricksheet_project\odis_cric.zip'
extract_odis_path='F:\Cricksheet_project\extract_odis_files'
with zipfile.ZipFile(odis_files, 'r') as zip_ref:
    zip_ref.extractall(extract_odis_path)

# Step 2: Process JSON files into a DataFrame
all_deliveries = []
for filename in os.listdir(extract_odis_path):
    if filename.endswith(".json"):
        with open(os.path.join(extract_odis_path, filename), 'r') as f:
            data = json.load(f)
        match_id = filename.replace('.json', '')

        for inning in data.get("innings", []):
            team = inning.get("team", None)
            for over_data in inning.get("overs", []):
                over_number = over_data.get("over", None)
                for delivery in over_data.get("deliveries", []):
                    delivery_info = {
                        "match_id": match_id,
                        "team": team,
                        "over": over_number,
                        "batter": delivery.get("batter"),
                        "bowler": delivery.get("bowler"),
                        "non_striker": delivery.get("non_striker"),
                        "runs_batter": delivery.get("runs", {}).get("batter", 0),
                        "runs_extras": delivery.get("runs", {}).get("extras", 0),
                        "runs_total": delivery.get("runs", {}).get("total", 0),
                        "extra_wides": delivery.get("extras", {}).get("wides", 0),
                        "extra_legbyes": delivery.get("extras", {}).get("legbyes", 0),
                        "extra_byes": delivery.get("extras", {}).get("byes", 0),
                        "extra_noballs": delivery.get("extras", {}).get("noballs", 0),
                        "extra_penalty": delivery.get("extras", {}).get("penalty", 0),
                        "wicket_kind": delivery.get('wickets', [{}])[0].get('kind') if 'wickets' in delivery else 'N_A',
                        'player_out': delivery.get('wickets', [{}])[0].get('player_out') if 'wickets' in delivery else 'N_A',
                        "fielders": delivery.get('wickets', [{}])[0].get('fielders') if 'wickets' in delivery else 'N_A'
                    }

                   
                    all_deliveries.append(delivery_info)

# Step 3: Convert to DataFrame
df_deliveries = pd.DataFrame(all_deliveries)
print(df_deliveries.head())

# Step 4: Save to CSV
df_deliveries.to_csv("odis.csv", index=False)
