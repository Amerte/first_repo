import tkinter as tk
from datetime import date, timedelta

root = tk.Tk()  
root.title("График дежурств")
root.geometry("400x300")


label = tk.Label(root, text = "Вітаю у застосунку контролю чергувань", fg= "red", font=("Colibri"))
label.pack()

duty_types = []
selected = tk.StringVar(value = None)

menu= tk.OptionMenu(root, selected, "выпадающее меню")
menu.pack()


#Кнопки и все с ними связанное
def button_action_1():
    print ("Кнопка працює")
    label.config(text="Тепер кнопка змінила текст!")

def button_statistic():
    pass

def add_duty():
    pass

def add_new_type():
    new_window= tk.Toplevel(root)

    entry= tk.Entry(new_window)
    entry.pack()

    def save_new_type():
        new_type = entry.get()
        if new_type:
            duty_types.append(new_type)
            menu['menu'].delete(0, 'end')
            for item in duty_types:
                menu['menu'].add_command(label = item, command = tk._setit(selected, item))
        new_window.destroy()
    save_button = tk.Button(new_window, text = "save changes", command=save_new_type)
    save_button.pack()

button = tk.Button(root, text = "Натисни на мене", bg= "white", fg="black", font=("Times New Roman", 16), command=button_action_1)
button.pack()

button = tk.Button(root, text = "Show Statistic", bg= "white", fg= "black", font=("Times New Roman", 16), command=button_statistic)
button.pack()

button = tk.Button(root, text= "Add duty", bg= "white", fg= "black", font=("Times New Roman", 16), command=add_duty)
button.pack()

button = tk.Button(root, text="Add new duty place", bg="white", fg="black", font=("Times New Roman", 16), command=add_new_type)
button.pack()


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
    label = tk.Label(frame_calendar,
                    text = format_day(day),
                    fg= "black", 
                    bg ="#e0f7fa",
                    font=("Times New Roman", 12),
                    relief= "ridge",
                    borderwidth=2,
                    width=15,
                    height=3
                )
    label.grid(row=row, column = column, padx = 5, pady = 5)
    i+=1


root.mainloop()
