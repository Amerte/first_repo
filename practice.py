import os
from datetime import datetime, date
import json


class DutyCalender:
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

        

        # try:
        #     with open("duties.json", "r", encoding="utf-8" ) as f:
        #         duties = json.load(f)
        # except FileExistsError:
        #     open("duties.json", "x", encoding="utf-8")

