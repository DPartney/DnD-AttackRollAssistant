from termcolor import colored
from enum import Enum
import sys, random, json

'''
TO DO:

Feats/Settings
'''

class RollType(Enum):
    ADVANTAGE = 1
    NORMAL = 2
    DISADVANTAGE = 3

class Feats(Enum):
    ElvenAccuracy = 1
    GreatWeaponFighter = 2

# Format for rerolls
# rolled 4d6 (6,1,2,3)
# rerolled 2d6(1,3)
# final (6,1,3,3)

class User:
    username = "default"
    attackModifier = 0
    numberAttacks = 1
    damageDieType = 0
    damageDieRollAmount = 1
    critModifier = 20
    proficiencyBonus = 0

def ModifyProfBonus(user):
    while True:
        try:
            user.proficiencyBonus = int(input(colored("Enter your proficiency bonus: ", color="cyan")))
            if CheckYorN("Your proficiency bonus is: " + str(user.proficiencyBonus) + "? y/n: ") == "y":
                return
        except ValueError:
            print(colored("invalid Input! Please enter a valid number.", color="red"))

def ModifyCritMod(user):
    while True:
        try:
            user.critModifier = int(input(colored("Enter the lowest number you crit with: ", color="cyan")))
            if CheckYorN("Your crit mod is: " + str(user.critModifier) + "? y/n: ") == "y":
                return
        except ValueError:
            print(colored("invalid Input! Please enter a valid number.", color="red"))

def ModifyAttackMod(user):
    while True:
        try:
            user.attackModifier = int(input(colored("Enter your attack modifier: ", color="cyan")))
            if user.attackModifier < -10:
                print(colored("Invalid input. Please enter a number greater than or equal to -10.", color="red"))
            else:
                break
        except ValueError:
            print(colored("Invalid input. Please enter a valid number.", color="red"))
    print(colored("Attack modifier set to: ", color="green"), end="")
    print(str(user.attackModifier))

def ModifyAttackCount(user):
    while True:
        try:
            user.numberAttacks = int(input(colored("Enter your attacks per turn: ", color="cyan")))
            if user.numberAttacks <= 0:
                print(colored("Invalid input. Please enter a number greater than 0.", color="red"))
            else:
                break
        except ValueError:
            print(colored("Invalid input. Please enter a valid number.", color="red"))
    print(colored("Number of attacks per turn set to: ", color="green"), end="")
    print(str(user.numberAttacks))

def ModifyDamageDieDamage(user):
    while True:
        try:
            user.damageDieType = int(input(colored("Enter your damage dice's highest number: ", color="cyan")))
            if user.damageDieType < 0:
                print(colored("Invalid input. Please enter a number greater than 0.", color="red"))
            else:
                break
        except ValueError:
            print(colored("Invalid input. Please enter a valid number.", color="red"))
    print(colored("Damage dice type set to: ", color="green"), end="")
    print("D" + str(user.damageDieType))

def ModifyDamageDieRollAmount(user):
    while True:
        try:
            user.damageDieRollAmount = int(input(colored("Enter your damage dice's roll amount per attack: ", color="cyan")))
            if user.damageDieRollAmount < 0:
                print(colored("Invalid input. Please enter a number greater than 0.", color="red"))
            else:
                break
        except ValueError:
            print(colored("Invalid input. Please enter a valid number.", color="red"))
    print(colored("Damage dice rolled per attack set to: ", color="green"), end="")
    print(str(user.damageDieRollAmount))

def DisplayStats(user):
    print(colored("-"*35, color="magenta"))
    OutputCommand("Attack Modifier: ", str(user.attackModifier))
    OutputCommand("Crit Modifier: ", str(user.critModifier))
    OutputCommand("Proficiency Bonus: ", str(user.proficiencyBonus))
    OutputCommand("Number of Attacks per Turn: ", str(user.numberAttacks))
    OutputCommand("Damage Dice Type: ", "D" + str(user.damageDieType))
    OutputCommand("Damage Dice Roll Amount: ", str(user.damageDieRollAmount))
    print(colored("-"*35, color="magenta"))

def CalculateAttack(user):
    for count in range(0, user.numberAttacks):
        while True:
            print(colored("Attack " + str(count + 1) + ": ", color="magenta"))
            userInput = input(colored("Advantage, Normal or Disadvantage: ", color="light_blue")).strip().upper()
            if userInput in "ADVANTAGE":
                user.attackRollType = RollType.ADVANTAGE
                if CheckYorN("Roll with advantage? y/n: ") == "y":
                    break
            elif userInput in "DISADVANTAGE":
                user.attackRollType = RollType.DISADVANTAGE
                if CheckYorN("Roll with disadvantage? y/n: ") == "y":
                    break
            elif userInput in "NORMAL":
                user.attackRollType = RollType.NORMAL
                if CheckYorN("Roll normally? y/n: ") == "y":
                    break
            else:
                print(colored("Invalid Input! Choose roll type!", color="red"))
    
        isCritting = False
        attackRoll = random.randint(1, 20)
        if user.attackRollType == RollType.ADVANTAGE:
            attackRoll = max(attackRoll, random.randint(1, 20))
        elif user.attackRollType == RollType.DISADVANTAGE:
            attackRoll = min(attackRoll, random.randint(1, 20))
        print(colored("Rolled a(n): ", color="light_blue"), end="")


        attackMod = user.attackModifier
        profBonus = user.proficiencyBonus
        if attackRoll >= user.critModifier:
            isCritting = True
            print(colored(str(attackRoll + (attackMod + profBonus)), color="green"), end="")
        elif attackRoll <= 1:
            print(colored(str(attackRoll + (attackMod + profBonus)), color="red"), end="")
        else:
            print(colored(str(attackRoll + (attackMod + profBonus)), color="white"), end="")
        print(colored(" to hit (", color="white"), end="")
    
        if attackRoll >= user.critModifier:
            print(colored(str(attackRoll), color="green"), end="")
        elif attackRoll <= 1:
            print(colored(str(attackRoll), color="red"), end="")
        else:
            print(colored(str(attackRoll), color="white"), end="")
    
        print(colored(" + " + str(attackMod) + " + " + str(profBonus) + ")", color="white"))
    
        if CheckYorN("Roll for damage? y/n: ") == "n":
            return
    
        damage = 0
        critMod = 2 if isCritting else 1
        print(colored("Rolled: ", color="light_blue"), end="")
        print(colored(str(user.damageDieRollAmount * critMod) + "D" + str(user.damageDieType) + " (", color="white"), end="")
        for count in range(user.damageDieRollAmount * critMod):
            amountRolled = random.randint(1, user.damageDieType)
            damage += amountRolled
            if (amountRolled == user.damageDieType):
                print(colored(str(amountRolled), color="green"), end="")
            elif(amountRolled == 1):
                print(colored(str(amountRolled), color="red"), end="")
            else:
                print(colored(str(amountRolled), color="white"), end="")
            if (count == (user.damageDieRollAmount * critMod) - 1):
                print(colored(")", color="white"))
            else:
                print(colored(", ", color="white"), end="")
    
        print(colored("Final Damage: ", color="light_green"), end="")
        print(str(damage + attackMod) + " (" + str(damage) + " + " + str(attackMod) + ")")

