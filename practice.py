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




def get_statistic(self):
        current_duties ={}
        prev_duties = {}
        other_duties = {}
        today = date.today()
        current_month = today.month
        current_year = today.year
        first_day_month = date(current_year, current_month, 1)
        last_day_prev = first_day_month - timedelta(days = 1)
        prev_month = last_day_prev.month
        prev_year = last_day_prev.year
        for duty_date in self.duties:
            if duty_date.month == current_month and duty_date.year == current_year:
                current_duties[duty_date] = self.duties[duty_date]
            elif duty_date.month == prev_month and duty_date.year == prev_year:
                prev_duties[duty_date] = self.duties[duty_date]
            else:
                other_duties[duty_date] = self.duties[duty_date]
        return current_duties, prev_duties, other_duties

current_duties, prev_duties, other_duties = calendar_data.get_statistic()
tmp_dict = {}
for cr_duty_date, cr_duty_place in current_duties.items():
    formated_date = cr_duty_date.strftime("%d,%m,%Y") 
print (formated_date, cr_duty_place)
