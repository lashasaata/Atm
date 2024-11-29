import concurrent.futures
import json, os
import concurrent

class Atm:
    id = 1
    def __init__(self, user, password):
        self.id = Atm.id
        self.__balance = 0
        self.user = user
        self.__pin = password

        Atm.id += 1

    def check_balanse(self):
        return print(f"Your balance is: {self.__balance}")
    
    def checkout(self, password, amount):
        pass

def valide_pin(input_text):
    try:
        int(input_text)
        if len(input_text) == 4:
            return True
        else:
            return False
    except:
        print("Invalid pin")
        return False
    
def asyn(obj, id, pin):
    print(type(obj["id"]), type(id))
    if obj["id"] == id and obj["pin"] == pin:
        return 2
    elif obj["id"] == id: 
        return 1
    else: 
        return 0

def authorization(data):
    id = input("Enter your id: ")
    pin = input("Enter your pin code: ")

    while not valide_pin(pin):
        pin = input("The PIN must be a 4-digit number: ")
    

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda obj: asyn(obj, int(id), int(pin)), data))
    
    if 2 in results:
        print("successfull authorization...\n")
        return
    elif 1 in results:
        tries = 2
        index = results.index(1)
        while tries > 0:
            print("Incorrect PIN code!")

            newpin = input("Enter your pin code: ")

            while not valide_pin(pin):
                newpin = input("The PIN must be a 4-digit number: ")
            
            if int(newpin) == data[index]["pin"]:
                print("successfull authorization...\n")
                return
            else:
                tries -= 1
                continue
        else: 
            print("Your card has blocked, go to a bank to update your PIN code!\nHave a nice day...")
            return
    else:
        print("User has not found!")



    

def atm():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    file_path = os.path.join(script_dir, "data.json")

    print("Wellcome!")

    with open(file_path, mode="r", encoding="utf-8") as file:
        data = json.load(file)

    authorization(data)

    

            


atm()
# Atm("lasha", 4747).check_balanse()
