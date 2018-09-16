import wpilib
from wpilib.interfaces.generichid import GenericHID


import components


class Gamepad:
    """
        Implements gamepad control via a xbox style gamepad
        
        Currently Gamepad and Zach control modes are the same
    """

    gamepad: wpilib.XboxController

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

        self.intake.set_speed(-self.gamepad.getY(GenericHID.Hand.kRight))

        if self.gamepad.getXButton():
            self.grabber.release()
        elif self.gamepad.getBButton():
            self.grabber.grab()

        pov = self.gamepad.getPOV()
        if pov == 180:
            self.lift.set_setpoint(0)
        elif pov == 270 or pov == 90:
            self.lift.set_setpoint(2565 * .5)
        elif pov == 0:
            self.lift.set_setpoint(2565)

    def execute(self):
        pass

