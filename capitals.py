import json

def load_capitals():
    """Завантажує список столиць із файлу capitals.json"""
    with open("capitals.json", "r", encoding="utf-8") as file:
        capitals = json.load(file)
    return capitals

if __name__ == "__main__":
    capitals = load_capitals()
    print(f"✅ Завантажено {len(capitals)} столиць")
