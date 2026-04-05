import customtkinter as ctk
from tkcalendar import Calendar
from duty_control import DutyCalendar


def open_add_duty():
    frame_add_duty.pack()
    frame_main.pack_forget()
    duty_places.configure(values=calendar_data.places)
    print(calendar_data.places)

def open_statistic():
    frame_statistic.pack()
    frame_main.pack_forget()
    current_duties, prev_duties, other_duties = calendar_data.get_statistic()
    for cr_duty_date, cr_duty_place in current_duties.items():
        formated_date = cr_duty_date.strftime("%d,%m,%Y") 
    print (formated_date, cr_duty_place)
   
    #current, prev, other = calendar_data.get_statistic()
    
    print("Відкриваємо вікно статистики")

def open_add_place():
    frame_add_place.pack()
    frame_main.pack_forget()
    print("Відкриваємо вікно додавання нового місця чергування")

def go_back():
    frame_main.pack()
    frame_add_duty.pack_forget()
    frame_add_place.pack_forget()
    frame_statistic.pack_forget()

def save_add_duty():
    duty_date = cal.selection_get()
    duty_place =  duty_places.get()
    calendar_data.add_duty(duty_date, duty_place)
    show_pop_up()

    print ("Saved")

def show_pop_up():
    pop_up = ctk.CTkToplevel(app)
    pop_up.geometry("450x300")
    pop_up_label = ctk.CTkLabel(pop_up, text = "Зміни успішно збережені")
    pop_up_label.pack(pady = 50)
    pop_up.grab_set()
    def ok_clicked():
        pop_up.destroy()
        go_back()
    btn_ok = ctk.CTkButton(pop_up, text ="Ok", command = ok_clicked)
    btn_ok.pack(pady =60)

def save_add_place():
    new_place = str_add_place.get()
    calendar_data.add_place(new_place)
    show_pop_up()
    


    print(f"New place - {new_place} - has been added")
    

   
app = ctk.CTk()
app.title("Контроль за графіком нарядів")
app.geometry("600x500")

frame_main = ctk.CTkFrame(app)
frame_main.pack()

label = ctk.CTkLabel (frame_main, text = "Вітаю в застосунку контролю нарядів")
label.pack(pady = 10)

#кнопки навігації
btn_add_duty= ctk.CTkButton(frame_main, text = "Додати нарядец", command = open_add_duty)
btn_add_duty.pack(pady = 10)

btn_statistic = ctk.CTkButton(frame_main, text = "Статистика нарядів", command = open_statistic)
btn_statistic.pack(pady = 10)

btn_add_type = ctk.CTkButton(frame_main, text = "Додати місце наряду", command = open_add_place)
btn_add_type.pack(pady = 10)

#Вікна кнопок
frame_add_duty = ctk.CTkFrame(app)
cal = Calendar(frame_add_duty)
cal.pack()
calendar_data = DutyCalendar("duties.json")
duty_places= ctk.CTkOptionMenu(frame_add_duty, values = calendar_data.places)
duty_places.pack()
btn_save_add_duty = ctk.CTkButton(frame_add_duty, text = "Зберегти", command = save_add_duty)
btn_save_add_duty.pack(pady = 60)



frame_add_place = ctk.CTkFrame(app)
str_add_place = ctk.CTkEntry(frame_add_place, placeholder_text="Write the new place")
str_add_place.pack(pady =20)
btn_save_add_place = ctk.CTkButton(frame_add_place, text="Save", command = save_add_place)
btn_save_add_place.pack(pady = 20)

frame_statistic = ctk.CTkFrame(app)

frame_scrollable = ctk.CTkScrollableFrame(frame_statistic)
frame_scrollable.pack()

#кнопки повернення
btn_back_add_duty = ctk.CTkButton(frame_add_duty, text = "Назад", command = go_back)
btn_back_add_duty.pack(pady = 40)

btn_back_add_place = ctk.CTkButton(frame_add_place, text = "Назад", command = go_back)
btn_back_add_place.pack(pady = 40)

btn_back_statistic = ctk.CTkButton(frame_statistic, text = "Назад", command = go_back)
btn_back_statistic.pack(pady = 40)

app.mainloop()