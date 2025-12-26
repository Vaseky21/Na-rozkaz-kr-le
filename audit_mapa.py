import json

with open("data/mapa.json", "r", encoding="utf-8") as f:
    story_map = json.load(f)

potential_dice = []
for page_id, data in story_map.items():
    choices = data.get("choices", [])
    if len(choices) >= 2:
        # Check if any choice is at the bottom of the page (y > 400)
        bottom_choices = [c for c in choices if c["area"][1] > 400]
        if len(bottom_choices) >= 2:
            potential_dice.append({
                "page": page_id,
                "choice_count": len(choices),
                "bottom_count": len(bottom_choices),
                "targets": [c["goto"] for c in choices]
            })

print(f"Potential dice roll pages (with 2+ bottom choices): {len(potential_dice)}")
for p in potential_dice:
    print(f"Page {p['page']}: {p['targets']}")
