# Day 1 Python Practice 
# Mistake note:
# I first crearted separate file as day1.py, day2.py, and day3.py 
# Later I learned how to combine them into one Day-01 practice file. 


name = "Pradip"
country =  "Nepal"
current_place = "UK"
goal = "Robotic Master in South Korea"

print("My name is: ", name)
print("I am from: ", country)
print("I currently live at  : ", current_place)
print("My goal is : ", goal)



name = input("What is your  name?" )
country  = input("Where are you from?" )
goal =  input("What is your goal? " )

print("---------- My Mission Profile -------------")
print("Name:", name) 
print("Country: " , country)
print("Goal: " , goal)
print("I am preparing for my mssion korea 2028")
name = input("What is your name?")
age = input("How old are you?")
target_year = input("In which year you want to go korea")

age = int(age)
target_year = int(target_year)
future_age = age + (target_year -  2026)
print("------Mission korea age calculator---")
print("Name: ",name)
print("Current age: ", age)
print("Target age: " ,target_year)
print("Future age : ", future_age)
