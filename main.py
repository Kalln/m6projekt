import csv # så vi kan hantera csv filer
from datetime import date #så vi kan konvertera till date format, som är enklare att hantera
import random

users = {
    "test": "test",
    "bengt": "bengt",
    "johan": "johan"
}

# Olika options för användaren att välja mellan.
options = {"r":"Try again", "q": "Quit"}

overview_options = {
    "1": "Spela",
    "2": "Se dina spel",
    "3": "Spelhistorik",
    "4": "TBD",
    "5": "logga ut"
}
sports_option = {
    "1": "Fotboll",
    "2": "Basketball",
    "3": "Icehockey",
    "4": "Handball",
    "5": "Back"
}
match_options = {
        "1": "ETT",
        "X": "KRYSS",
        "2": "TVÅ",
        "5": "Back"
    }
FILE = './data/matcher.csv' # Databasen av alla matcher.
LOGGED_IN_USER = "test" # Denna variabel håller koll på den inloggade användaren
ALL_GAMES = []

# Sparar inloggade användarnamnet.      
def set_logged_in_user(user):
    global LOGGED_IN_USER
    LOGGED_IN_USER = user

# meny
def menu(title, options, type, match=None):
    prompt = "Option: " # Användarens fråga när vi ska få in något värde

    # Följande skriver ut titeln samt alternativen som användaren har att välja mellan.
    print(f"""
    {title}
    """)

    for key, action in options.items():
        print(f"    {key}) {action}")

    """
    Bereoende på vilken meny som visas, kontrollerar vi rätt input från användaren.
    type = 'inlogg'                         -> "inlogg" skärmen visas där användaren loggar in
    type = 'fail_login'                     -> om användaren har misslyckats att logga in
    type = 'overview'                       -> Huvudmenyn där användaren kan navigera till olika alternativ, antingen att spela, visa sina spel, eller gå ur.
    type = 'sports'                         -> Menyn som visar alla tillgängliga sporter.
    type = 'fotboll' eller 'basketball' osv -> Menyn för den specifika sporten som valts i "sports"
    type = 'match'                          -> Menyn för den specifika valda matchen visas där användaren kan välja att spela antingen 1/x/2.
    """ 
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
                view_user_bettings(create_bettings('./data/mockup_played1.csv'))
                return "overview"
            elif userTry == '3':
                print("INTE IMPLEMENTERAD")
                return "overview"
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
            elif userTry == 'x': # spel på lika
                place_bet('X', match)
                return 'sports'
            elif userTry == '2': #spel på bortalaget
                place_bet('2', match)
                return 'sports'
            elif userTry == '5': # gå tillbaka
                return "sports"

def place_bet(place_bet_on, game_dict):
    """
    En meny där användaren får ge sin insats. Vi kontrollerar att det vad användaren har skrivit in är en integer. annars frågar vi om igen.

    """
    odds_on_user_choice = get_odds_on_bet(place_bet_on, game_dict)
    print(f"""
        {game_dict['HOME']} - {game_dict['AWAY']}
        ODDS: {odds_on_user_choice}
    """)
    while True: # kolla så att den är ett heltal som användaren skriver in
        insats = input("insats: ")
        try:
            (int(insats))
            save_bet(place_bet_on, game_dict, insats, odds_on_user_choice)
            return 'sports'
        except:
            print('Inte ett heltal')

def get_odds_on_bet(bet_choice, game_dict):
    if bet_choice == "1":
        return game_dict['HOMEODDS']
    elif bet_choice == 'X':
        return game_dict['TIEODDS']
    elif bet_choice == '2':
        return game_dict['AWAYODDS']


def save_bet(place_bet_on, game_dict, insats, odds):
    """ Sparar bettet till en databas.
    
    Argument: 
    place_bet_on(string): antingen 1/x/2 beroende på vad användaren har valt att spela på.
    game_dict(dictionary): matchen som användaren vill spela på
    insats(int): insatsen för spelet
    odds(float): oddset för det spelet

    bet_data: är info om spelet som placeras av användaren i följande ordning:
    MATCHID,(1/X/2),INSATS,ODDS,ANVÄNDARE
    """
    
    
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
    """
    När en match har blivit vald så ropas denna funktion. Den ser till att den valda matchen visar nya alternativ och skapar
    en ny meny där användaren sedan kan välja antingen 1/x/2 spel.

    Argument: 
    game_dict(dictionary): detta är matchen (dictionary) som användaren har valt att spela på.
    """
    title = f"""
    {game_dict['HOME']}     -     {game_dict['AWAY']}
    HOME:  {game_dict['HOMEODDS']} TIE: {game_dict['TIEODDS']} AWAY: {game_dict['AWAYODDS']}

    """ # titeln består av "hemmalag-bortalag" och odds
    match_options = {
            "1": "Hemmalaget vinner",
            "x": "Lika",
            "2": "Bortalaget vinner",
            "5": "Back"
        }
    return menu(title, match_options, 'match', game_dict)


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
    """Ser till att funktionen menu() visar rätt alternativ.

    Argument: 
    title(string):      Är titeln på alternativen som visas till användaren
    typeofmenu(string): Variabeln ser till att rätt meny visas.

    Returvärde: 
    state(string):  returnernar state alltså, "overview","sports","fotboll"..osv. som avgör vilken meny användaren vill navigera till.
                    Detta värde får vi från menu() funktionen
    """
    TYPE = typeofmenu
    if typeofmenu == "inlogg":
        OPTIONS = options

    elif typeofmenu == "overview":
        OPTIONS = overview_options

    elif typeofmenu == "sports":
        OPTIONS = sports_option

    elif typeofmenu == "fotboll" or typeofmenu == "basketball":
        OPTIONS = generate_options(typeofmenu) # generate_options genererar användarens valmöjligheter. 
        
        #TODO: Skriva ut varje match bereonde på sport
    
    return menu(title, OPTIONS, TYPE)

