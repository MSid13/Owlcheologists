# Import necessary modules from the Hub SDK
from hub import light_matrix, port
import runloop
import motor_pair
import motor
from hub import motion_sensor

notUseGyro = False


async def move_motor_port_d_forward(degrees: int, speed: int) -> None:
    """Move motor on port.D forward - takes positive value"""
    await motor.run_for_degrees(port.D, degrees, speed)


async def move_motor_port_d_backward(degrees: int, speed: int) -> None:
    """Move motor on port.D backward - takes positive value"""
    await motor.run_for_degrees(port.D, -degrees, speed)


async def move_motor_port_c_forward(degrees: int, speed: int) -> None:
    """Move motor on port.C forward - takes positive value"""
    await motor.run_for_degrees(port.C, degrees, speed)


async def move_motor_port_c_backward(degrees: int, speed: int) -> None:
    """Move motor on port.C backward - takes positive value"""
    await motor.run_for_degrees(port.C, -degrees, speed)


async def move_pair_tank_forward(left_speed: int, right_speed: int, degrees: int) -> None:
    """Move motor pair PAIR_1 in tank mode forward for specified degrees"""
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, left_speed, right_speed, degrees)


async def move_pair_tank_backward(left_speed: int, right_speed: int, degrees: int) -> None:
    """Move motor pair PAIR_1 in tank mode backward - takes positive values"""
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -left_speed, -right_speed, degrees)


async def move_straight_forward(degrees: int, speed: int) -> None:
    """Move straight forward using gyro correction - takes positive values"""
    if notUseGyro:
        await motor_pair.move_for_degrees(motor_pair.PAIR_1, degrees, 0, velocity=speed)
        return

    motor.reset_relative_position(port.F, 0)
    motor.reset_relative_position(port.E, 0)
    motion_sensor.reset_yaw(0)
    target_angle = 0
    Kp = 0.1

    while abs(motor.relative_position(port.F)) < abs(degrees):
        current_angle = motion_sensor.tilt_angles()[0]
        error = target_angle - current_angle
        correction = int(Kp * error)
        left_speed = speed + correction
        right_speed = speed - correction
        motor_pair.move_tank(motor_pair.PAIR_1, left_speed, right_speed)
        await runloop.sleep_ms(10)
    motor_pair.stop(motor_pair.PAIR_1)


async def move_straight_backward(degrees: int, speed: int) -> None:
    """Move straight backward using gyro correction - takes positive values"""
    if notUseGyro:
        await motor_pair.move_for_degrees(motor_pair.PAIR_1, -degrees, 0, velocity=speed)
        return

    motor.reset_relative_position(port.F, 0)
    motor.reset_relative_position(port.E, 0)
    motion_sensor.reset_yaw(0)
    target_angle = 0
    Kp = 0.1

    while abs(motor.relative_position(port.F)) < abs(degrees):
        current_angle = motion_sensor.tilt_angles()[0]
        error = target_angle - current_angle
        correction = int(Kp * error)
        left_speed = -speed + correction
        right_speed = -speed - correction
        motor_pair.move_tank(motor_pair.PAIR_1, left_speed, right_speed)
        await runloop.sleep_ms(10)
    motor_pair.stop(motor_pair.PAIR_1)


# Main routine
async def main():

    left_motor = port.F
    right_motor = port.E
    # Pair motors
    motor_pair.pair(motor_pair.PAIR_1, left_motor, right_motor)

    # Towards mission 1 (straight using gyro)
    await move_straight_forward(1500, 400)

    # Turn left to align with mission
    await move_pair_tank_forward(180, 0, 1000)
    # arm down
    await move_motor_port_d_backward(170, 250)
    # move forward and push topsoil
    await move_straight_forward(340, 600)
    # move backward a bit
    await move_straight_backward(60, 400)

    # arm up to collect one of the topsoil
    await move_motor_port_c_backward(100, 100)
    await move_straight_backward(300, 600)
    # await move_motor_port_d_forward(170, 100)
    await move_pair_tank_backward(240, 0, 1000)
    await move_straight_backward(1500, 1000)


# Run the main routine
runloop.run(main())
