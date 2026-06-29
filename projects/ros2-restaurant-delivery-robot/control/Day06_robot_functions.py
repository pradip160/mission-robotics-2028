#Impot time so robot can think for  few secs or minutes 
import time
# Robot startup 
def start_robot():
    print("-----TaroBot delivery-----")
    print("Robot control system starting..")
    print("sensors preparing...")
    print("TaroBot is ready")


# check emerygency stop 

def check_emergency_stop():
    emergency_stop = input("emergency stop  pressed yes/no: ").strip().lower()
 
    if emergency_stop == "yes":
       print("emergency stop warning")
       return True 
     
    else:
       print("emergency system clear")
       return False 


# check battery function
def check_battery():
    battery = int(input("Enter the battery percentage: "))
    
    if battery < 20:
       print("battery low, returning to base")
       return False 
    
    else:
       print("battery safe, continue the mission")
       return True 

# handle obstacle 
def handle_obstacle():
    obstacle = input("Obstacle detected yes/no: ").strip().lower()

    if obstacle == "yes":
       print("Wait and scan again")
       time.sleep(2)
    
       

       path_clear = input("Path become clear yes/no: ").strip().lower()
       if path_clear == "yes":
          print("Continue mission")
          return True
       
       else: 
          print("check alternative route")
          time.sleep(2)
       

          alternative_route = input("alternative route available: ").strip().lower()
          if alternative_route == "yes":
             print("check the alternative route safe or not")
             time.sleep(2)
                
   
             alta_route_safe = input("Is alternative route safe yes/no : ").strip().lower()
             if alta_route_safe == "yes":
                print("Following to the alternative route")
                return True 
         
             else: 
                 print("call the operator")
                 return False
   
          else: 
             print("No alternative route available")
             return False

    else:
       print("Path clear. No obstacle detected.")
       return True

# distane left
def move_robot():
    distance = 0
    distance_left = float(input("Enter distance to destination: "))
    if distance_left == 0:
       print("delivery complete")
       return True


    else:
       print("still on the way")
       return False



# Main robot control flow starts here 
def run_mission():
    start_robot()

    emergency_status = check_emergency_stop()

    if emergency_status == True:
       print("Mission stopped because emergency stop is activate.")

    else:
       battery_safe = check_battery()
  
       if battery_safe == False:
          print("Return to the charging station")
   
       else:
          print("handle obstacle")

          path_safe = handle_obstacle()
          if path_safe == True:
             print("Path is safe moving robot")
      
      
             delivery_complete = move_robot()        
             if delivery_complete == True:
                print("delivery completed")
         
             else:
                print("robot still moving")
         
          else:
             print("Mission paused because no safe path is available")
     

if __name__ == "__main__":
    run_mission()
