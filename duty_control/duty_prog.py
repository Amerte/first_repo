import tkinter as tk
from datetime import date, timedelta

root = tk.Tk()  
root.title("Контролль нарядів")
root.geometry("1024x720")


welcome_label = tk.Label(root, text = "Вітаю у застосунку відстежування нарядів", fg= "black", font=("Times New Roman", 14))
welcome_label.pack()

duty_types = [None]
selected = tk.StringVar(value = None)

menu= tk.OptionMenu(root, selected, *duty_types)
menu.pack()

def change_button_color(btn):
    current = btn.cget("bg")
    new_color = "green" if current == "#e0f7fa" else "#e0f7fa"
    btn.config(bg=new_color)
    

#Добавление нового дежурства

def on_day_click():
    new_window = tk.Toplevel(root)
    label = tk.Label(new_window, text="somethng")
    label.pack()


#Кнопки и все с ними связанное
def button_action_1():
    print ("Кнопка працює")
    welcome_label.config(text="Тепер кнопка змінила текст!")
    

def button_statistic():
    pass

def add_duty():
    new_duty_window = tk.Toplevel(root)
    new_duty_window.geometry("1024x720")
    label = tk.Label(new_duty_window, text="Обери потрібну дату наряду")
    label.pack()

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


    frame_calendar = tk.Frame(new_duty_window)
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

    
# Новый тип дежурства
def add_new_type():
    new_type_window= tk.Toplevel(root)

    entry= tk.Entry(new_type_window)
    entry.pack()

    def save_new_type():
        new_type = entry.get()
        if new_type:
            duty_types.append(new_type)
            menu['menu'].delete(0, 'end')
            for item in duty_types:
                menu['menu'].add_command(label = item, command = tk._setit(selected, item))
        new_type_window.destroy()
    save_button = tk.Button(new_type_window, text = "save changes", command=save_new_type)
    save_button.pack()

button = tk.Button(root, text = "Натисни на мене", bg= "white", fg="black", font=("Times New Roman", 16), command = on_day_click)
button.pack()

button = tk.Button(root, text = "Show Statistic", bg= "white", fg= "black", font=("Times New Roman", 16), command=button_statistic)
button.pack()

button = tk.Button(root, text= "Add duty", bg= "white", fg= "black", font=("Times New Roman", 16), command=add_duty)
button.pack()

button = tk.Button(root, text="Add new duty place", bg="white", fg="black", font=("Times New Roman", 16), command=add_new_type)
button.pack()


root.mainloop()
