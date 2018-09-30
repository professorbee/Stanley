from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
import wpilib

from components import drive, intake
from controller.angle_controller import AngleController


class Center(StatefulAutonomous):
    MODE_NAME = "Center"

    drive: drive.Drive
    intake: intake.Intake
    angle_ctrl: AngleController

    def on_enable(self):
        self.drive.reset_encoders()
        self.drive.left_encoder.zero()
        self.drive.right_encoder.zero()
        super().on_enable()

    @timed_state(first=True, duration=5, next_state="prep_reverse")
    def leave_wall(self):
        if self.drive.right_encoder.get() > 45:
            self.drive.reset_encoders()
            self.drive.left_encoder.zero()
            self.drive.right_encoder.zero()
            if wpilib.DriverStation.getInstance().getGameSpecificMessage()[0] == "L":
                self.next_state("turn_left_prep")
            else:
                self.next_state("turn_right_prep")
        self.drive.drive(.6, 0)

    @state()
    def turn_right_prep(self):
        self.angle_ctrl.set_target(40)
        self.angle_ctrl.finished = False
        self.next_state("turn")

    @state()
    def turn_left_prep(self):
        self.angle_ctrl.set_target(-40)
        self.angle_ctrl.finished = False
        self.next_state("turn")

    @timed_state(duration=2, next_state="finish2")
    def turn(self):
        self.angle_ctrl.enable()

    @state()
    def finish2(self):
        self.intake.set_speed(0)
        self.drive.drive(0, 0)
        self.done()
