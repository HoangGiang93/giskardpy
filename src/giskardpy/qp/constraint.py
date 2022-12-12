from collections import namedtuple
from typing import List, Union, Optional, Callable

import giskardpy.casadi_wrapper as w
from giskardpy.my_types import Derivatives

DebugConstraint = namedtuple('debug', ['expr'])


class Constraint:
    lower_error = -1e4
    upper_error = 1e4
    lower_slack_limit = -1e4
    upper_slack_limit = 1e4
    linear_weight = 0

    def __init__(self,
                 name: str,
                 expression: w.Expression,
                 lower_error: w.symbol_expr_float, upper_error: w.symbol_expr_float,
                 velocity_limit: w.symbol_expr_float,
                 quadratic_weight: w.symbol_expr_float, control_horizon: int,
                 linear_weight: Optional[w.symbol_expr_float] = None,
                 lower_slack_limit: Optional[w.symbol_expr_float] = None,
                 upper_slack_limit: Optional[w.symbol_expr_float] = None):
        self.name = name
        self.expression = expression
        self.quadratic_weight = quadratic_weight
        self.control_horizon = control_horizon
        self.velocity_limit = velocity_limit
        self.lower_error = lower_error
        self.upper_error = upper_error
        if lower_slack_limit is not None:
            self.lower_slack_limit = lower_slack_limit
        if upper_slack_limit is not None:
            self.upper_slack_limit = upper_slack_limit
        if linear_weight is not None:
            self.linear_weight = linear_weight

    def __str__(self):
        return self.name

    def normalized_weight(self, prediction_horizon):
        weight_normalized = self.quadratic_weight * (1 / (self.velocity_limit)) ** 2
        return weight_normalized


class DerivativeConstraint:

    def __init__(self,
                 name: str,
                 derivative: Derivatives,
                 expression: w.Expression,
                 lower_limit: Union[w.symbol_expr_float, List[w.symbol_expr_float]],
                 upper_limit: Union[w.symbol_expr_float, List[w.symbol_expr_float]],
                 quadratic_weight: w.symbol_expr_float,
                 normalization_factor: Optional[w.symbol_expr_float],
                 control_horizon: w.symbol_expr_float,
                 lower_slack_limit: Union[w.symbol_expr_float, List[w.symbol_expr_float]],
                 upper_slack_limit: Union[w.symbol_expr_float, List[w.symbol_expr_float]],
                 linear_weight: w.symbol_expr_float = None,
                 horizon_function: Optional[Callable[[float, int], float]] = None):
        self.name = name
        self.derivative = derivative
        self.expression = expression
        self.quadratic_weight = quadratic_weight
        self.control_horizon = control_horizon
        self.normalization_factor = normalization_factor
        if self.is_iterable(lower_limit):
            self.lower_limit = lower_limit
        else:
            self.lower_limit = [lower_limit] * self.control_horizon

        if self.is_iterable(upper_limit):
            self.upper_limit = upper_limit
        else:
            self.upper_limit = [upper_limit] * self.control_horizon

        if self.is_iterable(lower_slack_limit):
            self.lower_slack_limit = lower_slack_limit
        else:
            self.lower_slack_limit = [lower_slack_limit] * self.control_horizon

        if self.is_iterable(upper_slack_limit):
            self.upper_slack_limit = upper_slack_limit
        else:
            self.upper_slack_limit = [upper_slack_limit] * self.control_horizon

        if linear_weight is not None:
            self.linear_weight = linear_weight

        def default_horizon_function(weight, t):
            return weight

        self.horizon_function = default_horizon_function
        if horizon_function is not None:
            self.horizon_function = horizon_function

    def is_iterable(self, thing):
        if isinstance(thing, w.ca.SX) and sum(thing.shape) == 2:
            return False
        return hasattr(thing, '__iter__')

    def normalized_weight(self, t):
        weight_normalized = self.quadratic_weight * (1 / self.normalization_factor) ** 2
        return self.horizon_function(weight_normalized, t)
