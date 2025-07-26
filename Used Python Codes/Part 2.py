import os
import json
import requests

with open("dict.en.json", "r", encoding="utf-8") as dict_file:
    localization_dict = json.load(dict_file)

txt_files = [
    f for f in os.listdir()
    if f.endswith(".txt") and f not in ("errors.txt", "dict.en.json")
]

with open("errors.txt", "w", encoding="utf-8") as error_log:
    pass

def indent_metadata(text):
    result = []
    indent = 0
    for line in text.splitlines():
        stripped = line.strip()

        if stripped == "}" and indent > 0:
            indent -= 1

        result.append("    " * indent + stripped)

        if stripped.endswith("{") and stripped != "{":
            indent += 1
        elif stripped == "{":
            indent += 1

    return "\n".join(result)

for txt_file in txt_files:
    folder_name = os.path.splitext(txt_file)[0]
    os.makedirs(folder_name, exist_ok=True)

    with open(txt_file, "r", encoding="utf-8") as f:
        entries = [line.strip()[1:] for line in f if line.strip().startswith(">")]

    for entry in entries:
        url = f"http://localhost:6155/get_effective_metadata?{entry}"
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            content = res.text.strip()
        except Exception:
            with open("errors.txt", "a", encoding="utf-8") as error_log:
                error_log.write(entry + "\n")
            continue

        skip_check = content.lower()
        if "no such patch" in skip_check or "patch not applied" in skip_check:
            with open("errors.txt", "a", encoding="utf-8") as error_log:
                error_log.write(entry + "\n")
            continue

        formatted = indent_metadata(content)
        output_text = entry + "\n" + formatted

        filename = entry.replace("/", "_").strip("_") + ".txt"

        for line in content.splitlines():
            if line.startswith("LocalizeTag="):
                tag = line.split("=", 1)[1].strip()
                if tag in localization_dict:
                    readable = localization_dict[tag]
                    safe_name = "".join(c for c in readable if c not in r'\/:*?"<>|')
                    filename = safe_name + ".txt"
                break

        try:
            with open(os.path.join(folder_name, filename), "w", encoding="utf-8") as out_file:
                out_file.write(output_text)
        except Exception:
            with open("errors.txt", "a", encoding="utf-8") as error_log:
                error_log.write(entry + "\n")

print("Done.")
