# Day 5 : Robot Monotoring Loop 
# Goal : Keep checking robot status again and again using while loop 

# Robot thinking:
# While mission is running:
#     check battery
#     check obstacle 
#     check distance 
#     check emergency stop 
#     decide whether to continue or stop 


# Today's levels:
# 1. Simple While loop 
# 2. Stop loop using user input 
# 3. Add emergency stop 
# 4. Add battery and obstacke check 
# 5. Count delivires 

import time 
delivery_count= 0
mission_running = True

while mission_running:
     print("Robot checking the status")
     emergency_stop = input("Emergency stop yes/no: ").strip().lower()
 
     if  emergency_stop == "yes":
         print("Stop the mission immediately")
         break 
      
     if emergency_stop not in ["yes","no"]:
         print("Invalid emergency input. Robot stopping for saftey.")
         break

     
     battery_level = int(input("Enter the battery levl: "))
     if battery_level < 20:
         print("battery low. Going back to the charging station")
         break  

    
      
     obstacle = input("Enter obstacle yes/no: ").strip().lower()
     if obstacle == "yes":
       print("Obstacle detected. Robot waiting and scanning again.")
       time.sleep(3)
       
       obstacle_cleared = input("Enter is obstacle cleared yes/no: ")
       
       if obstacle_cleared == "yes":
          print("Obstacle cleared contuning mission")
       else:
           alternative_root = input("alternative root available? yes/no: ")
           
           if alternative_root == "yes":
              print("Changing root")
           else:
              print("mission paused call the operator")
              break

     if obstacle not in ["yes", "no"]:
        print("invalid obstacle input, Robot stopping for saftey.")
        break 
     distance = int(input("Enter distance: ")) 
     if distance < 2:
       print("Reached the destenation")
       break
       

     
     mission = input("Continue mission yes/no: ").strip().lower() 
     if mission == "no":
          print("mission stopped")
          break

     else:
         print("Continue misson safely")
         delivery_count = delivery_count + 1
         print("Total delivery count: ", delivery_count)
