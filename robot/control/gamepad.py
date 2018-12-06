import wpilib
from wpilib.interfaces.generichid import GenericHID
import marsutils

import components


class Gamepad(marsutils.ControlInterface):
    """
        Implements gamepad control via a xbox style gamepad
        
        Currently Gamepad and Trevor control modes are the same
    """

    _DISPLAY_NAME = "Gamepad"

    gamepad: wpilib.XboxController

    drive: components.drive.Drive
    lift: components.lift.Lift
    intake: components.intake.Intake
    grabber: components.grabber.Grabber

    def teleopPeriodic(self):
        self.drive.drive(
            self.gamepad.getTriggerAxis(GenericHID.Hand.kRight)
            + -self.gamepad.getTriggerAxis(GenericHID.Hand.kLeft),
            -self.gamepad.getX(GenericHID.Hand.kLeft) * .75,
        )

        self.intake.set_speed(-self.gamepad.getY(GenericHID.Hand.kRight))

        if self.gamepad.getXButton():
            self.grabber.release()
        elif self.gamepad.getBButton():
            self.grabber.grab()

        pov = self.gamepad.getPOV()
        if pov == 180:
            self.lift.set_setpoint(0)
        elif pov == 270 or pov == 90:
            # self.lift.set_setpoint(179 * .5)
            self.lift.set_setpoint(2367 * .5)
        elif pov == 0:
            # self.lift.set_setpoint(179)
            self.lift.set_setpoint(2367)
