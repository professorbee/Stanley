import wpilib

import navx
from common.encoder import ExternalEncoder


class Drive(object):
    drive_train: wpilib.drive.DifferentialDrive
    navx: navx.AHRS
    right_encoder: ExternalEncoder
    left_encoder: ExternalEncoder

    def __init__(self):
        self.y = self.rotation = 0
        self.squared = True

    def drive(self, y, rot, squared=True):
        self.y = y
        self.rotation = rot
        self.squared = squared

    def execute(self):
        self.drive_train.arcadeDrive(-self.y, -self.rotation, self.squared)

        self.y = 0
        self.rotation = 0
        self.update_sd()

    def update_sd(self):
        wpilib.SmartDashboard.putData(
            "Drive/Left Drive Encoder", self.left_encoder.encoder
        )
        wpilib.SmartDashboard.putData(
            "Drive/Right Drive Encoder", self.right_encoder.encoder
        )
        wpilib.SmartDashboard.putNumber("Drive/Navx", self.navx.getYaw())
