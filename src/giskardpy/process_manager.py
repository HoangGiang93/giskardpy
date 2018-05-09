import traceback
from collections import OrderedDict
from copy import copy
from time import sleep, time

import rospy

from giskardpy.god_map import GodMap
from giskardpy.exceptions import NameConflictException


class ProcessManager(object):
    def __init__(self, initial_state=None):
        self._plugins = OrderedDict()
        self._god_map = GodMap() if initial_state is None else copy(initial_state)
        self.original_universe = initial_state is None

    def register_plugin(self, name, plugin):
        if name in self._plugins:
            raise NameConflictException('A plugin with name "{}" already exists.'.format(name))
        self._plugins[name] = plugin

    def start_loop(self):
        for plugin in self._plugins.values():
            plugin.start(self._god_map)
            # TODO is it really a good idea to call get_readings here?
            # for identifier, value in plugin.get_readings().items():
            #     self._god_map.set_data(identifier, value)
        print('init complete')
        while self.update() and not rospy.is_shutdown():
            # TODO make sure this can be properly killed without rospy dependency
            if self.original_universe:
                rospy.sleep(0.1)

    def stop(self):
        for plugin in self._plugins.values():
            plugin.stop()

    def get_god_map(self):
        return self._god_map

    def update(self):
        for plugin_name, plugin in self._plugins.items():
            plugin.update()
            if plugin.end_parallel_universe():
                print('destroying parallel universe')
                return False
            for identifier, value in plugin.get_readings().items():
                self._god_map.set_data(identifier, value)
            if plugin.create_parallel_universe():
                print('creating new parallel universe')
                parallel_universe = ProcessManager(initial_state=self._god_map)
                for n, p in self._plugins.items():
                    parallel_universe.register_plugin(n, p.get_replacement())
                t = time()
                try:
                    parallel_universe.start_loop()
                except:
                    traceback.print_exc()
                    print('parallel universe died')
                parallel_universe.stop()
                rospy.loginfo('parallel universe existed for {}s'.format(time()-t))
                plugin.post_mortem_analysis(parallel_universe.get_god_map())
                # TODO different function for get readings after end of universe?
                for identifier, value in plugin.get_readings().items():
                    self._god_map.set_data(identifier, value)
        return True



