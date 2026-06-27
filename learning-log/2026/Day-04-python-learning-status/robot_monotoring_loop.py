while True:  
  battery_level = int(input("enter battery level: "))
  obstacle_detected = input("Enter obstacle detected yes/no: ").lower()
  emergency_stop = input("Enter emergency stop yes/no: ").lower()


  if emergency_stop == "yes":
     print("Emergency stop activated")
     break 
     print("Program is still running")

  elif battery_level < 20:
     print("Battery low return to the charging station")
 
  elif obstacle_detected == "yes":
     print("Obstacle detected.stop and wait")
  else: 
     print("Robot is operating normally")

