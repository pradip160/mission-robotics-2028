saftey_score = 100
# lets ask the user  inputs 
robot_name = input("Enter robot name: ")
battery_level = int(input("Enter battery level: "))
food_temperature = int(input("Enter food temperature: "))
obstacle_detected = input("Enter obstacle detected yes/no: ").lower()
distance_to_coustomer = float(input("Enter the distance to coustomer: "))
emergency_stop = input("Emergency stop yes/no: ").lower()

# lets put the logic 
if emergency_stop == "yes":
   saftey_score = saftey_score - 100
   print("Stop immediatly")
   
elif battery_level < 20: 
   saftey_score = saftey_score - 40 
   print("Battery level is low, Return to the charge station")
elif obstacle_detected == "yes":
  saftey_score = saftey_score - 30
  print("Obstacle detected, Stop and Wait")
elif food_temperature < 50:
  saftey_score = saftey_score - 10
  print("Food is gettig cold. Deliver quickly")
elif distance_to_coustomer <= 5:
  saftey_score = saftey_score - 10
  print("Coustomer reached. Deliver food")
else: 
  print("Continue delevery mission")


print("Expected risk: " , saftey_score)




if saftey_score >= 80:
   print("Safe mission")
elif saftey_score >= 50:
   print("Medium risk")
else:
   print("High risk mission")
