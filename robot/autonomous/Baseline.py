from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
import wpilib

from components import drive, intake
from controller.angle_controller import AngleController


class Baseline(StatefulAutonomous):
    MODE_NAME = "Baseline"
    DEFAULT = False

    drive: drive.Drive

    def on_enable(self):
        self.drive.reset_encoders()
        self.drive.left_encoder.zero()
        self.drive.right_encoder.zero()
        super().on_enable()

    @timed_state(first=True, duration=5, next_state="finish")
    def leave_wall(self):
        if self.drive.right_encoder.get() > 110.5:
            self.next_state("finish")
        self.drive.drive(.6, 0)

    @state()
    def finish():
        self.drive.drive(0, 0)
        self.done()
