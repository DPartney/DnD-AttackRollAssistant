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
    activeFeats = []

def ModifyProfBonus(user: User):
    while True:
        try:
            user.proficiencyBonus = int(input(colored("Enter your proficiency bonus: ", color="cyan")))
            if CheckYorN("Your proficiency bonus is: " + str(user.proficiencyBonus) + "? y/n: ") == "y":
                return
        except ValueError:
            print(colored("invalid Input! Please enter a valid number.", color="red"))

def ModifyCritMod(user: User):
    while True:
        try:
            user.critModifier = int(input(colored("Enter the lowest number you crit with: ", color="cyan")))
            if CheckYorN("Your crit mod is: " + str(user.critModifier) + "? y/n: ") == "y":
                return
        except ValueError:
            print(colored("invalid Input! Please enter a valid number.", color="red"))

def ModifyActiveFeats(user: User):
    all_feats = list(Feats)

    print(colored("Input the numbers from the list to activate those feats for your character", color="magenta"))
    for feat in all_feats:
        print(colored(feat.name + " - ", color="cyan"), end="")
        print(str(feat.value))
    while True:
        user_input = set(input(colored("List numbers seperated by a space and comma like 1, 3, 5: ", color="light_blue")).replace(" ", ""))
        user_input.discard(",")
        user_input = list(user_input)
        user_numbers = []
        for element in user_input:
            try:
                user_numbers.append(int(element))
            except ValueError:
                pass
        if len(user_numbers) == 0:
            if CheckYorN("No feats chosen! Leave without changes? y/n:") == 'y':
                return
            else:
                continue
        for featChoice in user_numbers:
            try:
                if Feats(featChoice).name in user.activeFeats:
                    if CheckYorN("Remove " + Feats(featChoice).name + " from active feats? y/n: ") == 'y':
                        user.activeFeats.remove(Feats(featChoice).name)
                        continue
                    else:
                        continue
                user.activeFeats.append(Feats(featChoice).name)
                print(colored(Feats(featChoice).name + " Added!", color="light_green"))
            except ValueError:
                pass
        break

def ModifyAttackMod(user: User):
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

def ModifyAttackCount(user: User):
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

def ModifyDamageDieDamage(user: User):
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

def ModifyDamageDieRollAmount(user: User):
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

def DisplayStats(user: User):
    print(colored("-"*35, color="magenta"))
    OutputCommand("Attack Modifier: ", str(user.attackModifier))
    OutputCommand("Crit Modifier: ", str(user.critModifier))
    OutputCommand("Proficiency Bonus: ", str(user.proficiencyBonus))
    OutputCommand("Number of Attacks per Turn: ", str(user.numberAttacks))
    OutputCommand("Damage Dice Type: ", "D" + str(user.damageDieType))
    OutputCommand("Damage Dice Roll Amount: ", str(user.damageDieRollAmount))
    print(colored("Active Feats: ", color="light_green"), end="")
    for feat in user.activeFeats:
        if feat == user.activeFeats[len(user.activeFeats) - 1]:
            print(feat, end="")
        else:
            print(feat, end=", ")
    print(colored("\n" + "-"*35, color="magenta"))

def CalculateAttack(user: User):
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

def CheckYorN(prompt: str):
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
    currentUser = User()
    userName = input(colored("\nEnter Username: ", color="light_blue"))
    currentUser.username = userName
    try:
        with open("D&D UsersDB.json", "r") as file:
            all_data = json.load(file)
            LoadUserData(all_data, currentUser)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        with open("D&D UsersDB.json", "w") as file:
            new_entry = [{"Username": currentUser.username, "AttackMod": currentUser.attackModifier, "ProfBonus": currentUser.proficiencyBonus, "AttacksPT": currentUser.numberAttacks, "DamageDiceType": currentUser.damageDieType,"DamageDiceRollAmount": currentUser.damageDieRollAmount, "CritMod": currentUser.critModifier, "ActiveFeats": currentUser.activeFeats}]
            json.dump(new_entry, file, indent=4)
            print(colored("User not found, loading default settings.", color="red"))

    print(colored("\nType help for list of modifiers & commands", color="light_green"))
    while True:
        userInput = input(colored("Enter a command: ", color="light_blue")).strip().lower()
        match userInput:
            case "help":
                print(colored("Commands: ", color="magenta"))
                OutputCommand("calcAttack ", "- Calculate attack")
                OutputCommand("attackMod ", " - Modify attack modifier")
                OutputCommand("profBonus ", " - Modify proficiency bonus")
                OutputCommand("attackPT  ", " - Modify number of attacks per turn")
                OutputCommand("diceType  ", " - Modify damage dice type")
                OutputCommand("diceRoll  ", " - Modify damage dice roll amount")
                OutputCommand("critMod   ", " - Modify crit modifier")
                OutputCommand("feats     ", " - Modify active feats")
                OutputCommand("stats     ", " - Display current stats")
                OutputCommand("save      ", " - Save user data")
                OutputCommand("exit      ", " - Exit the program")
            case "calcattack":
                CalculateAttack(currentUser)
            case "attackmod":
                ModifyAttackMod(currentUser)
            case "profbonus":
                ModifyProfBonus(currentUser)
            case "attackpt":
                ModifyAttackCount(currentUser)
            case "dicetype":
                ModifyDamageDieDamage(currentUser)
            case "critmod":
                ModifyCritMod(currentUser)
            case "feats":
                ModifyActiveFeats(currentUser)
            case "stats":
                DisplayStats(currentUser)
            case "save":
                SaveUserData(currentUser)
            case "exit":
                sys.exit()

def SaveUserData(currentUser: User):
    with open("D&D UsersDB.json", "r+") as file:
            all_data = list(json.load(file))
            for data in all_data:
                if currentUser.username in data.values():
                    all_data.remove(data)
            new_entry = {"Username": currentUser.username, "AttackMod": currentUser.attackModifier, "ProfBonus": currentUser.proficiencyBonus, "AttacksPT": currentUser.numberAttacks, "DamageDiceType": currentUser.damageDieType,"DamageDiceRollAmount": currentUser.damageDieRollAmount, "CritMod": currentUser.critModifier, "ActiveFeats": currentUser.activeFeats},
            all_data.extend(new_entry)
            file.seek(0)
            json.dump(all_data, file, indent=4)
    print(colored("Saved " + currentUser.username + "'s data", color="light_green"))

def LoadUserData(all_data, currentUser: User):
    found = False
    for data in all_data:
        if currentUser.username.lower() in data["Username"].lower():
            found = True
            currentUser.username = data["Username"]
            currentUser.attackModifier = data["AttackMod"]
            currentUser.proficiencyBonus = data["ProfBonus"]
            currentUser.numberAttacks = data["AttacksPT"]
            currentUser.damageDieType = data["DamageDiceType"]
            currentUser.damageDieRollAmount = data["DamageDiceRollAmount"]
            currentUser.critModifier = data["CritMod"]
            currentUser.activeFeats = data["ActiveFeats"]
            print(colored("Loaded " + currentUser.username + "'s data", color="light_green"))
    if not found:
        print(colored("User not found, loading default settings.", color="red"))

if __name__ == "__main__":
    main()
