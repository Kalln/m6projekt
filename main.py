import csv # så vi kan hantera csv filer
from datetime import date #så vi kan konvertera till date format, som är enklare att hantera
import random

users = {
    "test": "test"
}
options = {"r":"Try again", "q": "Quit"}

overview_options = {
    "1": "Spela",
    "2": "Se dina spel",
    "3": "Spelhistorik",
    "4": "TBD",
    "5": "logga ut"
}

sportsoption = {
    "1": "Fotboll",
    "2": "Basketball",
    "3": "Icehockey",
    "4": "Handball",
    "5": "Back"
}

MATCH_OPTIONS = {
        "1": "ETT",
        "X": "KRYSS",
        "2": "TVÅ",
        "5": "Back"
    }
FILE = './data/matcher.csv'
LOGGED_IN_USER = "test" # Denna variabel håller koll på den inloggade användaren
ALL_GAMES = []

# Sparar inloggade användarnamnet.      
def set_logged_in_user(user):
    global LOGGED_IN_USER
    LOGGED_IN_USER = user

# meny
def menu(title, options, type, match=None):
    prompt = "Option: "

    print(f"""
    {title}
    """)

    # Print menu
    for key, action in options.items():
        print(f"    {key}) {action}")

    # Bereoende på vilken meny som visas, kontrollerar vi rätt input från användaren.
    if type == "inlogg":
        userToLogin = login(users)
        if userToLogin != None:
            return None
        return "inlogg"

    elif type == "fail_login":
        while True: 
            selected = input(prompt)
            if selected == 'r' or selected == 'q':
                return selected

    elif type == "overview":
        while True:
            userTry = input(prompt)
            if userTry == '1': 
                return "sports"
            elif userTry == '2':
                return "game"
            elif userTry == '3':
                return "game_history"
            elif userTry == '4':
                return None
            elif userTry == '5':
                set_logged_in_user(None)
                return "inlogg"

    elif type == "sports":
        while True:
            userTry = input(prompt)
            if userTry == '1': 
                return "fotboll"
            elif userTry == '2':
                return "basketball"
            elif userTry == '3':
                return "handball"
            elif userTry == '4':
                return None
            elif userTry == '5':
                return "overview"
    
    elif type == "fotboll" or type == "basketball":
        while True:
            userTry = input(prompt)
            if userTry in options: 
                matchID = userTry
                for game in ALL_GAMES:
                    if matchID == game['ID']:
                        return match_menu(game)
                # här måste vi få en till meny så att användaren kan spela på den valda matchen
    elif type == "match":
        while True:
            userTry = input(prompt)
            if userTry == '1': # spel på hemmalaget
                place_bet('1', match)
                return 'sports'
            elif userTry == 'X': # spel på lika
                place_bet('X', match)
                return 'sports'
            elif userTry == '2': #spel på bortalaget
                place_bet('2', match)
                return 'sports'
            elif userTry == '5': # gå tillbaka
                return "sports"

def place_bet(place_bet_on, game_dict):
    odds_on_user_choice = random.uniform(1.1, 3.8)
    print(f"""
        {game_dict['HOME']} - {game_dict['AWAY']}
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
    with open('./data/test.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(bet_data)
    print("bet placed")

def match_menu(game_dict):
    title = f"{game_dict['HOME']} - {game_dict['AWAY']}"
    MATCH_OPTIONS = {
            "1": "ETT",
            "X": "KRYSS",
            "2": "TVÅ",
            "5": "Back"
        }
    return menu(title, MATCH_OPTIONS, 'match', game_dict)


def login(users):
    while True: 
        user = input('    User: ')
        password = input('Password: ')

        if user in users and password == users[user]:
            return user
            
        else: 
            userTry = menu('Invalid username or password', options, "fail_login")
            if userTry == 'q':
                return None

# Skapa menyn, denna funktion ser till att rätt meny visas.
def menuinit(title, typeofmenu):
    if typeofmenu == "inlogg":
        OPTIONS = options
        TYPE = "inlogg"
    elif typeofmenu == "overview":
        OPTIONS = overview_options
        TYPE = "overview"
    elif typeofmenu == "sports":
        OPTIONS = sportsoption
        TYPE = "sports"
    elif typeofmenu == "fotboll" or "basketball":
        OPTIONS = generate_options(typeofmenu)
        TYPE = typeofmenu
        
        #TODO: Skriva ut varje match bereonde på sport
    
    return menu(title, OPTIONS, TYPE)

def mainloop():

    # variabeln state avgör vilken meny som användaren är på
    # varje "meny" har en egen if-sats och i dessa if satser finns
    # det fler if-satser som gör det som ska göras bereonde på användarens input.
    state = "inlogg"
    while True: 

        # logga in skärmen
        if state == "inlogg":
            logged_in_user = login(users)
            if logged_in_user != None:
                set_logged_in_user(logged_in_user)
                state = "overview"
            else:
                print(LOGGED_IN_USER)
                break
        
        # den generella menyn för användanren
        elif state == "overview":
            state = menuinit("Overview", state)

        # Menyn med alla olika sporter
        #         
        elif state == "sports":
            state = menuinit("Choose sports", state)

        ######################################
        #       MENYER FÖR OLIKA SPORTER     #
        ######################################
        elif state == "fotboll" or 'basketball' or 'baseball':
            state = menuinit('Choose game to play', state)

def generate_list_of_sport(chosen_sport):
    """Funktionen väljer endast ut matcher som är i den valda sporten

    Args:
        chosen_sport (string): val av sport. T.ex. fotboll, basketball osv.

    Returns:
        list: lista med hemmalag och bortalag.
    """

    games = ALL_GAMES
    games_list = []

    for game in games:
        if game['SPORT'] == chosen_sport:
            games_list.append(game)

    return games_list


def create_games(file):
    """Skapar en dictionary med alla spel som finns i file

    Args:
        file: en csv fil som innehåller info om alla matcher

    Returvärdet: 
        [{spel1}, {spel2}].
        där dictionarien t.ex. är: {"HOME": "Djurgården", "AWAY": "AIK", osv}
    """

    games = []
    finalgame = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            games.append(row)
            
    
    for game in games:
        if game[1] != 'hemma':
            dict_to_be_added = {
                'ID': game[0],
                "HOME": game[1],
                "AWAY": game[2],
                'DATE': convert_to_time(game[3]),
                'TIME':   game[4],
                'SPORT': game[6]
            }
            finalgame.append(dict_to_be_added)
            
    return finalgame

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

def view_user_bettings(bettings):
    # TITELN
    # SPORT 1 
    # HEMMA - BORTA [17/10-22 15:00]
    # INSATS: 20 ODDS: 2.00  
    # UTDELNING: 40


    # Skriv ut varje spel för varje sport tillsammans. 
    pass


# konverterar tiden till datetime format
# datetime är enklare att hantera om man vill räkna ner till något.
def convert_to_time(time='2022,10,12'):
    rawtime = time.split(',')
    date_temp = date(int(rawtime[0]), int(rawtime[1]), int(rawtime[2]))
    return date_temp

# genererar nya val i menyn, denna är dynamisk och väljer beroende på hur många matcher som
# finns i databasen
def generate_options(sport):
    sport_games = generate_list_of_sport(sport)
    new_options = {}

    for game in sport_games:
        
        new_options[game['ID']] = f"{game['HOME']} - {game['AWAY']}"
    
    return new_options


if __name__ == '__main__':
    ALL_GAMES = create_games(FILE) 
    #print(view_user_bettings(create_bettings('./data/mockup_played1.csv')))
    #mainloop()
    create_betting('1', ALL_GAMES[1], 26, 2.6)