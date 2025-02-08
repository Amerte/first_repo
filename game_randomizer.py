import random

games = list()
#ведення даних

while True:
    games_name = str(input("Назва гри "))
    if games_name == "":
        break    
    games.append(games_name)

#рандомізація
try:
    result = random.choice(games)
    print (f"Ви граєте у {result}")
except:
    print ("Ви що самі вирішили?")

