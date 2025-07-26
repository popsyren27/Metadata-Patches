import json

input_file = 'E:/Metadata Project/Other shit which is fucking annoying/ExportWarframes.json'
warframe_output = 'E:/Metadata Project/Other shit which is fucking annoying/ExportWarframes.txt'
skills_output = 'E:/Metadata Project/Other shit which is fucking annoying/ExportSkills.txt'

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(warframe_output, 'w', encoding='utf-8') as wf, open(skills_output, 'w', encoding='utf-8') as sf:
    for top_key, info in data.items():
        wf.write(f">{top_key}\n")

        abilities = info.get('abilities', [])
        for ab in abilities:
            unique = ab.get('uniqueName')
            if unique:
                sf.write(f">{unique}\n")

print("Done. Files written.")
