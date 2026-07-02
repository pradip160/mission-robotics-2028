# Day 8 : Robot Order Data 
# Lists and dictionaries for restaurant delivery  robot mission queue

def create_order(order_id, table_number, food_item, distance, priority, status):
    order = {
        "order_id": order_id,  
        "table_number": table_number,
        "food_item": food_item,
        "distance": distance,
        "priority": priority,
        "status": status
           }
  
    return order

def add_order(orders,order):
    orders.append(order)



def display_order(order):
       
    print("Order ID:", order["order_id"])
    print("Table:", order["table_number"])
    print("Food:", order["food_item"])
    print("Distance:", order["distance"], "meters")
    print("Priority:", order["priority"])
    print("Status:",order["status"])
    print("----------------------------")


def display_order_queue(orders):
    print("Robot Order Queue")
    print("------------------")

    for order in orders:
        display_order(order)
    


def update_order_status(orders, target_order_id,new_status):
    for order in orders:
        if order["order_id"] == target_order_id:
           order ["status"] = new_status
           print("Order", target_order_id, "status update to",new_status) 
           return


    print("Order not  found")



def count_order_status(orders):
     status_counts = {}

     for order in orders:
         status = order["status"]

         if status not in status_counts:
            status_counts[status] = 0

         status_counts[status] = status_counts[status] + 1

     print("Mission Summary")

     for status in status_counts:
         print(status,"orders:", status_counts[status])

    
# Main robot program starts here 

orders = []
order1 = create_order(1,3,"noodles", 7, "high", "pending")
order2 = create_order(2,5,"burger", 4, "normal", "pending")
order3 = create_order(3,1,"coffee", 2, "low", "pending")
add_order(orders,order1)
add_order(orders,order2)
add_order(orders,order3)


display_order_queue(orders)
update_order_status(orders,1, "delivered")
update_order_status(orders,2, "packing")
display_order_queue(orders)
count_order_status(orders)
