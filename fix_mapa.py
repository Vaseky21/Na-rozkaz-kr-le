import json

with open("data/mapa.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Sort keys numerically
sorted_keys = sorted(data.keys(), key=int)
new_data = {k: data[k] for k in sorted_keys}

with open("data/mapa.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)

print("mapa.json has been deduplicated and sorted!")
