#!/usr/bin/env python
import os
from rospkg import RosPack

import rospy

from giskardpy.plugin_action_server import ActionServerPlugin
from giskardpy.application import ROSApplication
from giskardpy.plugin_instantaneous_controller import CartesianBulletControllerPlugin
from giskardpy.plugin_fk import FKPlugin
from giskardpy.plugin_interactive_marker import InteractiveMarkerPlugin
from giskardpy.plugin_joint_state import JointStatePlugin
from giskardpy.plugin_pybullet import PyBulletPlugin
from giskardpy.plugin_set_controlled_joints import SetControlledJointsPlugin
from giskardpy.process_manager import ProcessManager

if __name__ == '__main__':
    rospy.init_node('giskard')

    # root_link = rospy.get_param('~root_link', 'odom')
    root_tips = rospy.get_param('~interactive_marker_chains', [('base_link', 'r_gripper_tool_frame'),
                                                               ('base_link', 'l_gripper_tool_frame')])
    gui = rospy.get_param('~enable_gui', False)
    map_frame = rospy.get_param('~map_frame', 'map')
    joint_convergence_threshold = rospy.get_param('~joint_convergence_threshold', 0.001)
    wiggle_precision_threshold = rospy.get_param('~wiggle_precision_threshold', 5)
    sample_period = rospy.get_param('~sample_period', 0.1)
    default_joint_vel_limit = rospy.get_param('~default_joint_vel_limit', 0.5)
    default_collision_avoidance_distance = rospy.get_param('~default_collision_avoidance_distance', 0.02)
    fill_velocity_values = rospy.get_param('~fill_velocity_values', False)
    nWSR = rospy.get_param('~nWSR', None)
    root_link = rospy.get_param('~root_link', 'base_footprint')
    marker = rospy.get_param('~enable_collision_marker', True)
    enable_self_collision = rospy.get_param('~enable_self_collision', False)
    if nWSR == 'None':
        nWSR = None
    path_to_data_folder = rospy.get_param('~path_to_data_folder', RosPack().get_path('giskardpy') + '/data/pr2/')
    # path_to_data_folder = '/home/ichumuh/giskardpy_ws/src/giskardpy/data/pr2'
    if not path_to_data_folder.endswith('/'):
        path_to_data_folder += '/'

    fk_identifier = 'fk'
    cartesian_goal_identifier = 'goal'
    js_identifier = 'js'
    controlled_joints_identifier = 'controlled_joints'
    trajectory_identifier = 'traj'
    time_identifier = 'time'
    next_cmd_identifier = 'motor'
    collision_identifier = 'collision'
    closest_point_identifier = 'cpi'
    collision_goal_identifier = 'collision_goal'


    pm = ProcessManager()
    pm.register_plugin('js',
                       JointStatePlugin(js_identifier=js_identifier,
                                        time_identifier=time_identifier,
                                        next_cmd_identifier=next_cmd_identifier,
                                        sample_period=sample_period))
    pm.register_plugin('controlled joints',
                       SetControlledJointsPlugin(controlled_joints_identifier=controlled_joints_identifier))
    pm.register_plugin('action server',
                       ActionServerPlugin(js_identifier=js_identifier,
                                          trajectory_identifier=trajectory_identifier,
                                          cartesian_goal_identifier=cartesian_goal_identifier,
                                          time_identifier=time_identifier,
                                          closest_point_identifier=closest_point_identifier,
                                          controlled_joints_identifier=controlled_joints_identifier,
                                          collision_goal_identifier=collision_goal_identifier,
                                          joint_convergence_threshold=joint_convergence_threshold,
                                          wiggle_precision_threshold=wiggle_precision_threshold,
                                          plot_trajectory=False,
                                          fill_velocity_values=fill_velocity_values))
    pm.register_plugin('bullet',
                       PyBulletPlugin(js_identifier=js_identifier,
                                      collision_identifier=collision_identifier,
                                      closest_point_identifier=closest_point_identifier,
                                      collision_goal_identifier=collision_goal_identifier,
                                      map_frame=map_frame,
                                      root_link=root_link,
                                      path_to_data_folder=path_to_data_folder,
                                      gui=gui,
                                      marker=marker,
                                      default_collision_avoidance_distance=default_collision_avoidance_distance,
                                      enable_self_collision=enable_self_collision))
    pm.register_plugin('fk', FKPlugin(js_identifier=js_identifier, fk_identifier=fk_identifier))
    pm.register_plugin('cart bullet controller',
                       CartesianBulletControllerPlugin(root_link=root_link,
                                                       fk_identifier=fk_identifier,
                                                       goal_identifier=cartesian_goal_identifier,
                                                       js_identifier=js_identifier,
                                                       next_cmd_identifier=next_cmd_identifier,
                                                       collision_identifier=collision_identifier,
                                                       closest_point_identifier=closest_point_identifier,
                                                       controlled_joints_identifier=controlled_joints_identifier,
                                                       collision_goal_identifier=collision_goal_identifier,
                                                       path_to_functions=path_to_data_folder,
                                                       nWSR=nWSR,
                                                       default_joint_vel_limit=default_joint_vel_limit))
    pm.register_plugin('interactive marker',
                       InteractiveMarkerPlugin(root_tips=root_tips))

    app = ROSApplication(pm)
    app.run()
