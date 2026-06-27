mission_score  = 100
robot_name = input("Enter robot name: ")
battery_level = int(input("Enter battery level: "))
obstacle_detected = input("Enter obstacle dected yes/no: ").lower()
robot_speed = float(input("Enter robot speed: "))
emergency_stop = input("emergency stop yes/no: ").lower()
destination_distance  = float(input("Destination distance: "))


if emergency_stop == "yes":
   mission_score = mission_score - 100
if battery_level <=15:
   mission_score = mission_score - 50
if obstacle_detected == "yes":
   mission_score = mission_score - 30
if destination_distance <= 1:
   print("Destination reached")
if robot_speed > 2:
   mission_score = mission_score - 20



print("Mission Safety Score: ", mission_score)


if mission_score >= 80:
     print("Mission status: Safe")
elif mission_score >= 50:
     print("Mission status : Medium risk")
else:
     print("Mission status: High risk")
