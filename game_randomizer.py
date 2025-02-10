import random

variants = list()
#ведення даних

while True:
    choices_name = str(input("Введіть назву "))
    if choices_name == "":
        break    
    variants.append(choices_name)

#рандомізація
try:
    result = random.choice(variants)
    print (f"Цього разу це {result}")
except:
    print ("Ви що самі вирішили?")

