import sys
sys.path.append('.')
import unittest
from models.cpu import Cpu
from models.task import Task
from unittest.mock import Mock

class SimulationTestCase(unittest.TestCase):

    def test_updated_task_after_cpu_udpate(self):
        cpu_a = Cpu('Cpu A')
        deadline = period = 10
        cpu_time = 5
        task1 = Task('A', cpu_a, deadline, period, cpu_time, 5)
        task2 = Task('B', cpu_a, deadline, period, cpu_time, 3)
        cpu_a.update()

    def test_update_task_and_finish_instance(self):
        cpu_a = Mock()
        deadline = period = 2
        cpu_time = 2
        task = Task('A', cpu_a, deadline, period, cpu_time)
        cpu_a.active_task = task
        # cpu time equals period so task generate a new instance
        cpu_a.time = period
        self.assertFalse(task.instances)
        task.update()
        # cpu time not equal period so task doesnt generate more instances
        cpu_a.time = period + 1
        self.assertTrue(task.instances)
        # Now compute task until instance finish
        task.update()
        task.update()
        self.assertFalse(task.instances)


if __name__ == '__main__':
    unittest.main()
