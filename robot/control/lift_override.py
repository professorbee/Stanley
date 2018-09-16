import wpilib
from wpilib.interfaces.generichid import GenericHID

import components
import common.misc


class LiftOverride:
    """
        Implements a manual override for the lift
        
        This mode is to allow manual rezeroing of the lift encoder
    """

    gamepad: wpilib.XboxController

    lift: components.lift.Lift

    def process(self):
        # Lift Manual Override
        squared_lift_value = (
            misc.signed_square(self.gamepad.getY(GenericHID.Hand.kRight)) * .5
        )
        self.lift.set_manual_override_value(squared_lift_value)

    def execute(self):
        pass
