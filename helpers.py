class user:
    id: int
    first_name: str
    last_name: str
    house: str

    def __init__(self, id: int, fname: str, lname: str, house: str):
        self.id = id
        self.first_name = fname
        self.last_name = lname
        self.house = house


def find_water_intake(age: int) -> str:
    """Based on the users age, returns the recommended amount of water intake in oz."""
    if age < 4:
        return "16"
    elif age <= 8:
        return "40"
    elif age <= 13: 
        return "56-64"
    elif age <= 18:
        return "64-88"
    else:
        return "72-104"


def find_sleep(age: int) -> str:
    if age < 1:
        return "13-16"
    elif age == 1 or age == 2:
        return "11-14"
    elif age == 3 or age == 4 or age == 5:
        return "10-13"
    elif age >= 6 and age <= 13:
        return "9-12"
    elif age >= 14 and age <= 17:
        return "8-10"
    elif age >= 18 and age <= 64:
        return "7-9"
    else:
        return "7-8"


def doctor_or_not(symptoms: bool) -> bool:
    if symptoms:
        return True
    else: 
        return False
    

def find_house(animal: str) -> str:
    if animal == 'eagle':
        return 'Ravenclaw'
    elif animal == 'lion':
        return 'Gryffindor'
    elif animal == 'badger':
        return 'Hufflepuff'
    else:
        return 'Slytherin'


def covid_result(covid: str) -> str:
    if covid == 'yes':
        return "yes"
    elif covid == 'no':
        return "no"