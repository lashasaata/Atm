from user import User
import os, json, datetime

class Menu:
    def __init__(self):
        self.__students: dict[str, User] = {}
        self.__read_data()
    
    def file_path(self):
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        file_path = os.path.join(script_dir, "data.json")

        return file_path

    def date(self):
         now = datetime.datetime.now()
         now = now.replace(microsecond=0)

         return now

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

            for id, s in self.__students.items():
                newdata[id] = s.to_dict()

            with open(self.file_path(), mode="w", encoding="utf-8") as file:
                json.dump(newdata, file, indent=4)

    def add_user(self, nik: str, pin: int, balance: float):
        new_user = User(nik, int(pin), float(balance))
        new_user.data = f"Create account at {self.date()}."
        self.__students[str(new_user.id)]= new_user

        try:
            self.__store_db()
            print(f"\nUser {new_user.nik} has successfully added!")

            return str(new_user.id)
        except ValueError:
            print("Account has not added!")

    def check_balance(self, id):
         student = self.__students[id]
         return F"Your balance is {student.balance}."
    
    def withdraw(self, id, amount):
        current = self.__students[id].balance

        if current > amount:
             self.__students[id].balance = current - amount
             self.__students[id].data = f"Withdrawed {amount} lari at {self.date()}"

             self.__store_db()
             print(f"You have got {amount} lari.")
        else:
             print("You have not enough money on your account, chack your balance first!")
    
    def deposit(self, id, amount):
        current = self.__students[id].balance
        self.__students[id].balance = current + amount
        self.__students[id].data = f"Deposit {amount} lari at {self.date()}"

        self.__store_db()
        print("Successful deposit")

    def change_pin(self, id, newpin):
        self.__students[id].data = f"PIN: \"{self.__students[id].pin}\" Has changed into \"{newpin}\" lari at {self.date()}"
        self.__students[id].pin = newpin
        
        self.__store_db()
        print(f"Your PIN has changed into {newpin}.")

    def transfer(self, id1, amount, id2):
        try:
            self.__students[id2]
        except:
             print("User has not found!")
             return
        if amount*102.5/100 > self.__students[id1].balance:
             print("You have not enough money to transfer...")
             return
        else:
             self.__students[id2].balance = self.__students[id2].balance + amount
             self.__students[id1].balance = self.__students[id1].balance - amount*102.5/100

             self.__students[id1].data = f"Transfered {amount} lari + commission fee: {amount*0.025} on user {self.__students[id2].nik}'s account at {self.date()}."
             self.__students[id2].data = f"Transfered {amount} lari from user {self.__students[id1].nik}'s account at {self.date()}."
             self.__store_db()

             print(f"Successfull transfer, Commission fee: {amount*0.025} lari.\nYou have transfered {amount} lari on user \"{self.__students[id2].nik}\"'s account.")
    