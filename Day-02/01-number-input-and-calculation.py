#  Lets try to solve the robort batter  duration 
robot_name = input("Enter Robot name")
battery_percentage = int(input("How much battery percentage left"))
battery_usage_per_minutes = int(input("How much battery usages per minutes"))


if battery_usage_per_minutes == 0:
    print("Error: battery usages cannot be zero.")
else:
    battery_duration =  battery_percentage / battery_usage_per_minutes
    print(robot_name, "can run for" , battery_duration, "minutes")


if battery_percentage < 20:
    print("Warning: Battery low Return to charging station.")
else:
    print("Battery level is okay. Continue mission.")


