from giskardpy.configs.default_giskard import Giskard


class TiagoUnreal(Giskard):
    def __init__(self):
        self.add_robot_from_parameter_server(
            joint_state_topics=['/tiago/joint_states'])
        super().__init__()
        self.add_sync_tf_frame('map', 'odom')
        self.add_diff_drive_joint(parent_link_name='odom',
                                  child_link_name='base_footprint',
                                  translation_acceleration_limit=1,
                                  rotation_acceleration_limit=1,
                                  odometry_topic='/tiago/base_footprint')
        self.add_follow_joint_trajectory_server(namespace='/tiago/arm_left_controller/follow_joint_trajectory',
                                                state_topic='/tiago/arm_left_controller/state')
        self.add_follow_joint_trajectory_server(namespace='/tiago/arm_right_controller/follow_joint_trajectory',
                                                state_topic='/tiago/arm_right_controller/state')
        self.add_base_cmd_velocity(cmd_vel_topic='/tiago/cmd_vel',
                                   track_only_velocity=False)
