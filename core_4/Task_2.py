from pathlib import Path
import os

with open("core_4\\Cats_file.txt", 'w') as file:
    file.write ('''60b90c1c13067a15887e1ae1,Tayson,3
60b90c2413067a15887e1ae2,Vika,1
60b90c2e13067a15887e1ae3,Barsik,2
60b90c3b13067a15887e1ae4,Simon,12
60b90c4613067a15887e1ae5,Tessi,5
''')
def get_cats_info(path):
    try:    
        with open("core_4\\Cats_file.txt", 'r') as file:
            cats_info = []
            for line in file:
                id, name, age = line.split(",")
                cats_info.append({"id":id, "name": name,"age": age.strip()})
            for x in cats_info:
                print(x)
    except FileNotFoundError:
        print("Файл не знайдено перевірте правильність шляху")
    except ValueError:
        print("Помилка в форматі файлу")

get_cats_info("core_4\\Cats_file.txt")