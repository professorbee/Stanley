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
from controller.angle_controller import AngleController

ENCODER_REVOLUTION = 360
WHEEL_DIAMETER = 4
WHEEL_REVOLUTION = (math.pi * WHEEL_DIAMETER) / ENCODER_REVOLUTION

LIFT_HUB_DIAMETER = 3 + (7 / 8)
LIFT_HUB_REVOLUTION = (math.pi * LIFT_HUB_DIAMETER) / ENCODER_REVOLUTION


class Stanley(magicbot.MagicRobot):
    ## Magic components
    drive: drive.Drive
    lift: lift.Lift
    intake: intake.Intake
    grabber: grabber.Grabber

    ## Control modes
    joystick_control: control.Joystick
    # Gamepad or "Zach" controls
    gamepad_control: control.Gamepad
    zach_control: control.Zach
    trevor_control: control.Trevor
    lift_override_control: control.LiftOverride

    angle_ctrl: AngleController

    def createObjects(self):
        # Inputs
        # TODO: Update these dynamically
        self.stick = wpilib.Joystick(2)
        # self.gamepad = wpilib.XboxController(1)
        # self.gamepad_alt = wpilib.XboxController(2)
        self.gamepad = wpilib.XboxController(0)
        self.gamepad_alt = wpilib.XboxController(1)

        # Drive motors
        self.left_motor = wpilib.Spark(0)
        self.right_motor = wpilib.Spark(1)

        self.drive_train = wpilib.drive.DifferentialDrive(
            self.left_motor, self.right_motor
        )

        # Elevator encoder (gearbox)
        self.lift_encoder = ExternalEncoder(0, 1)
        # TODO: Fix the pid
        # self.lift_encoder.encoder.setDistancePerPulse(WHEEL_REVOLUTION)

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

        # Intake motors
        self.left_intake_motor = wpilib.Spark(2)
        self.right_intake_motor = wpilib.Spark(3)

        # Intake grabbers
        self.grabber_solenoid = wpilib.DoubleSolenoid(1, 0, 1)

        # PDP
        self.pdp = wpilib.PowerDistributionPanel(0)
        wpilib.SmartDashboard.putData("PowerDistributionPanel", self.pdp)

        # Misc
        self.navx = navx.AHRS.create_spi()

        self.net_table = NetworkTables.getTable("SmartDashboard")

        # Setup control chooser
        self.control_chooser = wpilib.SendableChooser()
        self.control_chooser.addObject("Joystick", 1)
        self.control_chooser.addObject("Gamepad", 2)
        self.control_chooser.addObject("Zach", 3)
        self.control_chooser.addDefault("Trevor", 4)
        self.control_chooser.addObject("Lift Override", 5)
        self.control_chooser.addObject("Remote Control", 6)

        wpilib.SmartDashboard.putData("Control Mode", self.control_chooser)

        self.control_chooser_control = ChooserControl(
            "Control Mode", on_selected=self.control_mode_changed
        )

        self.control_mode = ControlMode.GAMEPAD

        # Launch camera server
        wpilib.CameraServer.launch()

    def autonomous(self):
        """Prepare for autonomous mode"""

        magicbot.MagicRobot.autonomous(self)

    def teleopPeriodic(self):
        # Dont let an error take down robot
        with self.consumeExceptions():
            ## Drive code is in the ".control" module
            if self.control_mode == ControlMode.GAMEPAD:
                self.gamepad_control.process()
            elif self.control_mode == ControlMode.ZACH:
                self.zach_control.process()
            elif self.control_mode == ControlMode.TREVOR:
                self.trevor_control.process()
            elif self.control_mode == ControlMode.JOYSTICK:
                self.joystick_control.process()
            elif self.control_mode == ControlMode.MANUAL_LIFT:
                self.lift_override_control.process()

            # Set the override state
            # This is outside the if block so that it will be disabled properly
            self.lift.set_manual_override(self.control_mode == ControlMode.MANUAL_LIFT)

    def control_mode_changed(self, new_value):
        """
            Network tables callback to update control mode
        """
        try:
            self.control_mode = ControlMode(self.control_chooser.getSelected())
        except ValueError:
            print(
                "Unable to set control mode, `{}:{}` is not valid".format(
                    new_value, self.control_chooser.getSelected()
                )
            )


if __name__ == "__main__":
    # Run robot
    wpilib.run(Stanley)
