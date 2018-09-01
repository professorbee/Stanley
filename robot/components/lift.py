import wpilib
from enum import Enum, auto
from ctre import WPI_TalonSRX as CANTalon

import common.encoder


class LiftMode(Enum):
    MANUAL = auto()
    AUTO = auto()


class Lift(object):
    lift_master: CANTalon
    lift_encoder: common.encoder.BaseEncoder

    def setup(self):
        self.pid_controller = wpilib.PIDController(
            0.022, 0.0, 0.0, self.lift_encoder, self.lift_master
        )
        self.pid_controller.setAbsoluteTolerance(0.005)
        self.pid_controller.setContinuous(False)
        self.pid_controller.setOutputRange(-.12, .5)
        self.pid_controller.enable()

        self.setpoint = 0

    def set_setpoint(self, new_pos):
        self.setpoint = new_pos
        self.pid_controller.setSetpoint(new_pos)

    def execute(self):
        ...
