import unittest
from models.task import Task
from unittest.mock import Mock


class TaskTestCase(unittest.TestCase):

    def setUp(self) -> None:
        name = 'Demo Task'
        cpu = Mock()
        deadline = 0
        period = 0
        cpu_time = 0
        self.task_demo = Task(name, cpu, deadline, period, cpu_time)

    def test_gets(self):
        name = 'Task A'
        cpu = Mock()
        deadline = 0
        period = 0
        cpu_time = 0
        task_a = Task(name, cpu, deadline, period, cpu_time)
        self.assertEqual(name, task_a.name)
        self.assertEqual(cpu, task_a.cpu)
        self.assertEqual(deadline, task_a.deadline)
        self.assertEqual(period, task_a.period)
        self.assertEqual(cpu_time, task_a.cpu_time)

    def test_set_negative_deadline(self):
        with self.assertRaises(ValueError):
            self.task_demo.deadline = -1

    def test_set_negative_period(self):
        with self.assertRaises(ValueError):
            self.task_demo.period = -1

    def test_set_negative_cpu_time(self):
        with self.assertRaises(ValueError):
            self.task_demo.cpu_time = -1

    def test_set_null_name(self):
        with self.assertRaises(ValueError):
            self.task_demo.name = False

    def test_set_cpu_time_greater_than_deadline_changing_cpu_time(self):
        self.task_demo.deadline = 1
        self.task_demo.cpu_time = 1
        with self.assertRaises(ValueError):
            self.task_demo.cpu_time = 2

    def test_set_cpu_time_greater_than_deadline_changing_deadline(self):
        self.task_demo.deadline = 1
        self.task_demo.cpu_time = 1
        with self.assertRaises(ValueError):
            self.task_demo.deadline = 0

    # @TODO
    def test_update_task(self):
        self.task_demo.update()

if __name__ == '__main__':
    unittest.main()
