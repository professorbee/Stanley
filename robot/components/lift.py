import wpilib
from enum import Enum
from ctre import WPI_TalonSRX as CANTalon
from networktables.networktable import NetworkTable
from networktables.util import ntproperty

import common.encoder


class LiftMode(Enum):
    MANUAL = 0
    AUTO = 1


class Lift(object):
    lift_master: CANTalon
    lift_encoder: common.encoder.BaseEncoder
    net_table: NetworkTable

    def setup(self):
        wpilib.SmartDashboard.putBoolean("Lift Manual Override", False)
        self.net_table.addEntryListener(
            self.control_mode_changed, key="Lift Manual Override"
        )

        self.manual_override = False

        self.pid_controller = wpilib.PIDController(
            0.022, 0.0, 0.0, self.lift_encoder, self.lift_master
        )
        self.pid_controller.setAbsoluteTolerance(0.005)
        self.pid_controller.setContinuous(False)
        self.pid_controller.setOutputRange(-.14, .5)
        self.pid_controller.enable()

        self.setpoint = 0
        self.manual_override_value = 0

    def set_setpoint(self, new_pos):
        self.setpoint = new_pos
        self.pid_controller.setSetpoint(new_pos)

    def set_manual_override_value(self, new_value):
        self.manual_override_value = new_value

    def execute(self):
        if self.manual_override:
            self.lift_master.set(
                CANTalon.ControlMode.PercentOutput, self.manual_override_value
            )

        wpilib.SmartDashboard.putData("Lift Encoder", self.lift_encoder.encoder)

    def control_mode_changed(self, _table, _key, manual, _is_new):
        self.manual_override = manual
        if manual:
            self.pid_controller.disable()
        else:
            self.lift_encoder.zero()
            self.pid_controller.enable()
