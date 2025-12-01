
# Import necessary modules from the Hub SDK
from hub import port
import runloop
import motor_pair
import motor
from hub import motion_sensor


def forward(number):
    return number


def backward(number):
    return -number


async def move_motor_forward(degrees: int, speed: int) -> None:
    """Move motor on port.C forward for specified degrees at given speed"""
    await motor.run_for_degrees(port.C, degrees, speed)


async def move_motor_backward(degrees: int, speed: int) -> None:
    """Move motor on port.C backward for specified degrees at given speed"""
    await motor.run_for_degrees(port.C, -degrees, speed)


async def move_pair_forward(degrees: int, steering: int, velocity: int) -> None:
    """Move motor pair PAIR_1 forward for specified degrees"""
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degrees, steering, velocity=velocity)


async def move_pair_backward(degrees: int, steering: int, velocity: int) -> None:
    """Move motor pair PAIR_1 backward for specified degrees"""
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -degrees, steering, velocity=velocity)


async def move_pair_tank_forward(left_speed: int, right_speed: int, degrees: int) -> None:
    """Move motor pair PAIR_1 in tank mode forward for specified degrees"""
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, left_speed, right_speed, degrees)


async def move_pair_tank_backward(left_speed: int, right_speed: int, degrees: int) -> None:
    """Move motor pair PAIR_1 in tank mode backward for specified degrees"""
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -left_speed, -right_speed, degrees)


async def move_straight_for_degrees(degrees: int, speed: int) -> None:
    # motor_pair.pair(motor_pair.PAIR_1, left_motor, right_motor)

    motor.reset_relative_position(port.F, 0)
    motor.reset_relative_position(port.E, 0)
    # Reset the yaw angle to zero and wait for stabilization
    motion_sensor.reset_yaw(0)
    # await runloop.until(motion_sensor.stable)

    # Set the target angle (0 degrees for straight movement)
    target_angle = 0

    # Define the proportional gain for correction
    Kp = 0.08# 1# Adjust this value based on your robot's behavior

    # Loop to maintain straight movement

    while (abs(motor.relative_position(port.F))) < abs(degrees):
        # Get the current yaw angle
        current_angle = motion_sensor.tilt_angles()[0]
        # Calculate the error
        error = target_angle - current_angle# Corrected to target - current
        # Calculate the correction
        correction = int(Kp * error)
        # Adjust the motor speeds to apply correction for straight movement
        left_speed = speed + int(correction)
        right_speed = speed - int(correction)
        # Move the robot with corrected motor speeds
        motor_pair.move_tank(motor_pair.PAIR_1, left_speed, right_speed)
        # Small delay for stability
        await runloop.sleep_ms(10)
    # Stop the motors after the loop
    motor_pair.stop(motor_pair.PAIR_1)

    # You run the normal move_for_degrees function.
    ## CODE STARTS HERE


async def main():
    left_motor = port.F
    right_motor = port.E
    motor_pair.pair(motor_pair.PAIR_1, left_motor, right_motor)# pairing motors
    # left side second black line from the left
    await move_pair_backward(5, 0, 700)# alignment by pusing backwards

    # move forward towards silo
    await move_straight_for_degrees(907, 600)  # Go to silo

    # move arm thrice to take the gears out of the silo
    await move_motor_forward(170, 1000)# forward to hit lever
    await move_motor_backward(165, 1000)# backward
    await move_pair_tank_backward(5, 0, 600)# When the attactchment hits, turns bot- conteracts turn
    await move_motor_forward(165, 1000)# forward
    await move_pair_tank_backward(5, 0, 600)# When the attactchment hits, turns bot- conteracts turn
    await move_motor_backward(165, 1000)# backward
    await move_motor_forward(165, 1000)# forward
    await move_motor_backward(165, 1000)# backward

    await move_pair_tank_backward(5, 0, 600)# When the attactchment hits, turns bot- conteracts turn
    await move_motor_forward(165, 1000)# forward

    await move_motor_backward(165, 1000)# backward

    await move_motor_forward(130, 500)# forward

    await move_pair_tank_forward(35, 0, 250)# turn so the attatchment can do the Forge mission

    # Go to forge
    await move_pair_forward(650, 0, 500)# move forward so the wheelcan hit the stick to let the balls out

    await move_motor_backward(350, 500)# backward arm to make sure it does not get in the way

    await move_pair_backward(180, 0, 700)# go backward to be able to do the
    await move_pair_tank_forward(270, 0, 600)# first turn to turn toward mission
    await move_pair_forward(400, 0, 400)# go forward to the mission
    await move_pair_tank_forward(70, 0, 600)# second turn to turn toward mission
    await move_pair_backward(200, 0, 500)  # push back to complete mission
    await move_straight_for_degrees(450, 550)  # go forward to be able to turn to do whats on sale
    await move_pair_tank_forward(360, 0, 500)  # turn to whats on sale

    await move_motor_forward(160, 1000)# tip the scales

    # move back
    await move_pair_backward(60, 0, 400)# go back out of tip the scales
    await move_pair_tank_backward(505, 0, 600)# turn towards base
    await move_pair_backward(700, 0, 800)# go to base

    await move_pair_tank_backward(180, 0, 600)# turn towards base
    await move_pair_backward(1000, 0, 800)# go to base


runloop.run(main())
