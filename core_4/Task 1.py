from pathlib import Path

salary_file = Path("core_4/salary.txt")

def total_salary(path):
    try:
        with open(salary_file, 'r') as file:
            x = [] 
            total = 0
            for line in file:
                person, salary = line.split(",")
                x.append(salary)
            for items in x:
                total += int(items)
            average = total / len(x)
            print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")
    except FileNotFoundError:
        print ("Файл не знайденб перевірте правильність шляху")
    except ValueError:
        print("Помилка в форматі файлу")
    

total_salary(salary_file)
