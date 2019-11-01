import sys
sys.path.append('.')
import unittest
from unittest.mock import Mock
from models.cpu import Cpu


class CpuTestCase(unittest.TestCase):

    def setUp(self) -> None:
        name = 'Demo Cpu'
        self.cpu_demo = Cpu(name)
        self.task_demo = Mock()

    def test_gets(self):
        name = 'Cpu A'
        cpu_a = Cpu(name)
        self.assertEqual(name, cpu_a.name)

    def test_cpu_initial_time_is_0(self):
        name = 'Cpu A'
        cpu_a = Cpu(name)
        self.assertEqual(0, cpu_a.time)

    def test_cpu_initial_tasks_is_empty(self):
        name = 'Cpu A'
        cpu_a = Cpu(name)
        self.assertFalse(cpu_a.tasks)

    def test_cpu_assign_task(self):
        tasks_len = len(self.cpu_demo.tasks)
        self.cpu_demo.add_task(self.task_demo)
        self.assertEqual(tasks_len + 1, len(self.cpu_demo.tasks))

    def test_cpu_remove_task(self):
        tasks_len = len(self.cpu_demo.tasks)
        self.cpu_demo.add_task(self.task_demo)
        self.cpu_demo.remove_task(self.task_demo)
        self.assertEqual(tasks_len, len(self.cpu_demo.tasks))

    def test_cpu_add_one_time_after_update(self):
        initial_time = self.cpu_demo.time
        self.cpu_demo.update()
        self.assertEqual(initial_time + 1, self.cpu_demo.time)

    def test_proritize_task_by_deadline(self):
        task_a = self.task_demo.copy()
        task_a.deadline = 10
        self.cpu_demo.add_task(task_a)

        task_b = self.task_demo.copy()
        task_b.deadline = 20
        self.cpu_demo.add_task(task_b)

        task_c = self.task_demo.copy()
        task_c.deadline = 30
        self.cpu_demo.add_task(task_c)

        self.assertEqual(self.cpu_demo.tasks[0].deadline, task_a.deadline)
        self.cpu_demo.prioritize_tasks()
        self.assertEqual(self.cpu_demo.tasks[0], task_b)


if __name__ == '__main__':
    unittest.main()
