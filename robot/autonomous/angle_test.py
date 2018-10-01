# from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
# from magicbot import tunable
# from components import drive

# import navx
# from controller.angle_controller import AngleController


# class AngleTest(StatefulAutonomous):
#     MODE_NAME = "Gyro_Test"
#     DEFAULT = False

#     drive: drive.Drive
#     navx: navx.AHRS
#     angle_ctrl = AngleController

#     align_to = tunable(-45)  # Degrees

#     def on_enable(self):
#         super().on_enable()
#         self.navx.reset()

#     @timed_state(duration=10.0, first=True, next_state="finish")
#     def align(self, initial_call):
#         self.angle_ctrl.set_target(self.align_to)
#         self.angle_ctrl.enable()

#         if self.angle_ctrl.pid_controller.is_finished():
#             self.next_state("finish")

#     @state
#     def finish(self):
#         self.drive.drive(0.0, 0.0)
#         # self.drive.wait_for_align = False
#         # self.drive.threshold_input_vectors = True
#         # self.drive.disable_position_prediction()
#         self.done()
