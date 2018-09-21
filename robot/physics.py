from pyfrc.physics import motor_cfgs, tankmodel, motion
from pyfrc.physics.units import units

ENCODER_REVOLUTION = 360


class PhysicsEngine(object):
    """
        Provide a simplistic simulation for the robot hardware
    """

    def __init__(self, physics_controller):
        """
            :param physics_controller: `pyfrc.physics.core.PhysicsInterface`
                                       object to send simulation effects to
        """

        self.physics_controller = physics_controller
        # Create a lift simulation
        self.lift_motion = motion.LinearMotion("Lift", 6, 360)

        # TODO: Check the values
        bumper_width = 3.25 * units.inch
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,  # motor configuration
            110 * units.lbs,  # robot mass
            8.45,  # drivetrain gear ratio
            2,  # motors per side
            22 * units.inch,  # robot wheelbase
            23 * units.inch + bumper_width * 2,  # robot width
            32 * units.inch + bumper_width * 2,  # robot length
            4 * units.inch,  # wheel diameter
        )

        # "Attach" navx gyro on the spi port
        self.physics_controller.add_device_gyro_channel("navxmxp_spi_4_angle")

    def update_sim(self, hal_data, now, tm_diff):
        # Simulate the drivetrain
        # Get drive motor outputs
        l_motor = hal_data["pwm"][0]["value"]
        r_motor = hal_data["pwm"][1]["value"]

        # Process the values with the drive model
        x, y, angle = self.drivetrain.get_distance(l_motor, r_motor, tm_diff)
        # Execute the computed values
        self.physics_controller.distance_drive(x, y, angle)

        # Simulate drive encoders
        hal_data["encoder"][1]["count"] = int(
            self.drivetrain.l_position * ENCODER_REVOLUTION
        )
        hal_data["encoder"][2]["count"] = int(
            self.drivetrain.r_position * ENCODER_REVOLUTION
        )

        # Simulate the lift encoders
        hal_data["encoder"][0]["count"] = self.lift_motion.compute(
            hal_data["CAN"][2]["value"], tm_diff
        )

