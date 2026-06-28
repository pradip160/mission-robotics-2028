# Day 5: Resturdent Delivery Robot Monitoring System
# Mission Korea Robotics Journey (2026)

#  Goal: 
# Simulation a restautant delivery robot that continuously
# monitors its enviroment while delivering food. 

# Robot Monitoring Order:
# 1. Emergency stop 
# 2. Battery Status 
# 3. Obstacle Detection
# 4. Distance to Destination 
# 5. Mission Decision 
# 6. Delivery Counter 

# Notes:
# Sensor value are entered manually for learning purposes.
# Later in ROS2 these values will come from robot sensors. 




import time 

# Robot mission variables
# robot_name stores the robot identity
# delivery_count tracks sucessfull safe delivery cycles
robot_name = "TaroBot"
delivery_count = 0

# Start robot startup sequence 
# In a real robot, these would be separate ROS2 nodes/modules becoming ready

print("Korea bot system starting....")
time.sleep(1)
print("Navigation system: ready")
print("Battery system: ready")
print("Obstacle detection system: ready")
print("Robot ready for restaurant service")

# Main robot monotoring loop 
# The robot keeps checking saftey conditions during the delivery mission.
# The loop stops only when a critical saftey happens.
while True: 
   print("\n----Mission Monitoring Cycle-----")
   print("Checking robot saftey systems..")


   # Emergency stop check 
   emergency_stop =  input("Emergency stop yes/no:").strip().lower()
   if emergency_stop =="yes":
      print("Stop danger detected aborting mission")
      # This has highest pirority because the robot must stop immediatelt in danger")
      break 

   # Battery saftey check
   # If battery is too low, the robot should return to charging station.
   battery = int(input("Checking battery level: "))
   if battery < 15:
      print("Battery low, Going to the charging station")
      break
 
   # Obstacel check 
   #  If there is obstacle, the robot should stop and wait and check for the altrnative route
   route_status = "normal route" 
   obstacle = input("obstacle detected yes/no: ").strip().lower()
   if obstacle == "yes":
      print("Obstacle detected.")
      print("Robot stopping motors")
      print("Robot waiting and scanning again.")
      time.sleep(3)

      obstacle_cleared = input("obstacle cleared yes/no: ").strip().lower()
      if obstacle_cleared == "yes":
         print("Path cleared, followig the mission.")
         route_status = "obstacle_cleared"
         time.sleep(3)

      else:
         # if still the obstacle not cleared the robot should look for alternative direction
           alternative_route = input("alternative route available yes/no: ").strip().lower()
           if alternative_route == "yes":
              print("Alternative route selected.")
              print("Robot recalculating path and continuing mission.")
              route_status = "alternative route" 
           else:
              print("No saftey route available")
              print("Mission paused,calling  the operator")
              break 
 
      # Adding distance to track where our robot is
   distance = int(input("How much distance left: "))
   # Distance should be 0 otherwise the robot direct goes to else
   if distance == 0:
       print("hello here is you food, enjoy")
       status = input("delivery status complete/progess: ").strip().lower()
       if status == "complete":
          print("food deliverd, returning to the base")
          delivery_count = delivery_count + 1
          print("Total delivery count:" , delivery_count)
          print("Robot returning to the base.")
          time.sleep(2)
          print("Ready for another service.")
   
       else:
          print("Mission still in progess.")
         
         # robot should update its status after sucessfully delivery the food
         # so we going to add the status 

   else:
       print("Robot is still moving toward the destination....")
       distance = distance - 1 
       print("Update distance left: ",  distance)
       
       if distance == 0:
          print("Destinaton reched")
       else:
          print("Mission still in progess. continuing monitoring cycle.")
       
       continue
    
