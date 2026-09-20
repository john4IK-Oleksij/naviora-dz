import json

def load_tours():
    with open("data/tours.json", "r", encoding="utf-8") as file:
        tours_list = json.load(file)
    return tours_list

def save_tours(tours_list):
    with open("data/tours.json", "w", encoding="utf-8") as file:
        json.dump(tours_list, file, ensure_ascii=False, indent=2)