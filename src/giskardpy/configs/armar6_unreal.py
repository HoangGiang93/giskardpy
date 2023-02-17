from giskardpy.configs.default_giskard import Giskard


class Armar6Unreal(Giskard):
    def __init__(self):
        self.add_robot_from_parameter_server(
            joint_state_topics=['/armar6/joint_states'])
        super().__init__()
        self.add_sync_tf_frame('map', 'odom')
        self.add_diff_drive_joint(parent_link_name='odom',
                                  child_link_name='Armar6',
                                  odometry_topic='/armar6/Armar6')
        self.add_follow_joint_trajectory_server(namespace='/armar6/arm_left_controller/follow_joint_trajectory',
                                                state_topic='/armar6/arm_left_controller/state')
        self.add_follow_joint_trajectory_server(namespace='/armar6/arm_right_controller/follow_joint_trajectory',
                                                state_topic='/armar6/arm_right_controller/state')
        self.add_base_cmd_velocity(cmd_vel_topic='/armar6/cmd_vel',
                                   track_only_velocity=False)
