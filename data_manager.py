import json

class DataManager:
    def __init__(self, name):
        with open(file="user_data.json") as data:
            content = json.load(data)

        self.city_go = content[name]["from_country"]
        self.city_arrive = content[name]["to_country"]
        self.to_iata = content[name]["to_iata"]
        self.from_iata = content[name]["from_iata"]
        self.nonstop = content[name]["nonstop"]
        self.going_date = content[name]["travel_date"]
        self.arrival_date = content[name]["depature_date"]
        self.price = content[name]["price"]