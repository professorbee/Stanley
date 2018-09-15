import wpilib


class Grabber:
    grabber_solenoid: wpilib.DoubleSolenoid

    def setup(self):
        self.state = wpilib.DoubleSolenoid.Value.kReverse

    def set_state(self, new_state: wpilib.DoubleSolenoid.Value):
        self.state = new_state

    def grab(self):
        self.set_state(wpilib.DoubleSolenoid.Value.kReverse)

    def release(self):
        self.set_state(wpilib.DoubleSolenoid.Value.kForward)

    def execute(self):
        self.grabber_solenoid.set(self.state)

