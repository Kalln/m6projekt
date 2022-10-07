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
LOGGED_IN_USER = ""
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
                 return "logout"

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
                return "back"


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
                user = None
                break

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
            if state == "logout": 
                state = "inlogg" #TODO: Fråga om användaren är säker

        # Menyn med alla olika sporter
        #         
        elif state == "sports":
            state = menuinit("Choose sports", state)
            if state == "fotboll":
                state == "fotboll"
            elif state == "basketball":
                state = "basketball"
            elif state == "handball":
                state = "handball"
            elif state == "back":
                state = "overview"

        ######################################
        #       MENYER FÖR OLIKA SPORTER     #
        ######################################
        elif state == "fotboll":
            # Skriva ut en meny med alla fotbolls matcher
            pass
        elif state == "baskeball":
            # Skriva ut en meny med alla basket matcher
            pass
        elif state == "handball":
            # Skriver ut en meny med alla handbolls matcher
            pass
            
# Sparar inloggade användarnamnet.      
def set_logged_in_user(user):
    global LOGGED_IN_USER
    LOGGED_IN_USER = user

def view_games(sport):
    if sport == "fotball":
        pass
    elif sport == "basketball":
        pass
    elif sport == "handball":
      pass  
mainloop()
print(LOGGED_IN_USER)
