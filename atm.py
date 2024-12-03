import json, os
from menu import Menu

class App:
    def __init__(self):
        self.menu = Menu()
        self.commands: dict = {
            "b": self.check_balanse,
            "w": self.withdraw,
            "d": self.deposit,
            "p": self.change_pin,
            "t": self.transfer
        } 

    def comands_menu(self):
        print('==========Atm menu==========\n"X": Exit\n"B": Check balance\n"W": Withdraw\n"D": Deposit\n"P": Change PIN\n"T": Transfer')

        command = input("Chose from menu...").lower()
        while command not in ("x","b","w","i","p","t"):
            command = input("Chose from menu...").lower()
            print()
        
        if command == "x":
            return command
        else:
            self.commands[command]()
        
    def file_path(self):
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        file_path = os.path.join(script_dir, "data.json")

        return file_path
    
    def read_data(self):
        with open(self.file_path(), mode="r", encoding="utf-8") as file:
            data = json.load(file)

        return data
    
    def __valide_pin(self,input_pin):
        input_pin = input_pin.strip()

        if input_pin.isdigit() and len(input_pin) == 4:
            return True
        else:
            print("Invalid PIN.")
            return False

    def __new_account(self):    
        print("\n------------Creating new account------------")

        nik = input("What would be your nickname?: ")
        pin = input("What PIN do you want: ")

        while not self.__valide_pin(pin):
            pin = input("The PIN must be a 4-digit number: ").strip()

        balance = input("What is your starting input: ")

        while not balance.isnumeric():
            balance = input("Balance must be numeric!: ")
        
        self.id = self.menu.add_user(nik, pin, balance)
        print(f"Your ID would be {self.id}, remember it!")

    def __authorization(self):
        data = self.read_data()

        id = input("Enter your id: ")
        while not id.isdigit():
            id = input("Id must be numeric: ")
            
        pin = input("Enter your pin code: ")
        while not self.__valide_pin(pin):
            pin = input("The PIN must be a 4-digit number: ").strip()
            print()
        
        try:
            if data[id] and data[id]["pin"] == int(pin):
                print("successfull authorization...\n")
                self.id = id

                return "Access"
            elif data[id]:
                tries = 2

                while tries > 0:
                    print("Incorrect PIN code!\n")

                    newpin = input("Enter correct pin code: ")

                    while not self.__valide_pin(pin):
                        newpin = input("The PIN must be a 4-digit number: ")
                    
                    if int(newpin) == data[id]["pin"]:
                        print("successfull authorization...\n")
                        self.id = id
                        return "Access"
                    else:
                        tries -= 1
                        continue
                else:
                    print("\nYour card has blocked, go to a bank to update your PIN code!\nHave a nice day...")
                    return "Finish"
        except:
            print()
            print("User has not found!")
            print("============================\n|<= Exit || Create account =>|\n----------------------------")

            next = ""
            while not next.lower() in ("x", "n"):
                next = input("Enter \"X\" to exit, \"N\" to create new account:")

            if next.lower() == "x":
                return "Finish"
            else:
                return "New"
    
    def run(self):
        print("-----------The Atm is running-----------")

        value = self.__authorization()

        if value == "Access" or value == "New":
            if value == "New":
                self.__new_account()

            def rein():
                next = self.comands_menu()

                if next == "x":
                    return print("Process ended...")
                else:
                    return rein()
                
            rein()
        else:
            print("Process ended...")

    def check_balanse(self):
        print("\n---------------Checking balance---------------")

        balance = self.menu.check_balance(self.id)
        return print(balance)
    
    def withdraw(self):
        print("\n---------------withdraw money---------------")

        while True:
            amount = input("Enter withdrawal amount: ")
            try:
                float(amount)
                if float(amount) > 0: break 
                else: print("Deposit money must not negative or 0!")
            except ValueError:
                print("Invalid input. Please enter a number.")

        self.menu.withdraw(self.id, float(amount))

    def deposit(self):
        print("\n---------------deposit money---------------")

        while True:
            amount = input("Enter deposit amount: ")
            try:
                float(amount)
                if float(amount) > 0: break 
                else: print("Deposit money must not negative or 0!")
            except ValueError:
                print("Invalid input. Please enter a number.")

        self.menu.deposit(self.id, float(amount))


    def change_pin(self):
        print("\n---------------Changing PIN---------------")

        newpin = input("Enter new PIN: ")
        while not self.__valide_pin(newpin):
            newpin = input("The PIN must be a 4-digit number: ")
        
        self.menu.change_pin(self.id, newpin)

    def transfer(self):
        print("\n---------------Transfering money---------------")
        print("Transfer commission fee is 2.5%...")

        id = input("Enter the user's id: ")
        while not id.isalnum():
            id = input("The user's id must be numeric: ")

        while True:
            amount = input("Enter transfer amount: ")
            try:
                float(amount)
                if float(amount) > 0: break 
                else: print("Transfer money must not negative or 0!")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
        self.menu.transfer(self.id, float(amount), id)