from magicbot import tunable
import wpilib
from wpilib.interfaces import PIDOutput
import navx

from components.drive import Drive


class AngleController(PIDOutput):
    drive: Drive
    navx: navx.AHRS

    kP = tunable(0.002)
    kI = tunable(0.0)
    kD = tunable(0.0)
    rate = 0.0

    def setup(self):
        self.pid_controller = wpilib.PIDController(
            0.01, 0.0001, 0.0001, self.navx, self
        )
        self.pid_controller.setInputRange(-180.0, 180.0)
        self.pid_controller.setOutputRange(-.75, .75)
        self.pid_controller.setContinuous()
        self.pid_controller.setAbsoluteTolerance(3)
        self.pid_controller.enable()

    def enable(self):
        self.pid_controller.enable()

    def disable(self):
        self.pid_controller.disable()

    def align_to(self, value: float):
        self.pid_controller.setSetpoint(value)

    def on_target(self):
        return self.pid_controller.onTarget()

    # PIDOutput
    def pidWrite(self, output: float):
        self.rate = output

    def execute(self):
        self.drive.drive(0, self.rate)
