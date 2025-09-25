import tkinter as tk

root = tk.Tk()  
root.title("График дежурств")
root.geometry("400x300")


label = tk.Label(root, text = "Вітаю у застосунку контролю чергувань", fg= "red", font=("Colibri"))
label.pack()

#Кнопки и все с ними связанное
def button_action_1():
    print ("Кнопка працює")
    label.config(text="Тепер кнопка змінила текст!")

    

button = tk.Button(root, text = "Натисни на мене", bg= "white", fg="black", font=("Times New Roman", 16), command=button_action_1)
button.pack()




root.mainloop()
