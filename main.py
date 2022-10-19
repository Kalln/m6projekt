import csv # så vi kan hantera csv filer
from datetime import date #så vi kan konvertera till date format, som är enklare att hantera
import random
# from menu import menuinit
from betting_handler import place_bet, create_betting, create_bettings

users = {
    "test": "test"
}

FILE = './data/matcher.csv'
LOGGED_IN_USER = "" # Denna variabel håller koll på den inloggade användaren
ALL_GAMES = []

# Sparar inloggade användarnamnet.      
def set_logged_in_user(user):
    global LOGGED_IN_USER
    LOGGED_IN_USER = user



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

if __name__ == '__main__':
    ALL_GAMES = create_games(FILE) 
    #print(view_user_bettings(create_bettings('mockup_played1.csv')))
    #mainloop()
    place_bet('2',ALL_GAMES[1])