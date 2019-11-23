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

    def test_fail_having_more_than_one_task_overlapping(self):
        cpu = Cpu('Cpu A')
        Task('A', cpu, deadline=5, period=5, cpu_time=5)
        Task('B', cpu, deadline=5, period=5, cpu_time=5)
        with self.assertRaises(Exception):
            for x in range(20):
                cpu.update()

    def test_correct_simulation_1(self):
        cpu = Cpu('Cpu A')
        Task('A', cpu, deadline=10, period=10, cpu_time=5)
        Task('B', cpu, deadline=10, period=10, cpu_time=3)
        Task('C', cpu, deadline=10, period=20, cpu_time=1)
        Task('D', cpu, deadline=10, period=20, cpu_time=1)
        for x in range(40):
            cpu.update()

    def test_correct_simulation_2(self):
        cpu = Cpu('Cpu A')
        Task('A', cpu, deadline=5, period=5, cpu_time=3)
        Task('B', cpu, deadline=5, period=5, cpu_time=2)
        for x in range(40):
            cpu.update()


if __name__ == '__main__':
    unittest.main()
