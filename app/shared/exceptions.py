
from uuid import UUID


class EmailAlreadyExistsException(Exception): 
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email '{email}' already exists in the system")

class UserNotFound(Exception): 
    def __init__(self, id: UUID):
        self.id = id
        super().__init__(f"User with ID '{self.id}' not found")

class InvalidName(Exception): 
    def __init__(self, name:str, restaurant_id: UUID):
        self.name=name
        super().__init__(f"Name '{name}' already exists in the restaurant with ID '{restaurant_id}'")

class DishNotFound(Exception): 
    def __init__(self, id: UUID):
        self.id = id
        super().__init__(f"Dish with ID '{self.id}' not found")

class HoursReservation(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class TableNotFound(Exception):
    def __init__(self, id: UUID):
        self.id = id
        super().__init__(f"Table with ID '{self.id}' not found")

class HourConflict(Exception):
    def __init__(self, message: str):
        super().__init__(message)