from two_link_leg import forward_kinematics, inverse_kinematics  
import math 

x_hip = 0
z_hip = 0
thigh_length = 0.4
shin_length = 0.4

hip_angle_in_radians = math.radians(0)
knee_angle_in_radians = math.radians(90)

def test_straight_leg():

    straight_knee_x, straight_knee_z, straight_foot_x, straight_foot_z = forward_kinematics(
        0.4,
        0.4,
        0,
        0
    )
    assert math.isclose(straight_foot_x, 0, abs_tol=1e-9)
    assert math.isclose(straight_foot_z, -0.8, abs_tol=1e-9)

def test_unequal_leg():

    unequal_knee_x, unequal_knee_z, unequal_foot_x, unequal_foot_z = forward_kinematics(
        0.5,
        0.3,
        math.radians(0),
        math.radians(90)
    )

    assert math.isclose(unequal_foot_x, 0.3, abs_tol=1e-9)
    assert math.isclose(unequal_foot_z, -0.5, abs_tol=1e-9)

def test_invalid_link_lengths(): 

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
    
def test_maximum_reach(): 

    maximum_reach_result = inverse_kinematics(
        0.5,
        0.3,
        0.0,
        -0.8
    )
    assert maximum_reach_result is not None  
  
def test_minimum_reach(): 

    minimum_reach_result = inverse_kinematics(
        0.5,
        0.3,
        0.0,
        -0.2
    )

    assert minimum_reach_result is None 

def test_unreachable_target(): 

    unreachable_target = inverse_kinematics(
        0.5,
        0.3,
        1.0,
        0.0
    )
    assert unreachable_target is None 

def test_ik_fk_consistency():

    angles = inverse_kinematics(
        0.5,
        0.3,
        0.3,
        -0.4
    )
    assert angles is not None 
    hip_angle, knee_angle = angles 

    verified_knee_x, verified_knee_z, verified_foot_x, verified_foot_z = forward_kinematics(
        0.5,
        0.3,
        hip_angle,
        knee_angle
    )

    assert math.isclose(verified_foot_x, 0.3, abs_tol=1e-9)
    assert math.isclose(verified_foot_z, -0.4, abs_tol=1e-9)
    assert angles is not None

def test_link_lengths():

    hip_angle_in_radians = math.radians(0)
    knee_angle_in_radians = math.radians(90)

    x_hip = 0
    z_hip = 0
    thigh_length = 0.4
    shin_length = 0.4

    hip_angle_in_radians = math.radians(0)
    knee_angle_in_radians = math.radians(90)



    knee_x, knee_z, foot_x, foot_z = forward_kinematics(
        thigh_length,
        shin_length,
        hip_angle_in_radians,
        knee_angle_in_radians
    )

    calculated_thigh_length = math.sqrt((knee_x - x_hip)**2 + (knee_z - z_hip)**2)
    calculated_shin_length = math.sqrt((foot_x - knee_x)**2 + (foot_z - knee_z)**2)

    straight_line_distance = math.sqrt(foot_x**2 + foot_z**2)

    assert math.isclose(calculated_thigh_length, thigh_length, abs_tol=1e-9)
    assert math.isclose(calculated_shin_length, shin_length, abs_tol=1e-9)
    assert math.isclose(foot_x, 0.4, abs_tol=1e-9)
    assert math.isclose(foot_z, -0.4, abs_tol=1e-9)



