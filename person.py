from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name, email, phone):
        self._person_id = None   # Encapsulation: private attribute
        self._name = name
        self._email = email
        self._phone = phone

    @abstractmethod
    def display_details(self):
        """Abstract method to display details of the person"""
        pass

    @abstractmethod
    def generate_id(self):
        """Abstract method to generate a unique ID"""
        pass

    def __str__(self):
        return f"{self._name} ({self._email}, {self._phone})"

    def __repr__(self):
        return f"Person(name={self._name}, email={self._email}, phone={self._phone})"
