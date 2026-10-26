from two_link_leg import forward_kinematics
import math
import matplotlib.pyplot as plt

x_hip = 0
z_hip = 0

knee_x, knee_z, foot_x, foot_z = forward_kinematics(
    0.4, 0.4, math.radians(0), math.radians(90)
)

x_positions = [x_hip, knee_x, foot_x]
z_positions = [z_hip, knee_z, foot_z]

plt.plot(x_positions, z_positions, marker="o")
plt.axis("equal")
plt.show()
