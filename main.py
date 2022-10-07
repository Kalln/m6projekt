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

# meny
def menu(title, prompt, options, typeofmeny):
    print(title)
    for key, action in options.items():
        print(f"    {key}) {action}")

    if typeofmeny == "inlogg":
        while True: 
            userTry = input(prompt)
            if userTry == 'r' or userTry == 'q': 
                return userTry

    if typeofmeny == "overview":
        while True:
            userTry = input(prompt)
            if userTry == '1': 
                menu("Sports", "Option: ", sportoptions, "sports")
            elif userTry == '2':
                return "game"
            elif userTry == '3':
                return "game_history"
            elif userTry == '4':
                return None
            elif userTry == '5':
                return "logout"

    if typeofmeny == "sports":
         while True:
            userTry = input(prompt)
            if userTry == '1': 
                return "fotboll"
            elif userTry == '2':
                return "basketball"
            elif userTry == '3':
                return "game_history"
            elif userTry == '4':
                return None
            elif userTry == '5':
                return "logout"

# login

def login(users):
    while True: 
        user = input('    User: ')
        password = input('Password: ')

        if user in users and password == users[user]:
            return user
            break
        else: 
            userTry = menu('Invalid username or password', 'Option: ', options)
            if userTry == 'q':
                user = None
                break
# meny 2

menu("Övergripande vy", "Options: ", inlogg, "inlogg")