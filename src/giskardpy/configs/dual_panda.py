from giskardpy.configs.default_giskard import Giskard


class DualPanda1(Giskard):
    def __init__(self):
        self.add_robot_from_parameter_server(
            joint_state_topics=['/dual_panda/joint_states'])
        super().__init__(root_link_name='map')
        self.add_fixed_joint('map', 'dual_panda/base')
        self.add_follow_joint_trajectory_server(namespace='/dual_panda/panda_1_joint_trajectory_controller/follow_joint_trajectory',
                                                state_topic='/dual_panda/panda_1_joint_trajectory_controller/state')
class DualPanda2(Giskard):
    def __init__(self):
        self.add_robot_from_parameter_server(
            joint_state_topics=['/dual_panda/joint_states'])
        super().__init__(root_link_name='map')
        self.add_fixed_joint('map', 'dual_panda/base')
        self.add_follow_joint_trajectory_server(namespace='/dual_panda/panda_2_joint_trajectory_controller/follow_joint_trajectory',
                                                state_topic='/dual_panda/panda_2_joint_trajectory_controller/state')