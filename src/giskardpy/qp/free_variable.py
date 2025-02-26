from collections import defaultdict
from typing import Dict, Optional, List, Union
import numpy as np
import giskardpy.casadi_wrapper as w
from giskardpy import identifier
from giskardpy.god_map import GodMap
from giskardpy.my_types import Derivatives


class FreeVariable:
    state_identifier: List[str] = identifier.joint_states

    def __init__(self,
                 name: str,
                 god_map: GodMap,
                 lower_limits: Dict[Derivatives, float],
                 upper_limits: Dict[Derivatives, float],
                 quadratic_weights: Optional[Dict[Derivatives, float]] = None,
                 horizon_functions: Optional[Dict[Derivatives, float]] = None):
        self.god_map = god_map
        self._symbols = {}
        self.name = name
        for derivative in Derivatives:
            self._symbols[derivative] = self.god_map.to_symbol(self.state_identifier + [name, derivative])
        self.position_name = str(self._symbols[Derivatives.position])
        self.default_lower_limits = lower_limits
        self.default_upper_limits = upper_limits
        self.lower_limits = {}
        self.upper_limits = {}
        if quadratic_weights is None:
            self.quadratic_weights = {}
        else:
            self.quadratic_weights = quadratic_weights
        assert max(self._symbols.keys()) == len(self._symbols) - 1

        self.horizon_functions = defaultdict(float)
        if horizon_functions is None:
            horizon_functions = {1: 0.1}
        self.horizon_functions.update(horizon_functions)

    @property
    def order(self) -> Derivatives:
        return Derivatives(len(self.quadratic_weights) + 1)

    def get_symbol(self, derivative: Derivatives) -> Union[w.Symbol, float]:
        try:
            return self._symbols[derivative]
        except KeyError:
            raise KeyError(f'Free variable {self} doesn\'t have symbol for derivative of order {derivative}')

    def get_lower_limit(self, derivative: Derivatives, default: bool = False, evaluated: bool = False) -> Union[w.Expression, float]:
        if not default and derivative in self.default_lower_limits and derivative in self.lower_limits:
            expr = w.max(self.default_lower_limits[derivative], self.lower_limits[derivative])
        elif derivative in self.default_lower_limits:
            expr = self.default_lower_limits[derivative]
        elif derivative in self.lower_limits:
            expr = self.lower_limits[derivative]
        else:
            raise KeyError(f'Free variable {self} doesn\'t have lower limit for derivative of order {derivative}')
        if evaluated:
            return self.god_map.evaluate_expr(expr)
        return expr

    def set_lower_limit(self, derivative: Derivatives, limit: Union[w.Expression, float]):
        self.lower_limits[derivative] = limit

    def set_upper_limit(self, derivative: Derivatives, limit: Union[Union[w.Symbol, float], float]):
        self.upper_limits[derivative] = limit

    def get_upper_limit(self, derivative: Derivatives, default: bool = False, evaluated: bool = False) -> Union[Union[w.Symbol, float], float]:
        if not default and derivative in self.default_upper_limits and derivative in self.upper_limits:
            expr = w.min(self.default_upper_limits[derivative], self.upper_limits[derivative])
        elif derivative in self.default_upper_limits:
            expr = self.default_upper_limits[derivative]
        elif derivative in self.upper_limits:
            expr = self.upper_limits[derivative]
        else:
            raise KeyError(f'Free variable {self} doesn\'t have upper limit for derivative of order {derivative}')
        if evaluated:
            return self.god_map.evaluate_expr(expr)
        return expr

    def has_position_limits(self) -> bool:
        try:
            lower_limit = self.get_lower_limit(Derivatives.position)
            upper_limit = self.get_upper_limit(Derivatives.position)
            return lower_limit is not None and upper_limit is not None
        except KeyError:
            return False

    @profile
    def normalized_weight(self, t: int, derivative: Derivatives, prediction_horizon: int,
                          evaluated: bool = False) -> Union[Union[w.Symbol, float], float]:
        weight = self.quadratic_weights[derivative]
        start = weight * self.horizon_functions[derivative]
        a = (weight - start) / prediction_horizon
        weight = a * t + start
        expr = weight * (1 / self.get_upper_limit(derivative)) ** 2
        if evaluated:
            return self.god_map.evaluate_expr(expr)

    def __str__(self) -> str:
        return self.position_name

    def __repr__(self):
        return str(self)
