from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
import wpilib

from components import drive, intake
from controller.angle_controller import AngleController


class FarLeftSwitch(StatefulAutonomous):
    MODE_NAME = "Far Left Switch"

    drive: drive.Drive
    intake: intake.Intake
    angle_ctrl: AngleController

    def on_enable(self):
        self.drive.reset_encoders()
        self.drive.left_encoder.zero()
        self.drive.right_encoder.zero()
        super().on_enable()

    @timed_state(first=True, duration=5, next_state="finish")
    def leave_wall(self):
        if self.drive.right_encoder.get() > 120.5:
            if wpilib.DriverStation.getInstance().getGameSpecificMessage()[0] == "L":
                self.next_state("prep_turn")
            else:
                self.next_state("finish")
        self.drive.drive(.6, 0)

    @state()
    def prep_turn(self):
        self.angle_ctrl.set_target(90)
        self.angle_ctrl.finished = False
        self.next_state("turn")

    @timed_state(duration=3, next_state="launch")
    def turn(self):
        self.drive.right_encoder.zero()
        self.drive.left_encoder.zero()
        self.drive.reset_encoders()
        self.angle_ctrl.enable()

    @timed_state(duration=1, next_state="finish")
    def launch(self):
        self.intake.set_speed(1)

    @state()
    def finish(self):
        self.intake.set_speed(0)
        self.drive.drive(0, 0)
        self.done()
