#Определения дня недели и выведение календаря на ближайшую неделю
def day_today():
    today = date.today()
    return today

def format_day(day):
    return day.strftime("%d %B %Y")

def get_monday(some_day):
    monday = some_day - timedelta(days=some_day.weekday())
    return monday

monday = get_monday(day_today())
week_days = []
for i in range(7):
    new_day = monday + timedelta(days = i)
    week_days.append(new_day)


frame_calendar = tk.Frame(root)
frame_calendar.pack(pady=10)

i = 0
for day in week_days:
    row = i//3
    column = i%3
    day_button = tk.Button(frame_calendar,
                    text = format_day(day),
                    fg= "black", 
                    bg= "#e0f7fa",
                    font=("Times New Roman", 12),
                    relief= "ridge",
                    borderwidth=2,
                    width=15,
                    height=3,
                )
    day_button.config(command=lambda btn= day_button: change_button_color(btn))
    day_button.grid(row=row, column = column, padx = 5, pady = 5)
    i+=1
        