#!/usr/bin/env python
import rospy

from giskardpy.configs.ridgeback_panda import RidgebackPanda
from giskardpy.utils.dependency_checking import check_dependencies

if __name__ == '__main__':
    rospy.init_node('giskard')
    check_dependencies()
    giskard = RidgebackPanda()
    giskard.live()
