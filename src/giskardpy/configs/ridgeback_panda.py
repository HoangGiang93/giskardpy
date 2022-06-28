from giskardpy.configs.default_config import Giskard


class RidgebackPanda(Giskard):

    def __init__(self):
        super().__init__()
        self.add_sync_tf_frame('map', 'odom')
        self.set_odometry_topic('/ridgeback_panda/base_link')
        self.add_follow_joint_trajectory_server(namespace='/ridgeback_panda/joint_trajectory_controller/follow_joint_trajectory',
                                                state_topic='/ridgeback_panda/joint_trajectory_controller/state')
        self.add_omni_drive_interface(cmd_vel_topic='/ridgeback_panda/cmd_vel',
                                      parent_link_name='odom',
                                      child_link_name='base_link')
        self.robot_interface_config.joint_state_topic = '/ridgeback_panda/joint_states'