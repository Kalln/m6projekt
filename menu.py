from main import ALL_GAMES


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

def match_menu(game_dict):
    title = f"{game_dict['HOME']} - {game_dict['AWAY']}"
    return menu(title, MATCH_OPTIONS, 'match', game_dict)

# genererar nya val i menyn, denna är dynamisk och väljer beroende på hur många matcher som
# finns i databasen
def generate_options(sport):
    sport_games = generate_list_of_sport(sport)
    new_options = {}

    for game in sport_games:
        
        new_options[game['ID']] = f"{game['HOME']} - {game['AWAY']}"
    
    return new_options
