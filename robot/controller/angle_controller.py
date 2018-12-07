from magicbot import tunable
import wpilib
import navx
from wpilib.interfaces import PIDOutput

from components.drive import Drive


class AngleController:
    drive: Drive
    navx: navx.AHRS

    def setup(self,):
        self.target = 0
        self.speed = 0.45
        self.finished = False
        self.start = self.navx.getAngle()
        self.enabled = False

    def set_target(self, target: float):
        self.target = target

    def set_speed(self, speed: float):
        self.speed = speed

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def zero(self):
        self.navx.zeroYaw()

    def on_target(self) -> bool:
        return self.finished

    def execute(self):
        if self.enabled:
            # print((self.target - self.start) > 0)
            # print(self.target, self.start, self.navx.getAngle())
            angle = self.navx.getAngle() + 45
            if (self.target - self.start) > 0:
                # if (self.navx.getAngle() - self.start) < self.target+self.start:
                if (angle - self.start) < self.target - self.start:
                    # if (self.navx.getAngle() < self.target):
                    self.drive.drive(0, self.speed)
                else:
                    self.finished = True
            else:
                # if (self.navx.getAngle() - self.start) > (self.target + self.start):
                if (angle - self.start) > (self.target - self.start):
                    # if (self.navx.getAngle() > (self.target -self.start)):
                    self.drive.drive(0, -self.speed)
                else:
                    self.finished = True
