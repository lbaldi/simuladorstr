import pprint

class Cpu:

    def __init__(self, name: str) -> None:
        self._name = self._time = self._tasks = False
        self.name = name
        self._time = 0
        self._tasks = []

    def __str__(self):
        return self.name

    def status(self):

        status_dict = {
            'name': self.name,
            'active_task': self.active_task.name if self.active_task else None,
            'time': self.time,
            'tasks': [],
        }

        for task in self.tasks:

            task_status = {
                'name': task.name,
                'period': task.period,
                'deadline': task.deadline,
                'instances': [],
                'active': task.is_active,
            }

            status_dict.get('tasks').append(task_status)

            for instance in task.instances:
                instance_status = {
                    'name': instance,
                    'deadline': instance.deadline,
                    'cpu_time': instance.cpu_time,
                }

                task_status.get('instances').append(instance_status)

        return status_dict

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def time(self):
        return self._time

    @property
    def tasks(self):
        return self._tasks

    def add_task(self, task: object):
        self._tasks.append(task)

    def remove_task(self, task: object):
        self.tasks.remove(task)

    def _update_tasks(self):
        for task in self.tasks:
            task.update()
        for task in self.tasks:
            task.sigkill()

    def _print_status(self):
        pprint.pprint(self.status())
        print('\n\n\n')

    def update(self):
        self._print_status()
        self._update_tasks()
        self._time += 1

    def prioritize_tasks(self) -> list:
        instances = []
        for task in self.tasks:
            instances.extend(task.instances)
        if instances:
            return instances[0].task

    @property
    def active_task(self) -> object:
        return self.prioritize_tasks()