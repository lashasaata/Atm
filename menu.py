from user import User
import os, json

class Menu:
    def __init__(self):
        self.__students: dict[str, User] = {}
        self.__read_data()
    
    def file_path(self):
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        file_path = os.path.join(script_dir, "data.json")
        return file_path

    def __read_data(self):
        with open(self.file_path(), mode="r", encoding="utf-8") as file:
            try:
                data = json.load(file)
    
                for id, s in data.items():
                        self.__students[id] = User(s['name'], s['pin'], s['balance'])
            except:
                self.__students = {}
            return data

    def __store_db(self):            
            newdata = {}
            print(self.__students)
            for id, s in self.__students.items():
                newdata[id] = s.to_dict()
            print(newdata)

            with open(self.file_path(), mode="w", encoding="utf-8") as file:
                json.dump(newdata, file, indent=4)

    def add_user(self, nik: str, pin: int, balance: float):
        new_user = User(nik, int(pin), float(balance))
        self.__students[str(new_user.id)]= new_user
        try:
            self.__store_db()
            print(f"User {new_user.nik} has successfully added!")
        except ValueError:
            print("Account has not added!")
        return str(new_user.id)

    def check_balance(self, id):
         student = self.__students[id]
         return F"Your balance is {student.balance}."
    
    def withdraw(self, id, amount):
        current = self.__students[id].balance
        if current > amount:
             self.__students[id].balance = current - amount
             self.__store_db()
             print(f"You have got {amount} lari.")
        else:
             print("You have not enough money on your account, chack your balance first!")
    
    def deposit(self, id, amount):
        current = self.__students[id].balance
        self.__students[id].balance = current + amount

        self.__store_db()
        print("Successful deposit")

    def change_pin(self, id, newpin):
         self.__students[id].pin = newpin

         self.__store_db()
         print(f"Your PIN has changed into {newpin}.")
        
    