import wpilib
from wpilib.interfaces.generichid import GenericHID
import marsutils

import components
import common.misc


class LiftOverride(marsutils.ControlInterface):
    """
        Implements a manual override for the lift
        
        This mode is to allow manual rezeroing of the lift encoder
    """

    _DISPLAY_NAME = "Lift Override"

    gamepad: wpilib.XboxController

    lift: components.lift.Lift

    def teleopPeriodic(self):
        # Lift Manual Override
        squared_lift_value = (
            common.misc.signed_square(self.gamepad.getY(GenericHID.Hand.kRight)) * .5
        )
        self.lift.set_manual_override_value(squared_lift_value)

    def enabled(self):
        print("Lift override enable")
        self.lift.set_manual_override(True)

    def disabled(self):
        print("Lift override disabled")
        self.lift.set_manual_override(False)
