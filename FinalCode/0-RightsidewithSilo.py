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


async def move_straight_for_degrees(left_motor: int, right_motor: int, degrees: int, speed: int) -> None:
    # motor_pair.pair(motor_pair.PAIR_1, left_motor, right_motor)

    motor.reset_relative_position(left_motor, 0)
    motor.reset_relative_position(right_motor, 0)
    # Reset the yaw angle to zero and wait for stabilization
    motion_sensor.reset_yaw(0)
    # await runloop.until(motion_sensor.stable)

    # Set the target angle (0 degrees for straight movement)
    target_angle = 0

    # Define the proportional gain for correction
    Kp = 0.08  # 1# Adjust this value based on your robot's behavior

    # Loop to maintain straight movement

    while (abs(motor.relative_position(left_motor))) < abs(degrees):
        # Get the current yaw angle
        current_angle = motion_sensor.tilt_angles()[0]
        # Calculate the error
        error = target_angle - current_angle  # Corrected to target - current
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
    right_motor_port = port.C  # MAkeing sure that we do not get confused with Ports :)
    left_motor_port = port.D
    motor_pair.pair(motor_pair.PAIR_1, port.F, port.E)  # pairing motors
    # left side second black line from the left
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -5, 0, velocity=700)  # alignment by pusing backwards

    # move forward towards silo
    await move_straight_for_degrees(port.F, port.E, 907, 600)  # Go to silo

    # move arm thrice to take the gears out of the silo
    await motor.run_for_degrees(right_motor_port, 170, 10000)  # forward to hit lever
    await motor.run_for_degrees(right_motor_port, -165, 10000)  # backward
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -5, 0, 600)  # When the attactchment hits, turns bot- conteracts turn
    await motor.run_for_degrees(right_motor_port, 165, 10000)  # forward
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -5, 0, 600)  # When the attactchment hits, turns bot- conteracts turn
    await motor.run_for_degrees(right_motor_port, -165, 10000)  # backward
    await motor.run_for_degrees(right_motor_port, 165, 10000)  # forward
    await motor.run_for_degrees(right_motor_port, -165, 10000)  # backward

    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -5, 0, 600)  # When the attactchment hits, turns bot- conteracts turn
    await motor.run_for_degrees(right_motor_port, 165, 10000)  # forward

    await motor.run_for_degrees(right_motor_port, -165, 10000)  # forward

    await motor.run_for_degrees(right_motor_port, 130, 500)  # forward

    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 49, 0, 250)  # turn so the attatchment can do the Forge mission

    # Go to forge
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 650, 0, velocity=500)  # move forward so the wheelcan hit the stick to let the balls out

    await motor.run_for_degrees(right_motor_port, -350, 500)  # backward arm to make sure it does not get in the way

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -180, 0, velocity=700)  # go backward to be able to do the
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 270, 0, 600)  # first turn to turn toward mission
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 400, 0, velocity=400)  # go forward to the mission
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 70, 0, 600)  # second turn to turn toward mission
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -200, 0, velocity=500)  # push back to complete mission
    await move_straight_for_degrees(port.F, port.E, 450, 550)  # go forward to be able to turn to do whats on sale
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 360, 0, 500)  # turn to whats on sale

    await motor.run_for_degrees(right_motor_port, 160, 10000)  # tip the scales

    # move back
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -60, 0, velocity=400)  # go back out of tip the scales
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -505, 0, 600)  # turn towards base
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -700, 0, velocity=800)  # go to base

    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -180, 0, 600)  # turn towards base
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -1000, 0, velocity=800)  # go to base


runloop.run(main())
