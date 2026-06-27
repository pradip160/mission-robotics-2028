robot_name = input("Enter robot name: ")
battery_level = int(input("Enter battery level: "))
obstacle_detected = input("Enter obstacle dected yes/no: ").lower()
robot_speed = float(input("Enter robot speed: "))
emergency_stop = input("emergency stop yes/no: ").lower()
destination_distance  = float(input("Destination distance: "))


if emergency_stop == "yes":
   print("Stop immediately")
elif battery_level <=15:
   print("Return to charging station")
elif obstacle_detected == "yes":
   print("Stop and wait")
elif destination_distance <= 1:
   print("Destination reached")
elif robot_speed > 2:
   print("slow down")
else:
   print("continue delivery mission")
