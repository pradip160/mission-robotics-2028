import sys
import json

for line in sys.stdin:
    data = json.loads(line)

    for pose in data["pose"]:
        if pose.get("name") == "restaurant_robot":
            x = pose["position"]["x"]
            y = pose["position"]["y"]

            print("x:", x, "y:", y)
