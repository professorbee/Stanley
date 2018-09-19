from networktables.util import ntproperty

import components


class Remote:
    """
        Allow driving the robot over network tables
        Pulls control values from the following keys in the "/RemoteControl" table:
            * left_speed: Forward/reverse speed on the left motors
            * right_speed: Forward/reverse speed on the right motors
            * rotation: Inplace and moving rotation speed
            * grab: A True/False of whether or not to close the grabbers (defaults to `True`)
    """

    left_speed = ntproperty("/RemoteControl/left_speed", 0.0)
    right_speed = ntproperty("/RemoteControl/right_speed", 0.0)
    rotation = ntproperty("/RemoteControl/rotation", 0.0)
    grab = ntproperty("/RemoteControl/grab", True)

    drive: components.drive.Drive
    lift: components.lift.Lift
    intake: components.intake.Intake
    grabber: components.grabber.Grabber

    def process(self):
        if self.grab:
            self.grabber.grab()
        else:
            self.grabber.release()

        self.drive.direct_drive = True
        self.drive.drive_train.tankDrive(-self.left_speed, -self.right_speed)

    def execute(self):
        pass
