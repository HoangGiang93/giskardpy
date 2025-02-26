import traceback
from collections import defaultdict
from typing import Dict
import re
import numpy as np

from giskardpy import identifier
from giskardpy.data_types import JointStates
from giskardpy.model.trajectory import Trajectory
from giskardpy.tree.behaviors.plot_trajectory import PlotTrajectory
from giskardpy.utils.logging import logwarn
from giskardpy.utils.utils import plot_trajectory, create_path


class PlotDebugExpressions(PlotTrajectory):
    @profile
    def __init__(self, name, enabled, wait=True, **kwargs):
        super().__init__(name=name,
                         enabled=enabled,
                         velocity_threshold=None,
                         normalize_position=False,
                         wait=wait,
                         **kwargs)
        # self.path_to_data_folder += 'debug_expressions/'
        # create_path(self.path_to_data_folder)

    def split_traj(self, traj) -> Trajectory:
        new_traj = Trajectory()
        for time, js in traj.items():
            new_js = JointStates()
            for name, js_ in js.items():
                # name = name.replace('/', '|')
                # traj_name = ''.join(name.split('/')[:-1])
                # name = name.split('/')[-1]
                if isinstance(js_.position, np.ndarray):
                    for x in range(js_.position.shape[0]):
                        for y in range(js_.position.shape[1]):
                            tmp_name = f'{name}|{x}_{y}'
                            # tmp_name = re.escape(tmp_name)
                            # tmp_name = tmp_name.replace('/', '|')
                            # tmp_name = tmp_name.replace('/', '\/')
                            new_js[tmp_name].position = js_.position[x, y]
                            new_js[tmp_name].velocity = js_.velocity[x, y]
                else:
                    new_js[name] = js_
                new_traj.set(time, new_js)

        return new_traj

    def plot(self):
        trajectory = self.get_god_map().get_data(identifier.debug_trajectory)
        if trajectory and len(trajectory.items()) > 0:
            sample_period = self.get_god_map().get_data(identifier.sample_period)
            traj = self.split_traj(trajectory)
            controlled_joints = list(traj.get_exact(0).keys())
            try:
                plot_trajectory(tj=traj,
                                controlled_joints=controlled_joints,
                                path_to_data_folder=self.path_to_data_folder,
                                sample_period=sample_period,
                                file_name=f'debug.pdf',
                                **self.kwargs)
            except Exception:
                traceback.print_exc()
                logwarn('failed to save debug.pdf')
