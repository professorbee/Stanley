import wpilib


class Intake(object):
    left_intake_motor: wpilib.Spark
    right_intake_motor: wpilib.Spark

    def setup(self):
        self.right_intake_motor.setInverted(True)

        self.speed = 0.0

    def set_speed(self, new_speed: float):
        self.speed = new_speed

    def execute(self):
        self.left_intake_motor.set(self.speed)
        self.right_intake_motor.set(self.speed)
