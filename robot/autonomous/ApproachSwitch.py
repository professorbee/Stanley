from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
import wpilib

from components import drive, intake
from controller.angle_controller import AngleController


class ApproachSwitch(StatefulAutonomous):
    MODE_NAME = "Approach Switch"
    DEFAULT = True

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
        if self.drive.right_encoder.get() > 110.5:
            if wpilib.DriverStation.getInstance().getGameSpecificMessage()[0] == "L":
                self.next_state("launch")
            else:
                self.next_state("prep_reverse")
        self.drive.drive(.6, 0)

    @timed_state(duration=1, next_state="prep_reverse")
    def launch(self):
        self.intake.set_speed(1)

    @state()
    def prep_reverse(self):
        self.drive.right_encoder.zero()
        self.drive.left_encoder.zero()
        self.drive.reset_encoders()
        if self.drive.right_encoder.get() == 0:
            self.next_state("reverse")
        else:
            self.next_state("reverse2")

    @state()
    def reverse2(self):
        if self.drive.right_encoder.get() < -20:
            self.angle_ctrl.set_target(45)
            self.angle_ctrl.finished = False
            self.next_state("turn")
        self.drive.drive(-.6, 0)

    @state()
    def reverse(self):
        if self.drive.right_encoder.get() < 40:
            self.angle_ctrl.set_target(45)
            self.angle_ctrl.finished = False
            self.next_state("turn")
        self.drive.drive(-.6, 0)

    @timed_state(duration=2, next_state="finish2")
    def turn(self):
        self.angle_ctrl.enable()

    @state()
    def finish2(self):
        self.intake.set_speed(0)
        self.drive.drive(0, 0)
        self.done()
