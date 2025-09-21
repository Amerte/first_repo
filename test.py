trades = [
    {"token": "BTC", "entry": 100, "exit": 110, "position": "Long", "pnl": 0},
    {"token": "ETH", "entry": 200, "exit": 210, "position": "Short", "pnl": 0},
    {"token": "SOL", "entry": 50, "exit": 55, "position": "Long", "pnl": 0}
]

all_trades = []
def calculate_trade (entry, exit, token, position, pnl):
    
    if position == "Long":
        result = exit - entry
        pnl = result/entry*100
        all_trades.append(result)
    elif position == "Short":
        result = entry - exit
        pnl = result/entry*100
        all_trades.append(result)

        
    if result > 0:
        print ({ 
            "token":token, "position": position, "result": result, "pnl": pnl
            })
    elif result == 0:
        print ({ 
            "token":token, "position": position, "pnl": pnl
            })  
    else:
        print (
              { 
            "token":token, "position": position, "result": result, "pnl": pnl
            })
        
def stats():
    average = sum(all_trades)/len(all_trades)
    min_trade = min(all_trades)
    max_trade = max(all_trades)
    print (average)
    print (min_trade)
    print (max_trade)
       

for trade in trades:
    calculate_trade(trade["entry"], trade["exit"], trade["token"], trade["position"], trade["pnl"])

av_trades = stats()




    