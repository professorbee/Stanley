from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
import wpilib

from components import drive, intake, grabber

# from controller.angle_controller import AngleController


class ApproachSwitch(StatefulAutonomous):
    MODE_NAME = "Approach Switch"
    DEFAULT = True

    drive: drive.Drive
    intake: intake.Intake
    grabber: grabber.Grabber
    # angle_ctrl: AngleController

    def on_enable(self):
        self.drive.reset_encoders()
        self.drive.left_encoder.zero()
        self.drive.right_encoder.zero()
        super().on_enable()

    @timed_state(first=True, duration=5, next_state="prep_reverse")
    def leave_wall(self):
        if self.drive.right_encoder.get() > 110.5:
            if wpilib.DriverStation.getInstance().getGameSpecificMessage()[0] == "R":
                self.grabber.release()
                self.intake.set_speed(0.5)
                self.next_state("launch")
            else:
                self.next_state("prep_reverse")
        self.drive.drive(.6, 0)

    @timed_state(duration=1, next_state="launch_stop")
    def launch(self):
        self.intake.set_speed(1)

    @state()
    def launch_stop(self):
        self.intake.set_speed(0)
        self.next_state("prep_reverse")

    @state()
    def prep_reverse(self):
        self.drive.right_encoder.zero()
        self.drive.left_encoder.zero()
        self.drive.reset_encoders()
        if self.drive.right_encoder.get() == 0:
            self.next_state("reverse")
        else:
            self.next_state("reverse2")

    # TODO: Figure this out
    @state()
    def reverse2(self):
        if self.drive.right_encoder.get() < -20:
            self.next_state("finish2")
        self.drive.drive(-.6, 0)

    @state()
    def reverse(self):
        if self.drive.right_encoder.get() < 40:
            self.next_state("finish2")
        self.drive.drive(-.6, 0)

    # @state()
    # def prep_turn(self):
    #     self.angle_ctrl.set_target(45)
    #     self.angle_ctrl.finished = False
    #     self.next_state("turn")

    # @timed_state(duration=2, next_state="activate_intake")
    # @timed_state(duration=2, next_state="finish2")
    # def turn(self):
    #     self.drive.right_encoder.zero()
    #     self.drive.left_encoder.zero()
    #     self.drive.reset_encoders()
    # self.angle_ctrl.enable()

    # @state()
    # def activate_intake(self):
    #     self.intake.set_speed(-0.8)
    #     self.next_state("approach_stack")

    # @timed_state(duration=3, next_state="reverse_from_cubes")
    # def approach_stack(self):
    #     if self.drive.right_encoder.get() > 30:
    #         self.next_state("reverse_from_cubes")
    #     self.drive.drive(0.55, 0)

    # @timed_state(duration=3, next_state="finish2")
    # def reverse_from_cubes(self):
    #     self.intake.set_speed(0)
    #     if self.drive.right_encoder.get() < 0:
    #         self.next_state("finish")
    #     self.drive.drive(-.55, 0)

    @state()
    def finish2(self):
        self.drive.drive(0, 0)
        self.done()