def mainloop():
    """
        Variabeln state avgör vilken meny som användaren
        varje meny har en egen if-sats som skapar en meny bereonde på var i programmet användaren är.
    """

    state = "inlogg" # första gången visas "inlogg"-skärmen
    while True: 

        # 'INLOGG'-skärmen
        # börjar med att ropa på login funktionen, där users är en dictionary med användarnamn och lösenord.
        # login returnerar användarnamnet och vi ger den globala variabeln "LOGGED_IN_USER" på rad 33. 
        if state == "inlogg":
            logged_in_user = login(users)
            if logged_in_user != None:
                set_logged_in_user(logged_in_user)
                state = "overview"
            else:
                print(LOGGED_IN_USER)
                break
        
        # den generella menyn för användaren
        elif state == "overview":
            state = menuinit("Overview", state)

        # Menyn med alla olika sporter       
        elif state == "sports":
            state = menuinit("Choose sports", state)

        
        # MENYER FÖR OLIKA SPORTER
        elif state == "fotboll" or state == 'basketball' or state == 'baseball':
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
            homeodds = "%.2f" % random.uniform(1.8, 4.5)
            tieodds = "%.2f" % random.uniform(1.8, 4.5)
            awayodds = "%.2f" % random.uniform(1.8, 4.5)
            dict_to_be_added = {
                'ID': game[0],
                "HOME": game[1],
                "AWAY": game[2],
                'DATE': convert_to_time(game[3]),
                'TIME':   game[4],
                'SPORT': game[6],
                'HOMEODDS': homeodds,
                'TIEODDS':  tieodds,
                'AWAYODDS': awayodds
            }
            finalgame.append(dict_to_be_added)
            
    return finalgame

def create_bettings(file):
    """
    Mer dokumentation
    """
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
                'USER':     bets[4]
            }
            final_dict_betting.append(dict_to_be_added)
            
    return final_dict_betting

def view_user_bettings(bettings):
    # TITELN
    # SPORT 1 
    # HEMMA - BORTA [17/10-22 15:00]
    # INSATS: 20 ODDS: 2.00  
    # UTDELNING: 40

    # variabelen games: innehåller alla spel
    games = ALL_GAMES
    print("DINA SPEL")
    for bets in bettings:
        gameid = bets['MATCHID']
        for game in games:
            if(game['ID'] == gameid):
                if(bets['USER'] == LOGGED_IN_USER):
                    print(f"""
                        {game['HOME']} - {game['AWAY']} [{game['DATE']} {game['TIME']}]
                        Spelat: {bets['SPELAT']}
                        Insats: {bets['INSATS']} ODDS: {bets['ODDS']}
                        Utdelning: {int(bets['INSATS'])*float(bets['ODDS'])}
                    """)


    
    # argumentet bettings har alla bets
    # Skriv ut varje spel för varje sport tillsammans. 

    pass


def convert_to_time(time='2022,10,12'):
    """
    Konverterar till datetime format. 

    Argument:
    time(str): Innehåller värden av datum i formattet 'YYYY,MM,DD'.

    Returvärdet:
    datetime (ett datum)
    """
    rawtime = time.split(',')
    date_temp = date(int(rawtime[0]), int(rawtime[1]), int(rawtime[2]))
    return date_temp

def generate_options(sport):
    """Genererar nya val i menyn när användaren ska välja match att spela på.

    Args:
        sport (str): en sport som avgör vilka matcher i en valbar lista.

    Returns:
        dictionary: en dictionary med val alternativ som nyckel och hemma och borta laget som värde.
    """
    sport_games = generate_list_of_sport(sport)
    new_options = {}

    for game in sport_games:
        
        new_options[game['ID']] = f"{game['HOME']} - {game['AWAY']} --> [Datum: {game['DATE']} | Tid: {game['TIME']}]"
    
    return new_options


if __name__ == '__main__':
    ALL_GAMES = create_games(FILE) 
    #print(view_user_bettings(create_bettings('./data/mockup_played1.csv')))
    mainloop()
    #create_betting('1', ALL_GAMES[1], 26, 2.6)