from enum import Enum, auto


class ControlMode(Enum):
    """
        An enum of all the control modes. Only one can be active
        at any given time
    """

    JOYSTICK = auto()
    GAMEPAD = auto()
    ZACH = auto()
    MANUAL_LIFT = auto()
    REMOTE_CONTROL = auto()


# "Export" controls
from .joystick import Joystick
from .gamepad import Gamepad
from .lift_override import LiftOverride
from .zach import Zach
