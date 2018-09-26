import wpilib
from wpilib.interfaces.generichid import GenericHID


import components


class Zach:
    """
        Implements gamepad control via a xbox style gamepad
        
        Currently Gamepad and Zach control modes are the same
    """

    gamepad: wpilib.XboxController
    gamepad_alt: wpilib.XboxController

    drive: components.drive.Drive
    lift: components.lift.Lift
    intake: components.intake.Intake
    grabber: components.grabber.Grabber

    def process(self):
        self.drive.drive(
            self.gamepad.getTriggerAxis(GenericHID.Hand.kRight)
            + -self.gamepad.getTriggerAxis(GenericHID.Hand.kLeft),
            -self.gamepad.getX(GenericHID.Hand.kLeft) * .75,
        )

        self.intake.set_speed(-self.gamepad_alt.getY(GenericHID.Hand.kRight))

        if self.gamepad_alt.getRawButton(5):
            self.grabber.grab()
        elif self.gamepad_alt.getRawButton(6):
            self.grabber.release()

        if self.gamepad_alt.getXButton():
            self.lift.set_setpoint(0)
        elif self.gamepad_alt.getYButton():
            self.lift.set_setpoint(2565 * .5)
        elif self.gamepad_alt.getBButton():
            self.lift.set_setpoint(2565)

    def execute(self):
        pass

