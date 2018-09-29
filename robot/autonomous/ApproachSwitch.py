from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
import wpilib

from components import drive, intake


class ApproachSwitch(StatefulAutonomous):

    MODE_NAME = "Approach Switch"
    DEFAULT = True

    drive: drive.Drive
    intake: intake.Intake

    def on_enable(self):
        self.drive.left_encoder.zero()
        self.drive.right_encoder.zero()
        super().on_enable()

    @timed_state(first=True, duration=5, next_state="prep_reverse")
    def leave_wall(self):
        if self.drive.right_encoder.get() > 110.5:
            if wpilib.DriverStation.getInstance().getGameSpecificMessage()[0] == "R":
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
        self.drive.right_encoder.encoder.reset()
        self.next_state("reverse")

    @state()
    def reverse(self):
        if self.drive.right_encoder.get() < -10:
            self.next_state("finish2")
        self.drive.drive(-.6, 0)

    @state()
    def finish2(self):
        self.intake.set_speed(0)
        self.done()
