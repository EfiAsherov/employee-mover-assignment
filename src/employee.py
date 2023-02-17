class Employee:
    def __init__(self, name: str, age: int, currency: float = None, cash: float = None, registered_id: int = None) -> None:
        self.name = name
        self.age = age
        self.currency = currency
        self.cash = cash
        self.registered_id = registered_id