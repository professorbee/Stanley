import wpilib
from wpilib.interfaces.generichid import GenericHID
import marsutils


import components


class Trevor(marsutils.ControlInterface):
    """
        Implements gamepad control via a xbox style gamepad
    """

    _DISPLAY_NAME = "Trevor"
    _SORT = 8

    gamepad: wpilib.XboxController
    gamepad_alt: wpilib.XboxController

    drive: components.drive.Drive
    lift: components.lift.Lift
    intake: components.intake.Intake
    grabber: components.grabber.Grabber

    def process(self):
        forward_speed = self.gamepad.getTriggerAxis(GenericHID.Hand.kRight)
        reverse_speed = -self.gamepad.getTriggerAxis(GenericHID.Hand.kLeft)
        total_speed = forward_speed + reverse_speed
        if self.lift.lift_encoder.get() > 700:
            total_speed *= 0.8
        if self.lift.get_setpoint() > 1500:
            total_speed *= 0.8

        self.drive.drive(total_speed, -self.gamepad.getX(GenericHID.Hand.kLeft) * .75)

        left_intake_input = self.gamepad_alt.getY(GenericHID.Hand.kLeft)
        right_intake_input = self.gamepad_alt.getY(GenericHID.Hand.kRight)
        self.intake.set_speed(-(left_intake_input + right_intake_input))

        if self.gamepad_alt.getXButton() or self.gamepad_alt.getBumper(
            GenericHID.Hand.kLeft
        ):
            self.grabber.release()
        elif self.gamepad_alt.getBButton() or self.gamepad_alt.getBumper(
            GenericHID.Hand.kRight
        ):
            self.grabber.grab()

        # if self.gamepad_alt.getAButton():
        #     self.lift.set_setpoint(0)
        # elif self.gamepad_alt.getXButton():
        #     self.lift.set_setpoint(30)
        # elif self.gamepad_alt.getYButton():
        #     self.lift.set_setpoint(80)
        # elif self.gamepad_alt.getBButton():
        #     self.lift.set_setpoint(105)
        # 2323
        pov = self.gamepad_alt.getPOV()
        if pov == 180:  # Down (Minimum)
            self.lift.set_setpoint(0)
        elif pov == 270:  # Left (Switch)
            self.lift.set_setpoint(600)
        elif pov == 90:  # Right (Scale upper)
            self.lift.set_setpoint(1800)
        elif pov == 0:  # Up (Scale lower)
            self.lift.set_setpoint(1600)

        setpoint = self.lift.get_setpoint()
        if self.gamepad_alt.getRawAxis(3) > 0.02:
            self.lift.set_setpoint(setpoint + (self.gamepad_alt.getRawAxis(3) * 60))
        if self.gamepad_alt.getRawAxis(2) > 0.02:
            self.lift.set_setpoint(setpoint - (self.gamepad_alt.getRawAxis(2) * 60))

    def execute(self):
        pass
