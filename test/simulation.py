import unittest
from models.cpu import Cpu
from models.task import Task


class SimulationTestCase(unittest.TestCase):

    def test_updated_task_after_cpu_udpate(self):
        cpu_a = Cpu('Cpu A')
        deadline = period = 10
        cpu_time = 5
        Task('A', cpu_a, deadline, period, cpu_time)
        Task('B', cpu_a, deadline, period, cpu_time)
        cpu_a.update()


if __name__ == '__main__':
    unittest.main()
