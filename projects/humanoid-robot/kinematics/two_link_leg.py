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

def inverse_kinematics(thigh_length, shin_length, target_x, target_z):

    if thigh_length <= 0 or shin_length <=0: 
        return None 

    distance = math.sqrt((target_x)**2 + (target_z)**2)
    distance_minimum = abs(thigh_length - shin_length)
    distance_maximum = thigh_length + shin_length 

    is_reachable = distance_minimum <= distance <= distance_maximum 

    if not is_reachable: 
        return None 
    else: 
        numerator = distance**2 - thigh_length**2 - shin_length**2 
        denominator = 2 * (thigh_length * shin_length)

    cos_knee = max(-1.0, min(1.0, numerator / denominator))
    knee_angle = math.acos(cos_knee)

    if knee_angle > math.radians(135):
        return None 

    target_direction = math.atan2(target_x, - target_z)
    angular_difference = math.atan2(shin_length * math.sin(knee_angle), thigh_length + shin_length * math.cos(knee_angle))
    hip_angle =  target_direction - angular_difference 

    return hip_angle,knee_angle  


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

ik_knee_x, ik_knee_z, ik_foot_x, ik_foot_z = forward_kinematics(
    0.5,
    0.3,
    math.radians(1.954691398399838),
    math.radians(107.4576031237221)
)

assert math.isclose(ik_foot_x, 0.3, abs_tol=1e-9)
assert math.isclose(ik_foot_z, -0.4, abs_tol=1e-9)

ik_hip_angle, ik_knee_angle = inverse_kinematics( 
    0.5,
    0.3, 
    0.3,
    -0.4
)

verified_knee_x, verified_knee_z, verified_foot_x, verified_foot_z = forward_kinematics(
    0.5,
    0.3,
    ik_hip_angle,
    ik_knee_angle
)

assert math.isclose(verified_foot_x, 0.3, abs_tol=1e-9)
assert math.isclose(verified_foot_z, -0.4, abs_tol=1e-9)

result = inverse_kinematics(
    0.5,
    0.3,
    0.3,
    -0.4
)
if result is None: 
    print("Target unreachable.")
else:
    hip_angle, knee_angle = result 
    print("Target reachable.joint angles calculated.")


invalid_result = inverse_kinematics(
    0.0,
    0.3,
    0.0,
    -0.3
)

assert invalid_result is None

invalid_result_2 = inverse_kinematics(
    0.5,
    0.0,
    0.0,
    -0.5
)

assert invalid_result_2 is None

invalid_result_3 = inverse_kinematics(
    -0.5,
    0.3,
    0.0,
    -0.3
)

assert invalid_result_3 is None 

maximum_reach_result = inverse_kinematics(
    0.5,
    0.3,
    0.0,
    -0.8
)

minimum_reach_result = inverse_kinematics(
    0.5,
    0.3,
    0.0,
    -0.2
)

assert minimum_reach_result is None 

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
print(f"IK verification: ({ik_foot_x}, {ik_foot_z})")
print(f"Hip_Angle: {math.degrees(ik_hip_angle):2f}")
print(f"knee_angle: {math.degrees(ik_knee_angle):2f}")
print(f"Result : {result}")
print(f"Maximum reach result: {maximum_reach_result}")
print(f"Minimum reach result: {minimum_reach_result}")

plt.show()

