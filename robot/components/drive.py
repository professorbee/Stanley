import wpilib

from robotpy_ext.common_drivers import navx, distance_sensors
from networktables import NetworkTables
from networktables.networktable import NetworkTable
from common.encoder import ExternalEncoder


class Drive(object):
    drive_train: wpilib.drive.DifferentialDrive
    navX: navx.AHRS
    right_encoder: ExternalEncoder
    left_encoder: ExternalEncoder
    sd: NetworkTable

    def __init__(self):
        self.sd = NetworkTables.getTable("/SmartDashboard")

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
