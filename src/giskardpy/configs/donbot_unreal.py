from giskardpy.configs.default_giskard import Giskard


class DonbotUnreal(Giskard):
    def __init__(self):
        self.add_robot_from_parameter_server(
            joint_state_topics=['/iai_donbot/joint_states'])
        super().__init__()
        self.add_sync_tf_frame('map', 'odom')
        self.add_omni_drive_joint(parent_link_name='odom',
                                  child_link_name='base_footprint',
                                  odometry_topic='/iai_donbot/base_footprint')
        self.add_follow_joint_trajectory_server(namespace='/iai_donbot/joint_trajectory_controller/follow_joint_trajectory',
                                                state_topic='/iai_donbot/joint_trajectory_controller/state')
        self.add_base_cmd_velocity(cmd_vel_topic='/iai_donbot/cmd_vel',
                                   track_only_velocity=False)
