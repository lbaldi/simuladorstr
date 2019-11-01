import unittest
from models.cpu import Cpu
from models.task import Task
from unittest.mock import Mock


class SimulationTestCase(unittest.TestCase):

    def test_updated_task_after_cpu_udpate(self):
        cpu_a = Cpu('Cpu A')
        deadline = period = 10
        cpu_time = 5
        Task('A', cpu_a, deadline, period, cpu_time)
        Task('B', cpu_a, deadline, period, cpu_time)
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

    def test_fail_having_more_than_one_task_overlapping(self):
        cpu = Cpu('Cpu A')
        deadline_a = deadline_b = 5
        period_a = period_b = 5
        cpu_time_a = cpu_time_b = 5
        Task('A', cpu, deadline_a, period_a, cpu_time_a)
        Task('B', cpu, deadline_b, period_b, cpu_time_b)
        with self.assertRaises(Exception):
            for x in range(10):
                cpu.update()


if __name__ == '__main__':
    unittest.main()
