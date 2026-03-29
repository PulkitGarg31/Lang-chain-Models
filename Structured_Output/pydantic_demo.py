from pydantic import BaseModel,EmailStr,Field

from typing import Optional

class Student(BaseModel):
    name : str
    age : Optional[int] = None
    email : Optional[EmailStr] = None
    cgpa : Optional[float] = Field(default=None,gt = 0, lt = 10,description='Field representing CGPA of student')
    
# EmailStr check the format of email
# This will work fine
new_student_1  = {'name':'Pulkit', 'age':32, 'email':'abc@check.com','cgpa':8.5}
new_student_2  = {'name':'Pulkit', 'age':'32'}

# This will raise an error
# new_student_3  = {'name':'Pulkit', 'age':'Thirty Five'}

student_1 = Student(**new_student_1)
student_2 = Student(**new_student_2)
# student_3 = Student(**new_student_3)

print(student_1)
#can be converting in dict also
print(dict(student_2))
# print(student_3)