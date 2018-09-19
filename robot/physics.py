from pyfrc.physics import motor_cfgs, tankmodel, motion
from pyfrc.physics.units import units


class PhysicsEngine(object):
    """
        Simulates a motor moving something that strikes two limit switches,
        one on each end of the track. Obviously, this is not particularly
        realistic, but it's good enough to illustrate the point
    """

    def __init__(self, physics_controller):
        """
            :param physics_controller: `pyfrc.physics.core.PhysicsInterface`
                                       object to communicate simulation effects to
        """

        self.physics_controller = physics_controller
        self.motion = motion.LinearMotion("Lift", 360, 6)

        # Change these parameters to fit your robot!
        bumper_width = 3.25 * units.inch

        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,  # motor configuration
            100 * units.lbs,  # robot mass
            5.0,  # drivetrain gear ratio
            2,  # motors per side
            22 * units.inch,  # robot wheelbase
            23 * units.inch + bumper_width * 2,  # robot width
            32 * units.inch + bumper_width * 2,  # robot length
            4 * units.inch,  # wheel diameter
        )

        self.physics_controller.add_device_gyro_channel("navxmxp_spi_4_angle")

    def update_sim(self, hal_data, now, tm_diff):
        # Simulate the drivetrain
        l_motor = hal_data["pwm"][0]["value"]
        r_motor = hal_data["pwm"][1]["value"]

        x, y, angle = self.drivetrain.get_distance(l_motor, r_motor, tm_diff)
        self.physics_controller.distance_drive(x, y, angle)

        # Simulate drive encoders
        hal_data["encoder"][1]["count"] = int(self.drivetrain.l_position)
        hal_data["encoder"][2]["count"] = int(self.drivetrain.r_position)

        # Simulate the lift
        hal_data["encoder"][0]["count"] = self.motion.compute(
            hal_data["CAN"][2]["value"], tm_diff
        )

