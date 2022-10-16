import csv # så vi kan hantera csv filer
from datetime import date #så vi kan konvertera till date format, som är enklare att hantera

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
FILE = 'matcher.csv'
LOGGED_IN_USER = "" # Denna variabel håller koll på den inloggade användaren
ALL_GAMES = []

# Sparar inloggade användarnamnet.      
def set_logged_in_user(user):
    global LOGGED_IN_USER
    LOGGED_IN_USER = user

# meny
def menu(title, options, type):
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
    
    elif type == "fotboll":
        while True:
            userTry = input(prompt)
            print(options)
            if userTry in options: 
                print(options[userTry])
                break
                # här måste vi få en till meny så att användaren kan spela på den valda matchen


# login

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
        print(OPTIONS)
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
        elif state == "fotboll":
            state = menuinit('Choose game to play', state)

        elif state == "baskeball":
            # Skriva ut en meny med alla basket matcher
            pass
        elif state == "handball":
            # Skriver ut en meny med alla handbolls matcher
            pass

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
        if game['sport'] == chosen_sport:
            games_list.append(f"{game['hemma']} - {game['borta']}")

    return games_list


def create_games(file):
    """Skapar en dictionary med alla spel som finns i file

    Args:
        file: en csv fil som innehåller info om alla matcher

    Returvärdet: 
        [{spel1}, {spel2}].
        där dictionarien t.ex. är: {"hemma": "Djurgården", "borta": "AIK", osv}
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
                'id': game[0],
                "hemma": game[1],
                "borta": game[2],
                'datum': convert_to_time(game[3]),
                'tid':   game[4],
                'sport': game[6]
            }
            finalgame.append(dict_to_be_added)
            
    return finalgame

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

    for i in range(len(sport_games)):
        new_options[str(i+1)] = sport_games[i]
    
    return new_options


if __name__ == '__main__':
    ALL_GAMES = create_games(FILE) 
    mainloop()