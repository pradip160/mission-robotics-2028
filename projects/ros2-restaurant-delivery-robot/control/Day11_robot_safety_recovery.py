#battery_percentage =  int(input("Enter the battery percenage: "))
def choose_next_order(orders):
    if not orders:
       return None

    priority_rank = {
       "high": 3,
       "normal": 2,
       "low": 1
       }

    best_order = None
    best_priority = 0
     
    for order in orders:
        print(f"Checking order {order['order_id']} with status {order['status']}")

        if order["status"] in ["delivered", "cancelled"]:
           continue

        current_priority = priority_rank[order["priority"]] 

        if best_order is None:
           best_order = order
           best_priority = current_priority
   
        elif current_priority > best_priority:
             best_order = order
             best_priority = current_priority

        elif current_priority == best_priority and order["distance"] < best_order["distance"]:
             best_order = order
             best_priority = current_priority
      
    return best_order

def yes_no(question):
    while True:
       answer = input(question).strip().lower()
       if answer == "yes" or answer == "y":
          return True

       elif answer == "no" or answer =="n":
          return False


       else:
           print("Invalid answer")
           continue



   
def check_battery(battery_percentage, current_state):


   if battery_percentage <= 10: 
      if current_state == "IDLE":
         next_state = "RETURNING_TO_BASE"
         print("Go to the charging station")
      elif current_state == "WORKING":
         next_state = "WAITING_FOR_OPERATOR"
         print("Alert the operator and go to the safe place.")   


   
   elif 10 < battery_percentage < 20:
          if current_state == "WORKING":    
             next_state = "COMPLETING-CUURENT_ORDER" 
             print("Batter low, finish the current task and return to the charging station")

          elif current_state == "IDLE":
             next_state = "RETURNING_TO_BASE"
             print("Go to the charging station")
  
   elif battery_percentage >= 20:
      if current_state == "WORKING" or current_state == "IDLE":
         next_state = "CONTINUE_MISSION"
         print("Continue the mission")
     
   return next_state


#battery_result = check_battery(battery_percentage, current_state)
#print("Next robot state:", battery_result)

 


def check_obstacle():
    obstacle_detected = yes_no("Enter obstacle detected yes/no: ")
    if obstacle_detected:
       next_state = "CONTINUE_MISSION"
       print("Look for the alternative route")


       alternative_route = yes_no("Enter alternative route available yes/no: ")
       if alternative_route:
          
          print("Check if alternative route is safe or not")
       
       

          safe_route = yes_no("Enter path safety check yes/no: ")
          if safe_route:
             next_state = "REROUTING"
             print("Follow the alternative route")

          else:
             next_state = "WAITING_FOR_OPERATOR"
             print("alert the operator")
  
    else:
       next_state = "CONTINUE MISSION"
     
    return next_state 
          



#obstacle_result = check_obstacle()
#print("obstacle decision:", obstacle_result)


def check_tray_stability():
    tray_stability = yes_no("Enter the tray is stable yes/no: ")
    if tray_stability:
       next_state = "CONTINUE_MISSION"
       print("Ready to service")

    else:
       next_state = "WAITING_FOR_OPERATOR"
       print("Witing for the operator to fix")

    return next_state

#tray_result = check_tray_stability()
#print("Tray stability: ", tray_result)

def run_robot_controller(orders, battery_percentage, current_state):
    mission_history = []
    mission_history.append("SELECT_ORDER")
    selected_order = choose_next_order(orders)
    if selected_order is None: 
       mission_history.append("IDLE")
       print("no active order is available")
       return mission_history


    mission_history.append("SAFETY_CHECK")
    battery_result = check_battery(battery_percentage, current_state)

    mission_history.append(battery_result)
    if battery_result != "CONTINUE_MISSION":
       print("mission cannot start")
       return mission_history


    obstacle_result = check_obstacle()
    mission_history.append(obstacle_result)
    if obstacle_result == "WAITING_FOR_OPERATOR":
       return mission_history

   
    tray_result = check_tray_stability()
    mission_history.append(tray_result)
    if tray_result != "CONTINUE_MISSION":
       print("Mission stopped. Tray is unstable.")
       return mission_history


    mission_history.append("MOVING-TO_TABLE")

    mission_history.append("ARRIVRD")
    mission_history.append("DELIVERED")
    selected_order["status"] = "delivered"
    mission_history.append("IDLE")    
    return mission_history

if __name__ == "__main__":
    orders = [
        {     
        "order_id": 101,
        "table": 5,
        "item": "ramen",
        "priority": "normal",
        "status": "pending",
        "distance": 5
      },
     {
        "order_id": 102,
        "table": 2,
        "item": "sushi",
        "priority": "high",
        "distance": 8,
        "status": "pending"
        },

       {  
        "order_id": 103,
        "table": 7,
        "item": "bibimbap",
        "priority": "high",
        "distance": 3,
        "status": "delivered"

      }
   ]

    current_state = input("What is the current sate: ")
    battery_percentage = int(input("Enter battery percentage: "))

    controller_history = run_robot_controller(
        orders,
        battery_percentage,
        current_state
             )
    print("Controller history:", controller_history)
    print("Updated orders:", orders)