def CheckYorN(prompt):
    while(True):
        userInput = input(colored(prompt, color="light_green")).strip().lower()
        if userInput == "y" or userInput == "n":
            return userInput
        else:
            print(colored("Ivalid Input! Type y or n", color="red"))

def OutputCommand(comName, comDescription):
    print(colored(comName, color="light_green"), end="")
    print(comDescription)

def main():
    print(colored("Welcome to the D&D Attack Roll Assistant!", color="light_green") )
    print(colored("Type help for list of modifiers & commands", color="light_green"))
    currentUser = User()
    userName = input(colored("\nEnter Username: ", color="light_blue"))
    try:
        with open("D&D UsersDB.json", "r") as file:
            all_data = json.load(file)
            LoadUserData(all_data, userName, currentUser)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        with open("D&D UsersDB.json", "w") as file:
            new_entry = [{"Username": userName, "AttackMod": -10, "AttacksPT": 0, "DamageDiceType": 0,"DamageDiceRollAmount": 0, "CritMod": 20}]
            json.dump(new_entry, file, indent=4)
            print(colored("User not found, loading default settings.", color="red"))
    
    while True:
        userInput = input(colored("Enter a command: ", color="light_blue")).strip().lower()
        if userInput == "help":
            print(colored("Commands: ", color="magenta"))
            OutputCommand("calcAttack ", "- Calculate attack")
            OutputCommand("attackMod ", " - Modify attack modifier")
            OutputCommand("profBonus ", " - Modify proficiency bonus")
            OutputCommand("attackPT  ", " - Modify number of attacks per turn")
            OutputCommand("diceType  ", " - Modify damage dice type")
            OutputCommand("diceRoll  ", " - Modify damage dice roll amount")
            OutputCommand("critMod   ", " - Modify crit modifier")
            OutputCommand("stats     ", " - Display current stats")
            OutputCommand("save      ", " - Save User Data")
            OutputCommand("exit      ", " - Exit the program")
        elif userInput == "calcattack":
            CalculateAttack(currentUser)
        elif userInput == "attackmod":
            ModifyAttackMod(currentUser)
        elif userInput == "profbonus":
            ModifyProfBonus(currentUser)
        elif userInput == "attackpt":
            ModifyAttackCount(currentUser)
        elif userInput == "dicetype":
            ModifyDamageDieDamage(currentUser)
        elif userInput == "diceroll":
            ModifyDamageDieRollAmount(currentUser)
        elif userInput == "critmod":
            ModifyCritMod(currentUser)
        elif userInput == "stats":
            DisplayStats(currentUser)
        elif userInput == "save":
            SaveUserData(currentUser)
        elif userInput == "exit":
            sys.exit()

def SaveUserData(currentUser):
    with open("D&D UsersDB.json", "r") as file:
            all_data = json.load(file)
            for data in all_data:
                if currentUser.username in data.values():
                    all_data.remove(data)
            with open("D&D UsersDB.json", "w") as file:
                new_entry = [{"Username": currentUser.username, "AttackMod": currentUser.attackModifier, "ProfBonus": currentUser.proficiencyBonus, "AttacksPT": currentUser.numberAttacks, "DamageDiceType": currentUser.damageDieType,"DamageDiceRollAmount": currentUser.damageDieRollAmount, "CritMod": currentUser.critModifier}]
                json.dump(new_entry, file, indent=4)
    print(colored("Saved " + currentUser.username + "'s data", color="light_green"))

def LoadUserData(all_data, username, currentUser):
    found = False
    for data in all_data:
        if username.lower() in data["Username"].lower():
            found = True
            currentUser.username = data["Username"]
            currentUser.attackModifier = data["AttackMod"]
            currentUser.proficiencyBonus = data["ProfBonus"]
            currentUser.numberAttacks = data["AttacksPT"]
            currentUser.damageDieType = data["DamageDiceType"]
            currentUser.damageDieRollAmount = data["DamageDiceRollAmount"]
            currentUser.critModifier = data["CritMod"]
            print(colored("Loaded " + currentUser.username + "'s data", color="light_green"))
    if found:
        return
    else:
        print(colored("User not found, loading default settings.", color="red"))
        currentUser = User()
    

if __name__ == "__main__":
    main()
