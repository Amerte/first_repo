from datetime import datetime, date, timedelta
import json
import os


class DutyCalendar:
    def __init__(self, file_path):
        self.file_path = file_path
        self.places = []
        self.duties = {}

        if os.path.exists(self.file_path):
            self._load_from_json()
        else:
            self._save_to_json()

    def _load_from_json (self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f) 
        tmp_dict = {}
        for duty_date, duty_place in data["duties"].items():
            formated_date = datetime.strptime(duty_date, "%d.%m.%Y").date() 
            tmp_dict[formated_date] = duty_place

        self.duties = tmp_dict
        self.places = data["places"]
                

    
    def _save_to_json(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            tmp_dict = {}
            for duty_date, duty_place in self.duties.items():
                formated_date = duty_date.strftime("%d.%m.%Y")
                tmp_dict[formated_date] = duty_place
            json.dump({"duties": tmp_dict, "places":self.places}, f, ensure_ascii=False, indent = 4)

    def add_duty(self,duty_date, place):
        #duty_date = datetime.strptime(duty_date, "%d.%m.%Y").date()
        if place not in self.places:
            self.places.append(place)
        self.duties[duty_date]= place
        self._save_to_json()

    def add_place(self, place):
        if place not in self.places:
            self.places.append(place)
        self._save_to_json()




