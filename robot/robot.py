import magicbot
import wpilib
from wpilib.interfaces.generichid import GenericHID
import wpilib.drive
import math

from robotpy_ext.common_drivers import navx
from networktables import NetworkTables

from ctre import WPI_TalonSRX as CANTalon

from components import drive, lift, grabber, intake
from common.encoder import ExternalEncoder
from common import misc


class Stanley(magicbot.MagicRobot):
    drive: drive.Drive
    lift: lift.Lift
    intake: intake.Intake
    grabber: grabber.Grabber

    def createObjects(self):
        self.stick = wpilib.Joystick(0)
        self.gampad = wpilib.XboxController(1)

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

        # Elevator motors
        self.lift_master = CANTalon(2)
        self.lift_follower1 = CANTalon(3)
        self.lift_follower2 = CANTalon(4)
        self.lift_follower1.follow(self.lift_master)
        self.lift_follower2.follow(self.lift_master)

        self.left_intake_motor = wpilib.Spark(2)
        self.right_intake_motor = wpilib.Spark(3)

        self.grabber_solenoid = wpilib.DoubleSolenoid(1, 0, 1)

        self.navX = navx.AHRS.create_spi()

        self.sd = NetworkTables.getTable("SmartDashboard")

    def autonomous(self):
        """Prepare for autonomous mode"""

        magicbot.MagicRobot.autonomous(self)

    def disabledPeriodic(self):
        pass

    def disabledInit(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        self.drive.drive(self.stick.getY(), self.stick.getZ())

        intake_speed = self.gampad.getY(GenericHID.Hand.kLeft)
        if abs(intake_speed) >= 0.03:
            self.intake.set_speed(misc.signed_square(intake_speed))
        else:
            self.intake.set_speed(0)

        if self.stick.getRawButton(4):
            self.grabber.grab()
        elif self.stick.getRawButton(5):
            self.grabber.release()

        if self.stick.getRawButton(8):
            self.lift.set_setpoint(0)
        elif self.stick.getRawButton(9):
            self.lift.set_setpoint(2565 * .5)
        elif self.stick.getRawButton(10):
            self.lift.set_setpoint(2565)


if __name__ == "__main__":
    wpilib.run(Stanley)
