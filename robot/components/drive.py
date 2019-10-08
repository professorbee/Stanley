import wpilib

import navx
from common.encoder import ExternalEncoder
from magicbot import will_reset_to


class Drive:
    drive_train: wpilib.drive.DifferentialDrive
    navx: navx.AHRS
    right_encoder: ExternalEncoder
    left_encoder: ExternalEncoder

    y = will_reset_to(0)
    rotation = will_reset_to(0)
    squared = True

    def drive(self, y, rot, squared=True):
        self.y = y
        self.rotation = rot
        self.squared = squared

    def execute(self):
        self.drive_train.arcadeDrive(-self.y, -self.rotation, self.squared)
        self.update_sd()

    def reset_encoders(self):
        self.left_encoder.zero()
        self.right_encoder.zero()

    def update_sd(self):
        wpilib.SmartDashboard.putData(
            "Drive/Left Drive Encoder", self.left_encoder.encoder
        )
        wpilib.SmartDashboard.putData(
            "Drive/Right Drive Encoder", self.right_encoder.encoder
        )
        wpilib.SmartDashboard.putNumber("Drive/Navx", self.navx.getYaw())
