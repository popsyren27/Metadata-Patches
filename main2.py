import os
import json
import requests
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DICT_PATH = os.path.join(SCRIPT_DIR, "dict.en.json")
ERROR_LOG_PATH = os.path.join(SCRIPT_DIR, "errors.txt")
FOLDER_PATH = os.path.join(SCRIPT_DIR, "Weapons")

if not os.path.isfile(DICT_PATH):
    raise FileNotFoundError(f"Dictionary not found: {DICT_PATH}")
if not os.path.isdir(FOLDER_PATH):
    raise FileNotFoundError(f"Folder not found: {FOLDER_PATH}")

with open(ERROR_LOG_PATH, "w", encoding="utf-8"):
    pass

with open(DICT_PATH, "r", encoding="utf-8") as dict_file:
    localization_dict = json.load(dict_file)

def indent_metadata(text):
    result = []
    indent = 0

    for line in text.splitlines():
        stripped = line.strip()

        closing = stripped.count("}")
        opening = stripped.count("{")

        if stripped.startswith("}"):
            indent -= 1

        indent = max(indent, 0)
        result.append("    " * indent + stripped)

        indent += opening - closing
        indent = max(indent, 0)

    return "\n".join(result)

txt_files = [f for f in os.listdir(FOLDER_PATH) if f.endswith(".txt")]

if not txt_files:
    raise FileNotFoundError(f"No .txt file found in {FOLDER_PATH}")

txt_file_path = os.path.join(FOLDER_PATH, txt_files[0])

with open(txt_file_path, "r", encoding="utf-8") as f:
    entries = [line.strip()[1:] for line in f if line.strip().startswith(">")]

for entry in entries:
    url = f"http://localhost:6155/get_effective_metadata?{entry}"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        content = res.text.strip()
    except Exception:
        with open(ERROR_LOG_PATH, "a", encoding="utf-8") as error_log:
            error_log.write(entry + "\n")
        continue

    skip_check = content.lower()
    if "no such patch" in skip_check or "patch not applied" in skip_check:
        with open(ERROR_LOG_PATH, "a", encoding="utf-8") as error_log:
            error_log.write(entry + "\n")
        continue

    formatted = indent_metadata(content)
    output_text = f">{entry}\n{formatted}"

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
        with open(os.path.join(FOLDER_PATH, filename), "w", encoding="utf-8") as out_file:
            out_file.write(output_text)
    except Exception:
        with open(ERROR_LOG_PATH, "a", encoding="utf-8") as error_log:
            error_log.write(entry + "\n")

print("Done.")
