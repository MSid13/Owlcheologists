# Import necessary modules from the Hub SDK
from hub import light_matrix, port
import runloop
import motor_pair
import motor
from hub import motion_sensor

notUseGyro = False

# Custom function to move straight using gyro correction
async def move_straight_for_degrees(left_motor: int, right_motor: int, degrees: int, speed: int) -> None:


    if notUseGyro:
        await motor_pair.move_for_degrees(motor_pair.PAIR_1, degrees, 0, velocity=speed)
        return

    # Reset motor positions
    motor.reset_relative_position(left_motor, 0)
    motor.reset_relative_position(right_motor, 0)

    # Reset yaw angle to zero
    motion_sensor.reset_yaw(0)

    # Target angle for straight movement
    target_angle = 0

    # Proportional gain for correction
    Kp = 0.1# Adjust if needed for better correction

    # Loop until desired degrees reached
    while abs(motor.relative_position(left_motor)) < abs(degrees):
        # Current yaw angle
        current_angle = motion_sensor.tilt_angles()[0]

        # Error calculation
        error = target_angle - current_angle

        # Correction based on error
        correction = int(Kp * error)

        # Adjust motor speeds
        left_speed = speed + correction
        right_speed = speed - correction

        # Apply movement
        motor_pair.move_tank(motor_pair.PAIR_1, left_speed, right_speed)

        # Small delay for stability
        await runloop.sleep_ms(10)

    # Stop motors after movement
    motor_pair.stop(motor_pair.PAIR_1)


# Main routine
async def main():

    # Pair motors
    motor_pair.pair(motor_pair.PAIR_1, port.F, port.E)

    # Towards mission 1 (straight using gyro)
    await move_straight_for_degrees(port.F, port.E, 1500, 400)

    # Turn left to align with mission
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 180, 0, 1000)
    #arm down
    await motor.run_for_degrees(port.D, -170, 250)
    #move forward and push topsoil
    await move_straight_for_degrees(port.F, port.E, 340, 600)

    await motor.run_for_degrees(port.C, -170, 250)
    await motor.run_for_degrees(port.D, 170, 250)


    await move_straight_for_degrees(port.F, port.E, 340, -400)

    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -260, 0, 1000)
    await move_straight_for_degrees(port.F, port.E, 1500, -800)


# Run the main routine
runloop.run(main())
