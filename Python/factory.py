from typing import Type

class Pet:
    def __init__(self,name):
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError
    

class Dog(Pet):
    def speak(self):
        return "Au"
    
class Cat(Pet):
    def speak(self):
        return "Miau"
    

def create_pet(pet_class: Type[Pet], name: str) -> Pet:
    return pet_class(name)