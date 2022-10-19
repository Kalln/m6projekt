import random
from main import LOGGED_IN_USER

def place_bet(place_bet_on, game_dict):
    # Placera spelet, där "place_bet_on" är 1,x eller 2. som avgör vad man spelar på.
    odds_on_user_choice = random.uniform(1.1, 3.8)
    print(f"""
        {game_dict['HOME']} - {game_dict['AWAY']}
        ODDS: {odds_on_user_choice}
    """)
    while True: # kolla så att den är ett heltal som användaren skriver in
        insats = input("insats: ")
        try:
            (int(insats))
            create_betting(place_bet_on, game_dict, insats, odds_on_user_choice)
            return 'sports'
        except:
            print('Inte ett heltal')

def create_betting(place_bet_on, game_dict, insats, odds):
    # bet_data: är info om spelet som placeras av användaren i följande ordning:
    # MATCHID,(1/X/2),INSATS,ODDS,ANVÄNDARE
    
    bet_data = [game_dict['ID'],
                place_bet_on,
                insats,
                odds,
                LOGGED_IN_USER
                ]

    # Detta öppnar csv filen och lägger till bet_data på en ny rad.
    with open('test.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(bet_data)
    print("bet placed")

def create_bettings(file):
    raw_bettings = []
    final_dict_betting = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            raw_bettings.append(row)
            
    
    for bets in raw_bettings:
        if bets[1] != 'spelat':
            dict_to_be_added = {
                'MATCHID':  bets[0],
                "SPELAT":   bets[1],
                "INSATS":   bets[2],
                'ODDS':     bets[3],
                'USER':     bets[4],
            }
            final_dict_betting.append(dict_to_be_added)
            
    return final_dict_betting
