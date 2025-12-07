# Import necessary modules from the Hub SDK
from hub import light_matrix, port
import runloop
import motor_pair
import motor
from hub import motion_sensor


def forward(number):
    return number


def backward(number):
    return -number


async def move_motor_forward(degrees: int, speed: int) -> None:
    """Move motor on port.D forward - takes positive value"""
    await motor.run_for_degrees(port.D, degrees, speed)


async def move_motor_backward(degrees: int, speed: int) -> None:
    """Move motor on port.D backward - takes positive value"""
    await motor.run_for_degrees(port.D, -degrees, speed)


async def move_motor_port_f(degrees: int, speed: int) -> None:
    """Move motor on port.F - always takes positive value, negative applied internally"""
    await motor.run_for_degrees(port.F, -degrees, speed)


async def move_motor_port_c(degrees: int, speed: int) -> None:
    """Move motor on port.C - always takes positive value"""
    await motor.run_for_degrees(port.C, degrees, speed)

async def move_motor_port_e(degrees: int, speed: int) -> None:
    """Move motor on port.E - always takes positive value"""
    await motor.run_for_degrees(port.E, degrees, speed)

async def move_pair_forward(degrees: int, steering: int, velocity: int) -> None:
    """Move motor pair PAIR_1 forward for specified degrees"""
    await move_straight_for_degrees(degrees, velocity)


async def move_pair_backward(degrees: int, steering: int, velocity: int) -> None:
    """Move motor pair PAIR_1 backward for specified degrees - takes positive value"""
    await move_straight_for_degrees(degrees, -velocity)


async def move_pair_tank_forward(left_speed: int, right_speed: int, degrees: int) -> None:
    """Move motor pair PAIR_1 in tank mode forward for specified degrees"""
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, left_speed, right_speed, degrees)


async def move_pair_tank_backward(left_speed: int, right_speed: int, degrees: int) -> None:
    """Move motor pair PAIR_1 in tank mode backward - takes positive values"""
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
    motor_pair.pair(motor_pair.PAIR_1, left_motor, right_motor)

    await move_straight_for_degrees(1800, 600)

    ############################################!111111111111111111111111111111!!!!!!!!!!!!!!!!!!!!!!!!

    await move_pair_tank_backward(110, 0, 600)

    await move_pair_backward(230, 0, 400)

    await move_motor_forward(80, 300)

    for i in range(7):
        await move_motor_backward(70, 300)
        await move_motor_forward(70, 300)

    await move_motor_backward(70, 300)

    await move_pair_forward(237, 0, 550)

    await move_motor_port_f(360, 400)




    await move_pair_tank_backward(50, 0, 600)

    await move_straight_for_degrees(220, 550)

    await move_motor_port_c(190, 400)

    await move_motor_port_f(260, 400)

    await move_pair_backward(200, 0, 400)

    await move_pair_tank_forward(140, 0, 600)

    await move_pair_backward(1500, 0, 600)

    await move_pair_tank_backward(50, 0, 600)

    await move_pair_backward(1000, 0, 600)



runloop.run(main())
