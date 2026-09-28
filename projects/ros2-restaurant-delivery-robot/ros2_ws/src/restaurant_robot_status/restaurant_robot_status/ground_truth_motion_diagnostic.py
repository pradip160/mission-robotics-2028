import sys
import json
import math 

previous_x = None
previous_y = None

for line in sys.stdin:
    data = json.loads(line)

    for pose in data["pose"]:
        if pose.get("name") == "restaurant_robot":
            x = pose["position"]["x"]
            y = pose["position"]["y"]

            qx = pose["orientation"].get("x", 0.0)
            qy = pose["orientation"].get("y", 0.0) 
            qz = pose["orientation"].get("z", 0.0) 
            qw = pose["orientation"].get("w", 1.0)

            theta = math.atan2(
                2.0 * (qw * qz + qx * qy),
                1.0 - 2.0 * (qy * qy + qz * qz)
            )

            print("theta:", theta)
            print("x:", x, "y:", y)

            if previous_x is not None: 
                delta_x = x - previous_x
                delta_y = y - previous_y

                print("delta_x:", delta_x , "delta_y:", delta_y)

            previous_x  = x 
            previous_y = y 
