from collections import OrderedDict

import sympy as sp

from giskardpy.sympy_wrappers import point3


class ControllerInputArray(object):
    separator = '__'

    def __init__(self, float_names, prefix='', suffix=''):
        if prefix == '':
            self._prefix = prefix
        else:
            self._prefix = '{}{}'.format(prefix, self.separator)
        if suffix == '':
            self._suffix = suffix
        else:
            self._suffix = '{}{}'.format(self.separator, suffix)

        self._symbol_map = OrderedDict({fn: sp.Symbol('{}{}{}'.format(self._prefix, fn, self._suffix))
                                        for fn in float_names})
        self._str_map = OrderedDict({k: str(v) for k, v in self._symbol_map.items()})

    def to_symbol(self, float_name):
        return self._symbol_map[float_name]

    def to_str_symbol(self, float_name):
        return self._str_map[float_name]

    def get_float_names(self):
        return self._symbol_map.keys()

    def get_update_dict(self, **kwargs):
        return {self._str_map[k]: v for k, v in kwargs.items() if k in self._symbol_map}

    def get_expression(self):
        return sp.Matrix([sp.Symbol(x) for x in self._symbol_map.values()])


class ScalarInput(ControllerInputArray):
    def __init__(self, prefix, suffix=''):
        super(ScalarInput, self).__init__(['v'], prefix, suffix)

    def get_update_dict(self, v):
        return super(ScalarInput, self).get_update_dict(v)

    def get_expression(self):
        return self._symbol_map['v']

    def get_symbol_str(self):
        return self._str_map['v']


class Point3(ControllerInputArray):
    def __init__(self, prefix, suffix=''):
        super(Point3, self).__init__(['x', 'y', 'z'], prefix, suffix)

    def get_update_dict(self, x, y, z):
        return super(Point3, self).get_update_dict(x, y, z)

    def get_x(self):
        return self._symbol_map['x']

    def get_y(self):
        return self._symbol_map['y']

    def get_z(self):
        return self._symbol_map['z']

    def get_expression(self):
        return point3(*self._symbol_map.values())


class Vec3(ControllerInputArray):
    def __init__(self, prefix, suffix=''):
        super(Vec3, self).__init__(['x', 'y', 'z'], prefix, suffix)

    def get_expression(self):
        return vec3(*self._symbol_map.values())


class Quaternion(ControllerInputArray):
    def __init__(self, prefix, suffix=''):
        super(Quaternion, self).__init__(['x', 'y', 'z', 'w'], prefix, suffix)

    def get_update_dict(self, x, y, z, w):
        return super(Quaternion, self).get_update_dict(x, y, z, w)

    def get_x(self):
        return self._symbol_map['x']

    def get_y(self):
        return self._symbol_map['y']

    def get_z(self):
        return self._symbol_map['z']

    def get_w(self):
        return self._symbol_map['w']

    def get_expression(self):
        return rotation3_quaternion(*self._symbol_map.values())


class Frame3(ControllerInputArray):
    def __init__(self, prefix, suffix=''):
        super(Frame3, self).__init__(['qx', 'qy', 'qz', 'qw', 'x', 'y', 'z'], prefix, suffix)

    def get_update_dict(self, qx, qy, qz, qw, x, y, z):
        return super(Quaternion, self).get_update_dict(qx, qy, qz, qw, x, y, z)

    def get_expression(self):
        return frame3_quaternion(*(self._symbol_map.values()[:4] + [point3(self._symbol_map.values()[4:])]))

    def get_position(self):
        return point3(*self._symbol_map.values()[4:])

    def get_rotation(self):
        return rotation3_quaternion(*self._symbol_map.values()[:4])