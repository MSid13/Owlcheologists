# Import necessary modules from the Hub SDK
from hub import light_matrix, port
import runloop
import motor_pair
import motor
from hub import motion_sensor

notUseGyro = True


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
    await motor.run_for_degrees(port.D, -140, 100)

    # Towards mission (straight using gyro)
    await move_straight_for_degrees(port.F, port.E, 1190, 600)

    # The above code is to reach the mission

    # Backward (straight using gyro)
    await move_straight_for_degrees(port.F, port.E, 300, -400)
    await runloop.sleep_ms(500)

    # Arm up
    await motor.run_for_degrees(port.D, 20, 180)
    await runloop.sleep_ms(500)
    # move forward
    await move_straight_for_degrees(port.F, port.E, 145, 400)
    # Go forward
    # await move_straight_for_degrees(port.F, port.E, 10, -500)

    # Arm down to collect red
    await motor.run_for_degrees(port.D, -35, 100)
    await runloop.sleep_ms(500)

    # Arm up a bit
    await motor.run_for_degrees(port.D, 50, 180)

    # Go back more (straight using gyro)
    await move_straight_for_degrees(port.F, port.E, 300, -800)

    # Arm up TO DROP RED
    await motor.run_for_degrees(port.D, 140, 800)
    print("done")
    # Turn right facing Mineshaft Explorer
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -155, -0, 300)
    #Move forward
    await move_straight_for_degrees(port.F, port.E, 400, 400)
    #Turn near the oval to face map revea;
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -160, 300, -0,)

    # Move forward
    await move_straight_for_degrees(port.F, port.E, 690, 500)

    # Turn to align with map reveal
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -100, 300, -0)
    # Claw Down
    await motor.run_for_degrees(port.C, 140, 800)
    # One-way Door down
    await motor.run_for_degrees(port.D, 170, -400)
    # Move forward to push one of the top soil
    await move_straight_for_degrees(port.F, port.E, 420, 200)
    #go back
    await move_straight_for_degrees(port.F, port.E, 60, -200)
    # Arm up to capture one of the top soil
    await motor.run_for_degrees(port.C, 140, -100)
    #arm up
    await motor.run_for_degrees(port.D, 160, 400)
    #Move backward
    await move_straight_for_degrees(port.F, port.E, 170, -300)
    #turn to begin to align to wall
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -570, 400, -0,)
    #backward to perfectly align to wall
    await move_straight_for_degrees(port.F, port.E, 360, -400)
    # forward a bit
    await move_straight_for_degrees(port.F, port.E, 560, 400)
    #turn
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -340, 400, -0,)
    #arm dwon (not touching floor completely)
    await motor.run_for_degrees(port.D, 170, -400)
    #forward
    await move_straight_for_degrees(port.F, port.E, 640, 600)
    #arm up to complete mineshaft
    await motor.run_for_degrees(port.D, 140, 75)
    #turn to align with oval
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 340, 400, -0,)
    #forward
    await move_straight_for_degrees(port.F, port.E, 180, 400)
    #drop the topsoil
    await motor.run_for_degrees(port.C, 140, 100)
    await move_straight_for_degrees(port.F, port.E, 200, -400)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -500, 800, -0,)
    await move_straight_for_degrees(port.F, port.E, 1500, -800)






# Run the main routine
runloop.run(main())
