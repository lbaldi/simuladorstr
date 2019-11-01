import unittest
from models.task_instance import TaskInstance
from unittest.mock import Mock


class TaskInstanceTestCase(unittest.TestCase):

    def setUp(self) -> None:
        deadline = 0
        cpu_time = 0
        task = Mock()
        self.task_instance_demo = TaskInstance(task, deadline, cpu_time)

    def test_gets(self):
        deadline = 0
        cpu_time = 0
        task = Mock()
        task_instance_a = TaskInstance(task, deadline, cpu_time)
        self.assertEqual(deadline, task_instance_a.deadline)
        self.assertEqual(cpu_time, task_instance_a.cpu_time)
        self.assertEqual(task, task_instance_a.task)

    def test_update_instance_decrease_deadline(self):
        deadline = self.task_instance_demo.deadline
        self.task_instance_demo.update()
        self.assertEqual(deadline - 1, self.task_instance_demo.deadline)

    def test_update_instance_with_active_task_decrease_cpu_time(self):
        deadline = 0
        cpu_time = 0
        task = Mock()
        task.is_active = True
        task_instance = TaskInstance(task, deadline, cpu_time)
        cpu_time = task_instance.cpu_time
        task_instance.update()
        self.assertEqual(cpu_time - 1, task_instance.cpu_time)

    def test_after_finished_instance_doesnt_have_task(self):
        deadline = 0
        cpu_time = 0
        task = Mock()
        task.is_active = True
        task_instance = TaskInstance(task, deadline, cpu_time)
        task_instance.finish()
        self.assertFalse(task_instance.task)

if __name__ == '__main__':
    unittest.main()
