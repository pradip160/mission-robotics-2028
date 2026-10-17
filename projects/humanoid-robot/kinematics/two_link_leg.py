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

    return knee_x, knee_z, foot_x, foot_z



knee_x, knee_z, foot_x, foot_z = forward_kinematics(
    thigh_length,
    shin_length,
    hip_angle_in_radians,
    knee_angle_in_radians
)

calculated_thigh_length = math.sqrt((knee_x - x_hip)**2 + (knee_z - z_hip)**2)
calculated_shin_length = math.sqrt((foot_x - knee_x)**2 + (foot_z - knee_z)**2)

assert math.isclose(calculated_thigh_length, thigh_length, abs_tol=1e-9)
assert math.isclose(calculated_shin_length, shin_length, abs_tol=1e-9)
assert math.isclose(foot_x, 0.4, abs_tol=1e-9)
assert math.isclose(foot_z, -0.4, abs_tol=1e-9)


straight_knee_x, straight_knee_z, straight_foot_x, straight_foot_z = forward_kinematics(
    thigh_length,
    shin_length,
    math.radians(0),
    math.radians(0)
)

assert math.isclose(straight_foot_x, 0, abs_tol=1e-9)
assert math.isclose(straight_foot_z, -0.8, abs_tol=1e-9)

unequal_knee_x, unequal_knee_z, unequal_foot_x, unequal_foot_z = forward_kinematics(
    0.5,
    0.3,
    math.radians(0),
    math.radians(90)
)

assert math.isclose(unequal_foot_x, 0.3, abs_tol=1e-9)
assert math.isclose(unequal_foot_z, -0.5, abs_tol=1e-9)

x_positions = [x_hip, knee_x, foot_x]
z_positions = [z_hip, knee_z, foot_z]

straight_line_distance = math.sqrt(foot_x**2 + foot_z**2)

plt.plot(x_positions, z_positions, marker="o")
plt.axis("equal")

print(f"Knee Cordinates: ({knee_x:.2f}, {knee_z:.2f}) | Foot Coordinates: ({foot_x:.2f}, {foot_z:.2f})")
print(f"hip_angle_in_radians: {hip_angle_in_radians}")
print(f"knee_angle_in_radians: {knee_angle_in_radians}")
print(f"Calculated thigh length: {calculated_thigh_length}")
print(f"knee_x: {knee_x}, knee_z: {knee_z}")
print(f"foot_x: {foot_x}, foot_z: {foot_z}")
print(f"straight_line_distance: {straight_line_distance}")
print(f"straight_foot_x: {straight_foot_x}, straight_foot_z: {straight_foot_z}")
print(f"Unequal leg foot: ({unequal_foot_x}, {unequal_foot_z})")

plt.show()

