import json

class Car:
    def __init__(self,carid, make, category, model, year, price, color, picture_url):
        self.carid = carid
        self.make = make
        self.category = category        
        self.model = model
        self.year = year
        self.price = price
        self.color = color
        self.picture_url = picture_url
        self.is_available = True

    def get_carid(self):
        return self.carid
    
    def to_json(self):
        return {"carid":self.carid, "make":self.make, "year":self.year, "category":self.category, "model":self.model, "color":self.color, "pride":self.price}
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model} - ${self.price}"
    
    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)
    
class Car_manager:
    def __init__(self, filepath="../data/car_inventory.json") -> None:
        self.car_inventory = []

        with open(filepath, "r") as json_file:
            json_data = json.load(json_file)

        for data in json_data:
            car = Car.from_json(data)
            self.car_inventory.append(car)

    def get_car_inventory(self):
        return self.car_inventory
    
    def get_car_info(self, carid):
        for car in self.car_inventory:
            if car.carid == carid:
                return car
        return None
        
    def get_car_display_name(self, carid):
        for car in self.car_inventory:
            if car.carid == carid:
                return f"{self.year} {self.make} {self.model} - ${self.price}"
        return None
        