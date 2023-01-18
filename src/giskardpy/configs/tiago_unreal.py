from giskardpy.configs.default_giskard import Giskard


class RidgebackPandaMujoco(Giskard):
    def __init__(self):
        self.add_robot_from_parameter_server(
            joint_state_topics=['/ridgeback_panda/joint_states'])
        super().__init__()
        self.add_sync_tf_frame('map', 'odom')
        self.add_omni_drive_joint(parent_link_name='odom',
                                  child_link_name='base_link',
                                  translation_velocity_limit=0.4,
                                  rotation_velocity_limit=0.2,
                                  translation_acceleration_limit=1,
                                  rotation_acceleration_limit=1,
                                  translation_jerk_limit=5,
                                  rotation_jerk_limit=5,
                                  odometry_topic='/ridgeback_panda/base_link')
        self.add_follow_joint_trajectory_server(namespace='/ridgeback_panda/joint_trajectory_controller/follow_joint_trajectory',
                                                state_topic='/ridgeback_panda/joint_trajectory_controller/state')
        self.add_base_cmd_velocity(cmd_vel_topic='/ridgeback_panda/cmd_vel',
                                   track_only_velocity=False)
