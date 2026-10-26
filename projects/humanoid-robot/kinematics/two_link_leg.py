import math 

def forward_kinematics(thigh_length, shin_length, hip_angle, knee_angle):

    knee_x = thigh_length * math.sin(hip_angle)
    knee_z = thigh_length * -math.cos(hip_angle)

    shin_angle = hip_angle + knee_angle

    foot_x  = knee_x + shin_length * math.sin(shin_angle)
    foot_z = knee_z - shin_length * math.cos(shin_angle)

    return knee_x, knee_z, foot_x, foot_z

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


