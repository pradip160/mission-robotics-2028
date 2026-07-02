def choose_next_order(orders):
    priority_rank = {
           "high": 3,
           "normal": 2,
           "low": 1
     } 

    best_order = None

    for order in orders:
        order_status = order["status"]
 
        if order_status == "delivered" or order_status == "cancelled":
           continue 
 
        if best_order is None:  
           best_order = order

        else:
           current_priority = priority_rank[order["priority"]]
           best_priority = priority_rank[best_order["priority"]]

           if current_priority > best_priority:
              best_order = order
         
           elif current_priority == best_priority:
                current_distance = order["distance"]
                best_distance = best_order["distance"]
              
                if current_distance < best_distance:
                   best_order = order
   
    return best_order
   

orders = [
       {
              "order_id": 1,
              "table": 3,
              "status": "delivered",
              "priority": "normal",
              "distance": 8
        },
          {   
              "order_id": 2,
              "table": 3,
              "status": "pending",
              "priority": "high",
              "distance": 2
           },
          {
              "order_id": 3,
              "table": 1,
              "status": "cancelled",
              "priority": "high",
              "distance": 4
            }
         ]
next_order = choose_next_order(orders)

if next_order is not None:
   print("Robot should deliver this order next:")
   print("Order ID:", next_order["order_id"])
   print("Table:", next_order["table"])
   print("Priority:", next_order["priority"])
   print("Status:", next_order["status"])             
else:
   print("No active orders available for delivery.")
