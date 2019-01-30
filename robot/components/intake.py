import wpilib
from magicbot import will_reset_to


class Intake:
    left_intake_motor: wpilib.Spark
    right_intake_motor: wpilib.Spark

    speed = will_reset_to(0)

    def set_speed(self, new_speed: float):
        self.speed = new_speed

    def execute(self):
        self.left_intake_motor.set(self.speed)
        self.right_intake_motor.set(self.speed)
