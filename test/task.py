import unittest
from models.task import Task
from unittest.mock import Mock


class TaskTestCase(unittest.TestCase):

    def setUp(self) -> None:
        name = 'Demo Task'
        cpu = Mock()
        cpu.time = 0
        deadline = 1
        period = 1
        cpu_time = 1
        self.task_demo = Task(name, cpu, deadline, period, cpu_time)

    def test_gets(self):
        name = 'Task A'
        cpu = Mock()
        deadline = 1
        period = 1
        cpu_time = 1
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
        self.task_demo.period = 1
        self.task_demo.deadline = 1
        self.task_demo.cpu_time = 1
        with self.assertRaises(ValueError):
            self.task_demo.cpu_time = 2

    def test_set_cpu_time_greater_than_deadline_changing_deadline(self):
        self.task_demo.period = 1
        self.task_demo.deadline = 1
        self.task_demo.cpu_time = 1
        with self.assertRaises(ValueError):
            self.task_demo.deadline = 0

    def test_set_deadline_greater_than_period_changing_period(self):
        self.task_demo.period = 1
        self.task_demo.deadline = 1
        self.task_demo.cpu_time = 1
        with self.assertRaises(ValueError):
            self.task_demo.period = 0

    def test_set_deadline_greater_than_period_changing_deadline(self):
        self.task_demo.period = 1
        self.task_demo.deadline = 1
        self.task_demo.cpu_time = 1
        with self.assertRaises(ValueError):
            self.task_demo.deadline = 2

    def test_task_initial_instance_is_empty(self):
        self.assertFalse(self.task_demo.instances)

    def test_task_add_instance(self):
        instance_len = len(self.task_demo.instances)
        self.task_demo.add_instance(Mock())
        self.assertEqual(instance_len + 1, len(self.task_demo.instances))

    def test_task_remove_instance(self):
        instance_len = len(self.task_demo.instances)
        task = Mock()
        self.task_demo.add_instance(task)
        self.task_demo.remove_instance(task)
        self.assertEqual(instance_len, len(self.task_demo.instances))

    def test_task_create_instance_return_object(self):
        instance = self.task_demo.create_instance()
        self.assertIsInstance(instance, object)

    def test_error_creating_a_task_already_having_one(self):
        self.task_demo.create_instance()
        with self.assertRaises(Exception):
            self.task_demo.create_instance()

    def test_update_task_when_period_divisible_create_instance(self):
        self.task_demo.period = 10
        self.task_demo.cpu.time = 20
        instance_len = len(self.task_demo.instances)
        self.task_demo.update()
        self.assertEqual(instance_len + 1, len(self.task_demo.instances))

    def test_update_task_when_period_not_divisible_dont_create_instance(self):
        self.task_demo.period = 10
        self.task_demo.cpu.time = 17
        instance_len = len(self.task_demo.instances)
        self.task_demo.update()
        self.assertEqual(instance_len, len(self.task_demo.instances))

    def test_active_when_task_is_not_active_in_cpu(self):
        self.task_demo.cpu.active_task = Mock()
        self.assertFalse(self.task_demo.is_active)

    def test_active_when_task_is_active_in_cpu(self):
        self.task_demo.cpu.active_task = self.task_demo
        self.assertTrue(self.task_demo.is_active)

    def test_check_in_period_not_divisible(self):
        self.task_demo.period = 10
        self.task_demo.cpu.time = 5
        self.assertFalse(self.task_demo._check_in_period())

    def test_check_in_period_divisible(self):
        self.task_demo.period = 10
        self.task_demo.cpu.time = 20
        self.assertTrue(self.task_demo._check_in_period())


if __name__ == '__main__':
    unittest.main()
