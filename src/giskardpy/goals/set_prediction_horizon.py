from giskardpy import identifier
from giskardpy.goals.goal import Goal, NonMotionGoal
from giskardpy.utils import logging


class SetPredictionHorizon(Goal):
    def __init__(self,
                 prediction_horizon: int):
        """
        Will overwrite the prediction horizon for a single goal.
        Setting it to 1 will turn of acceleration and jerk limits.
        :param prediction_horizon: size of the prediction horizon, a number that should be 1 or above 5.
        """
        super().__init__()
        self.new_prediction_horizon = prediction_horizon

    def make_constraints(self):
        self.prediction_horizon = self.new_prediction_horizon
        if 5 > self.prediction_horizon > 1:
            logging.logwarn('Prediction horizon should be 1 or greater equal 5.')
        if self.prediction_horizon == 1:
            if 'acceleration' in self.god_map.get_data(identifier.joint_weights):
                del self.god_map.get_data(identifier.joint_weights)['acceleration']
            if 'acceleration' in self.god_map.get_data(identifier.joint_limits):
                del self.god_map.get_data(identifier.joint_limits)['acceleration']
        if self.prediction_horizon <= 2:
            if 'jerk' in self.god_map.get_data(identifier.joint_weights):
                del self.god_map.get_data(identifier.joint_weights)['jerk']
            if 'jerk' in self.god_map.get_data(identifier.joint_limits):
                del self.god_map.get_data(identifier.joint_limits)['jerk']
        if self.prediction_horizon <= 3:
            if 'jerk' in self.god_map.get_data(identifier.joint_weights):
                del self.god_map.get_data(identifier.joint_weights)['snap']
            if 'jerk' in self.god_map.get_data(identifier.joint_limits):
                del self.god_map.get_data(identifier.joint_limits)['snap']
        self.god_map.set_data(identifier.prediction_horizon, self.prediction_horizon)
        self.world.apply_default_limits_and_weights()

    def __str__(self) -> str:
        return str(self.__class__.__name__)


class SetMaxTrajLength(NonMotionGoal):
    def __init__(self,
                 new_length: int):
        """
        Overwrites Giskard trajectory length limit for planning.
        If the trajectory is longer than new_length, Giskard will prempt the goal.
        :param new_length: in seconds
        """
        super().__init__()
        self.god_map.set_data(identifier.MaxTrajectoryLength + ['length'], new_length)

    def __str__(self) -> str:
        return super().__str__()


class EnableVelocityTrajectoryTracking(NonMotionGoal):
    def __init__(self, enabled: bool = True):
        """
        A hack for the PR2. This goal decides whether the velocity part of the trajectory message is filled,
        when they are send to the robot.
        :param enabled: If True, will the velocity part of the message.
        """
        super().__init__()
        self.god_map.set_data(identifier.fill_trajectory_velocity_values, enabled)

    def __str__(self) -> str:
        return super().__str__()
