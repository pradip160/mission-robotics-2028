robot_name = input("Enter Robot name: ")
battery_level = int(input("Enter battery level: "))

if battery_level < 20:
   print("Return to charging station")
elif battery_level <= 60:
   print("Continue carefully")
else:
   print("Continue mission")

