import wpilib
from wpilib.interfaces.generichid import GenericHID
import marsutils

from common import misc
import components


class Joystick(marsutils.ControlInterface):
    """
        Implements joystick control via a flight stick
    """

    _DISPLAY_NAME = "Joystick"

    stick: wpilib.Joystick
    gamepad: wpilib.XboxController

    drive: components.drive.Drive
    lift: components.lift.Lift
    intake: components.intake.Intake
    grabber: components.grabber.Grabber

    def teleopPeriodic(self):
        self.drive.drive(-self.stick.getY(), -self.stick.getZ())

        intake_speed = self.gamepad.getY(GenericHID.Hand.kLeft)
        if abs(intake_speed) >= 0.03:
            self.intake.set_speed(misc.signed_square(intake_speed))
        else:
            self.intake.set_speed(0)

        if self.stick.getRawButton(1):
            self.intake.set_speed(.75)
        if self.stick.getRawButton(2):
            self.intake.set_speed(-.75)

        if self.stick.getRawButton(4):
            self.grabber.release()
        elif self.stick.getRawButton(3):
            self.grabber.grab()

        if self.stick.getRawButton(8):
            self.lift.set_setpoint(0)
        elif self.stick.getRawButton(9):
            self.lift.set_setpoint(2565 * .5)
        elif self.stick.getRawButton(10):
            self.lift.set_setpoint(2565)
            # self.lift.set_setpoint(1620)
