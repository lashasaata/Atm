class User:
    _id = 1
    def __init__(self, nik, pin, balance=0):
        self.id = User._id
        self.nik = nik
        self.__pin = pin
        self.__balance = balance
        self.__data = []

        User._id += 1

    @property
    def pin(self):
        return self.__pin
    
    @property
    def balance(self):
        return self.__balance
    
    @property
    def data(self):
        return self.__data
    
    @pin.setter
    def pin(self, newpin):
        self.__pin = newpin

    @balance.setter
    def balance(self, newbalance):
        self.__balance = newbalance

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.nik,
            "pin": self.__pin,
            "balance": self.__balance,
            "data": self.__data
        }