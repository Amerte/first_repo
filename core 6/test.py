import tkinter as tk

root = tk.Tk()
root.title("Example")


def on_click(event, day):
    print(f"Day {day} was clicked at {event.x} and {event.y}")
    event.widget.config(bg='gray')

for day in range(1, 6):
    lbl = tk.Label(root, text = f"Day {day}", bg = "lightblue", width= 15)
    lbl.pack(pady = 15)

    lbl.bind("<Button-1>", lambda e, d=day: on_click(e, d))


root.mainloop()