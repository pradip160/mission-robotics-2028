import math 
import matplotlib.pyplot as plt 

x_hip = 0
z_hip = 0
thigh_length = 0.4  # meters 
shin_length = 0.4  # meters 

hip_angle_in_radians = math.radians(0)
knee_angle_in_radians = math.radians(90)

def forward_kinematics(thigh_length, shin_length, hip_angle, knee_angle):

    knee_x = thigh_length * math.sin(hip_angle)
    knee_z = thigh_length * -math.cos(hip_angle)

    shin_angle = hip_angle + knee_angle
    foot_x  = knee_x + shin_length * math.sin(shin_angle)
    foot_z = knee_z - shin_length * math.cos(shin_angle)

    straight_line_distance = math.sqrt(foot_x**2 + foot_z**2)

    x_positions = [x_hip, knee_x, foot_x]
    z_positions = [z_hip, knee_z, foot_z]

    plt.plot(x_positions, z_positions, marker="o")

    plt.axis("equal")
    plt.show()

    print(hip_angle)
    print(knee_angle)

    print(f"knee_x: {knee_x}, knee_z: {knee_z}")
    print(f"foot_x: {foot_x}, foot_z: {foot_z}")
    print(f"straight_line_distance: {straight_line_distance}")

    print(x_positions)
    print(z_positions)

    return knee_x, knee_z, foot_x, foot_z

knee_x, knee_z, foot_x, foot_z = forward_kinematics(
    thigh_length,
    shin_length,
    hip_angle_in_radians,
    knee_angle_in_radians
)
print(f"Knee Cordinates: ({knee_x:.2f}, {knee_z:.2f}) | Foot Coordinates: ({foot_x:.2f}, {foot_z:.2f})")
