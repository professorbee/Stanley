import math
import magicbot
import wpilib
import wpilib.drive

import navx
from networktables import NetworkTables
from networktables.util import ChooserControl

from ctre import WPI_TalonSRX as CANTalon

from components import drive, lift, grabber, intake
from common.encoder import ExternalEncoder
import control
from control import ControlMode

ENCODER_REVOLUTION = 360
WHEEL_DIAMETER = 4
WHEEL_REVOLUTION = (math.pi * WHEEL_DIAMETER) / ENCODER_REVOLUTION


class Stanley(magicbot.MagicRobot):
    drive: drive.Drive
    lift: lift.Lift
    intake: intake.Intake
    grabber: grabber.Grabber

    ## Control modes
    joystick_control: control.Joystick
    # Gamepad or "Zach" controls
    gamepad_control: control.Gamepad
    lift_override_control: control.LiftOverride
    remote_control: control.Remote

    def __init__(self):
        self.control_chooser = wpilib.SendableChooser()
        self.control_chooser.addObject("Joystick", 1)
        self.control_chooser.addObject("Gamepad", 2)
        self.control_chooser.addObject("Zach", 3)
        self.control_chooser.addObject("Lift Override", 4)
        self.control_chooser.addObject("Remote Control", 5)

        wpilib.SmartDashboard.putData("Control Mode", self.control_chooser)

        self.control_chooser_control = ChooserControl(
            "Control Mode", on_selected=self.control_mode_changed
        )

        self.control_mode = ControlMode.GAMEPAD

        wpilib.CameraServer.launch()

        super().__init__()

    def createObjects(self):
        self.stick = wpilib.Joystick(0)
        self.gamepad = wpilib.XboxController(1)

        # Drive motors
        self.left_motor = wpilib.Spark(0)
        self.right_motor = wpilib.Spark(1)

        self.drive_train = wpilib.drive.DifferentialDrive(
            self.left_motor, self.right_motor
        )

        # Elevator encoder (gearbox)
        self.lift_encoder = ExternalEncoder(0, 1)

        # Drive encoders
        self.left_encoder = ExternalEncoder(2, 3)
        self.right_encoder = ExternalEncoder(4, 5, True)
        self.left_encoder.encoder.setDistancePerPulse(WHEEL_REVOLUTION)
        self.right_encoder.encoder.setDistancePerPulse(WHEEL_REVOLUTION)

        # Elevator motors
        self.lift_master = CANTalon(2)
        self.lift_follower1 = CANTalon(3)
        self.lift_follower2 = CANTalon(4)
        self.lift_follower1.follow(self.lift_master)
        self.lift_follower2.follow(self.lift_master)

        self.left_intake_motor = wpilib.Spark(2)
        self.right_intake_motor = wpilib.Spark(3)

        self.grabber_solenoid = wpilib.DoubleSolenoid(1, 0, 1)

        self.navx = navx.AHRS.create_spi()

        self.net_table = NetworkTables.getTable("SmartDashboard")

        self.pdp = wpilib.PowerDistributionPanel(0)
        wpilib.SmartDashboard.putData("PowerDistributionPanel", self.pdp)

    def autonomous(self):
        """Prepare for autonomous mode"""

        magicbot.MagicRobot.autonomous(self)

    def teleopPeriodic(self):
        ## Drive code is in the ".control" module
        if (
            self.control_mode == ControlMode.GAMEPAD
            or self.control_mode == ControlMode.ZACH
        ):
            self.gamepad_control.process()
        elif self.control_mode == ControlMode.JOYSTICK:
            self.joystick_control.process()
        elif self.control_mode == ControlMode.MANUAL_LIFT:
            self.lift_override_control.process()
        elif self.control_mode == ControlMode.REMOTE_CONTROL:
            self.remote_control.process()

        # Set the override state
        # This is outside the if block so that it will be disabled properly
        self.lift.set_manual_override(self.control_mode == ControlMode.MANUAL_LIFT)

    def control_mode_changed(self, new_value):
        try:
            self.control_mode = ControlMode(self.control_chooser.getSelected())
        except ValueError:
            print(
                "Unable to set control mode, `{}:{}` is not valid".format(
                    new_value, self.control_chooser.getSelected()
                )
            )


if __name__ == "__main__":
    wpilib.run(Stanley)
