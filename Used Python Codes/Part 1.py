import json
import os

for filename in os.listdir():
    if filename.endswith(".json"):
        base_name = os.path.splitext(filename)[0]
        output_name = base_name + ".txt"

        with open(filename, 'r') as f:
            data = json.load(f)

        with open(output_name, 'w') as out:
            for key in data:
                out.write(f'>{key}\n')
