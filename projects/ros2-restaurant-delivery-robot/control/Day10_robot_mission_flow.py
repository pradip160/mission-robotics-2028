# Day 10: Robot Mission Flow/ State Machine
# Mission Korea Robotics Journey
# Goal: Simulate what happens after the robot choose an order
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
def run_delivery_mission(order):

    if order is None: 
       print("No mission available. Robot remainls IDEL.")
       return 



    mission_history = []

    state = "SELECT_ORDER"
    mission_history.append(state)
    print("=== Robot Delivery Mission Started ===")
    print(f"State: {state}")
    print(f"Selected Order ID: {order['order_id']}")
    print(f"Target Table: {order['table']}")

    state = "MOVING_TO_TABLE"
    mission_history.append(state)
    print(f"State: {state}")
    print(f"Robot is moving to table: {order['table']}...")

    state = "ARRIVED"
    mission_history.append(state)
    print(f"State: {state}")
    print(f"Robot arrived at table {order['table']}.")

    state = "DELIVERED"
    mission_history.append(state)
    order["status"] = "delivered"
    print(f"State: {state}")
    print(f"Order {order['order_id']} delivered successfully.")
    print(f"Updated order status: {order['status']}")
 
    state = "IDLE"
    mission_history.append(state)
    print(f"State: {state}")
    print("Robot is ready for the next mission.")
 
    print("Mission history: ")
    print(mission_history)
    print("Mission path:", " → ".join(mission_history))



    mission_report = {

       "order_id": order["order_id"],
       "table": order["table"],
       "final_status": order["status"],
       "mission_history": mission_history

     }
    return mission_report

    






 
test_order = {
          "order_id": 101,
          "table": 5,
          "item": "ramen",
          "priority": "high", 
          "distance": 4,
          "status": "pending"
           }

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


selected_order = choose_next_order(orders)
mission_result = run_delivery_mission(selected_order)
if mission_result is not None:
   print("=== Mission Report ===")
   print(f"Order ID: {mission_result['order_id']}")
   print(f"Table: {mission_result['table']}")
   print(f"Final Status: {mission_result['final_status']}")
   mission_path = " → ".join(mission_result["mission_history"])
   print(f"Mission Path: {mission_path}")


# Later: Day 9 choose_next_order will provide the selected order.


