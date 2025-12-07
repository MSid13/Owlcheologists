# Import necessary modules from the Hub SDK
from hub import light_matrix, port
import runloop
import motor_pair
import motor
from hub import motion_sensor

notUseGyro = False


# Custom function to move straight using gyro correction
async def move_straight_for_degrees(
    left_motor: int, right_motor: int, degrees: int, speed: int
) -> None:

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
    # Ensure arm is in the right position to pick up red thing (FIRST ARM DOWN)
    await motor.run_for_degrees(port.D, -135, 100)

    # Towards mission (straight using gyro)
    await move_straight_for_degrees(port.F, port.E, 1190, 400)

    # The above code is to reach the mission

    # Backward (straight using gyro)
    await move_straight_for_degrees(port.F, port.E, 300, -400)
    await runloop.sleep_ms(500)

    # Arm up
    await motor.run_for_degrees(port.D, 20, 180)
    await runloop.sleep_ms(500)
    # move forward
    await move_straight_for_degrees(port.F, port.E, 120, 400)
    # Go forward
    # await move_straight_for_degrees(port.F, port.E, 10, -500)

    # Arm down to collect red
    await motor.run_for_degrees(port.D, -35, 100)
    await runloop.sleep_ms(500)

    # Arm up
    await motor.run_for_degrees(port.D, 50, 180)

    # Go back more (straight using gyro)
    await move_straight_for_degrees(port.F, port.E, 300, -200)

    # Arm up TO DROP RED
    await motor.run_for_degrees(port.D, 140, 800)

    # Turn right toward Mineshaft Explorer
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -110, 0, 1000)

    # Move forward toward Mineshaft Explorer (straight using gyro)
    await move_straight_for_degrees(port.F, port.E, 830, 400)

    # Move arm towards the floor (ARM MOVEMENT ##3)
    await motor.run_for_degrees(port.D, -150, 250)

    # Move right
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -190, 0, 1000)

    # Move straight (straight using gyro)
    await move_straight_for_degrees(port.F, port.E, 520, 400)

    # Move arm up to complete mission
    await motor.run_for_degrees(port.D, 90, 25)

    await runloop.sleep_ms(500)

    # RETURNING TO HOME

    # Turn left a bit
    # await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 100, 0, 1000)

    # Move backward
    await move_straight_for_degrees(port.F, port.E, 200, -1000)

    # Turn left
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 180, 0, 1000)

    # Move backward at a high velocity.
    await move_straight_for_degrees(port.F, port.E, 1500, -1000)


# Run the main routine
runloop.run(main())
