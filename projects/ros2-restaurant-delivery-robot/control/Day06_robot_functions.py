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
    emergency_stop = get_yes_no("emergency stop  pressed yes/no: ")
 
    if emergency_stop == True:
       print("emergency stop warning")
       return True 
     
    else:
       print("emergency system clear")
       return False 


# check battery function
def check_battery():
  while True:
    battery_status = input("Enter the battery percentage: ").strip()

    if not battery_status.isdigit():
       print("Invalid battery reading")
       continue
    
    battery = int(battery_status)
    if battery > 100: 
       print("Invalid battery  range, please try again")
       continue 


    if battery < 20:
       print("Battery unsafe, returning to the base")
       return False

    
    else:
       print("battery safe, continue the mission")
       return True 


    

# handle obstacle 
def handle_obstacle():
    obstacle = get_yes_no("Obstacle detected yes/no: ")

    if obstacle == True:
       print("Wait and scan again")
       time.sleep(2)
    
       

       path_clear = get_yes_no("Path become clear yes/no: ")
       if path_clear == True:
          print("Continue mission")
          return True
       
       else: 
          print("check alternative route")
          time.sleep(2)
       

          alternative_route = get_yes_no("alternative route available yes/no: ")
          if alternative_route == True:
             print("check the alternative route safe or not")
             time.sleep(2)
                
   
             alta_route_safe = get_yes_no("Is alternative route safe yes/no : ")
             if alta_route_safe == True:
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
  while True:
    distance = input("Enter the distance to destination: ").strip().lower()
    distance_left = float(distance)
    



    if distance_left < 0:
       print("Invalid distance rage")
       continue 

    if distance_left == 0:
       return True

    if distance_left > 0:
       print("robot still moving toward destination")
       continue




# lets define yes_no
def get_yes_no(question):
    while True: 
       
      answer = input(question).strip().lower()
      
      if answer == "yes" or answer == "y":
         print("Answer type is valid")
         return True

      elif answer == "no" or answer == "n":
         print("Answer type is valid")
         return False

     
      else:
         print("Answer is invalid and ask again")
         continue

# lets creat reusable helper for float numbers.


def get_float(question):
   while True: 
     
       number = input(question).strip()
      
       try:
          float_number = float(number)
          return float_number 
   
       except:
          print("Invalid number reading")
          continue
      


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
