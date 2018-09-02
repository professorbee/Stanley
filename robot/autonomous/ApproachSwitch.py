from robotpy_ext.autonomous import StatefulAutonomous, state

from components import drive


class ApproachSwitch(StatefulAutonomous):

    MODE_NAME = "Approach Switch"

    drive: drive.Drive

    @state(first=True)
    def leave_wall(self):
        if self.drive.left_encoder.get() > 4:
            self.next_state("straighten")
        self.drive.drive(.4, -0.06)

    @state()
    def straighten(self):
        if self.drive.left_encoder.get() > 6:
            self.next_state("to_switch")
        self.drive.drive(.4, 0.12)

    @state()
    def to_switch(self):
        if self.drive.left_encoder.get() > 7:
            self.done()
        self.drive.drive(.4, 0)
