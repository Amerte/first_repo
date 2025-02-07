import random


games = list()
#ведення даних

while True:
    games_name = str(input("Назва гри "))
    if games_name == "":
        break
    games.append(games_name)    
  
#рандомізація
result = random.choice(games)
print ("Ви граєте у " + result)
