# Import necessary modules from the Hub SDK
from hub import light_matrix, port
import runloop
import motor_pair
import motor
from hub import motion_sensor



async def move_straight_for_degrees(
    left_motor: int, right_motor: int, degrees: int, speed: int
) -> None:
    # motor_pair.pair(motor_pair.PAIR_1, left_motor, right_motor)

    motor.reset_relative_position(left_motor, 0)
    motor.reset_relative_position(right_motor, 0)
    # Reset the yaw angle to zero and wait for stabilization
    motion_sensor.reset_yaw(0)
    # await runloop.until(motion_sensor.stable)

    # Set the target angle (0 degrees for straight movement)
    target_angle = 0

    # Define the proportional gain for correction
    Kp = 0.08# 1# Adjust this value based on your robot's behavior

    # Loop to maintain straight movement

    while (abs(motor.relative_position(left_motor))) < abs(degrees):
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

def forward(number):
    return number


def backward(number):
    return -number


async def move_motor_forward(degrees: int, speed: int) -> None:
    """Move motor on port.D forward for specified degrees at given speed"""
    await motor.run_for_degrees(port.D, degrees, speed)


async def move_motor_backward(degrees: int, speed: int) -> None:
    """Move motor on port.D backward for specified degrees at given speed"""
    await motor.run_for_degrees(port.D, -degrees, speed)


async def move_pair_forward(degrees: int, steering: int, velocity: int) -> None:
    """Move motor pair PAIR_1 forward for specified degrees"""
    # await motor_pair.move_for_degrees(motor_pair.PAIR_1, degrees, steering, velocity=velocity)
    await move_straight_for_degrees(port.F, port.E, degrees, velocity)

async def move_pair_backward(degrees: int, steering: int, velocity: int) -> None:
    """Move motor pair PAIR_1 backward for specified degrees"""
    # await motor_pair.move_for_degrees(motor_pair.PAIR_1, -degrees, steering, velocity=velocity)
    await move_straight_for_degrees(port.F, port.E, degrees, -velocity)


async def move_pair_tank_forward(left_speed: int, right_speed: int, degrees: int) -> None:
    """Move motor pair PAIR_1 in tank mode forward for specified degrees"""
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, left_speed, right_speed, degrees)

async def move_pair_tank_backward(left_speed: int, right_speed: int, degrees: int) -> None:
    """Move motor pair PAIR_1 in tank mode backward for specified degrees"""
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -left_speed, -right_speed, degrees)


async def main():
    left_motor = port.F
    right_motor = port.E
    motor_pair.pair(motor_pair.PAIR_1, left_motor, right_motor)

    await move_straight_for_degrees(port.F, port.E, 1800, 600)

    ############################################!111111111111111111111111111111!!!!!!!!!!!!!!!!!!!!!!!!

    await move_pair_tank_backward(110, 0, 600)

    await move_pair_backward(230, 0, 400)

    await move_motor_forward(80, 300)

    for i in range(7):
        await move_motor_backward(70, 300)
        await move_motor_forward(70, 300)

    await move_motor_backward(70, 300)
    
    await move_pair_forward(400, 0, 550)

    await move_pair_tank_forward(100, 0, 600)

    await move_pair_forward(200, 0, 650)

    await move_pair_tank_forward(145, 0, 600)

    await move_pair_forward(1800, 0, 1000)


runloop.run(main())
