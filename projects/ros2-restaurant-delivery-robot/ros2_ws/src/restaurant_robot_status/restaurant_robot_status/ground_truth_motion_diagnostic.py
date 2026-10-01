import sys
import json
import math 

previous_time = None 
previous_x = None
previous_y = None
previous_theta = None 

for line in sys.stdin:
    data = json.loads(line)
   
    stamp = data["header"]["stamp"]

    current_time = (
        float(stamp["sec"])
        + float(stamp.get("nsec", 0)) * 1e-9
    )

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

            if previous_x is not None and previous_time is not None: 
                delta_x = x - previous_x
                delta_y = y - previous_y
                delta_theta = math.atan2(
                    math.sin(theta - previous_theta),
                    math.cos(theta - previous_theta)
                )
                theta_mid = previous_theta + delta_theta / 2.0


                forward = (
                     delta_x * math.cos(theta_mid)
                     + delta_y * math.sin(theta_mid) 
                )
                sideways = ( 
                     -delta_x  * math.sin(theta_mid)
                     + delta_y * math.cos(theta_mid)
                )

                delta_t = current_time - previous_time 

                if delta_t > 0: 
                    forward_velocity = forward / delta_t 
                    sideways_velocity = sideways / delta_t 
                    angular_velocity = delta_theta /delta_t 
 
                    print(
                        "v_forward:", forward_velocity, 
                        "v_sideways:", sideways_velocity,
                        "omega:", angular_velocity
                    )
                print("delta_x:", delta_x , "delta_y:", delta_y)
                print("forward:", forward, "sideways:", sideways)

            previous_x  = x 
            previous_y = y 
            previous_theta = theta
            previous_time = current_time

