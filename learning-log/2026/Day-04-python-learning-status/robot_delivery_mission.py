robot_name = input("Enter robot name: ")
battery_level = int(input("Enter battery level: "))
obstacle_detected = input("Enter obstacle detected yes/no: ")
destination_distance = float(input("Enter destination distance: "))

if battery_level < 20:
     print("return to charging station")
elif obstacle_detected == "yes" :
     print("stop and wait")
elif destination_distance <=1:
     print("destination reached")
else:
    print("continue delivery mission")
 
