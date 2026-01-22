import json
import os

root_dir = os.getcwd()  # directory where main.py is located

for root, dirs, files in os.walk(root_dir):
    for filename in files:
        if filename.endswith(".json"):
            json_path = os.path.join(root, filename)

            base_name = os.path.splitext(filename)[0]
            output_name = base_name + ".txt"
            output_path = os.path.join(root, output_name)

            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            with open(output_path, 'w', encoding='utf-8') as out:
                for key in data:
                    out.write(f'>{key}\n')
