from typing import TypedDict

class Person(TypedDict):
    name : str
    age : int
    
new_person_1: Person = {'name': 'Aman', 'age': 35}

# this is also allowed, will not create an error
new_person_2: Person = {'name': 'Aman', 'age': '35'}
new_person_3: Person = {'name': 'Aman', 'age': 'Thirty Five'}

print(new_person_1)
print(new_person_2)
print(new_person_3)