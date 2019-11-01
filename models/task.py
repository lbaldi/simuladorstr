from models.cpu import Cpu
from models.task_instance import TaskInstance


class Task:

    def __init__(self, name: str, cpu: Cpu, deadline: int, period: int, cpu_time: int, priority: int) -> None:
        self._name = self._cpu = False
        self._deadline = self._period = self._cpu_time = 0
        self.name = name

        self.cpu = cpu
        self.period = period
        self.deadline = deadline
        self.cpu_time = cpu_time
        self.priority = priority

        self._instances = []

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError('Name value error.')
        self._name = value

    @property
    def cpu(self):
        return self._cpu

    @cpu.setter
    def cpu(self, value: Cpu):
        self._cpu and self._cpu.remove_task(self)
        self._cpu = value
        self._cpu.add_task(self)

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, value: int):
        if value <= 0:
            raise ValueError('Deadline cant be negative or zero.')
        self._deadline = value
        self._check_deadline_and_cpu_time(self.deadline, self.cpu_time)
        self._check_period_and_deadline(self.period, self.deadline)

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value: int):
        if value <= 0:
            raise ValueError('Period cant be negative or zero')
        self._period = value
        self._check_period_and_deadline(self.period, self.deadline)

    @property
    def cpu_time(self):
        return self._cpu_time

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value: int):
        self._priority = value


    @cpu_time.setter
    def cpu_time(self, value: int):
        if value <= 0:
            raise ValueError('Cpu Time cant be negative or zero')
        self._cpu_time = value
        self._check_deadline_and_cpu_time(self.deadline, self.cpu_time)
        self._check_period_and_deadline(self.period, self.deadline)

    def _check_deadline_and_cpu_time(self, deadline, cpu_time):
        if cpu_time > deadline:
            raise ValueError('Cpu Time cant be greater than Deadline')

    def _check_period_and_deadline(self, period, deadline):
        if deadline > period:
            raise ValueError('Deadline cant be greater than Period')

    def create_instance(self):
        if self.instances:
            raise Exception('Cant create a new instance if already exists one')
        return TaskInstance(self, self.deadline, self.cpu_time)

    @property
    def instances(self):
        return self._instances

    def add_instance(self, instance: object):
        self._instances.append(instance)

    def remove_instance(self, instance: object):
        self.instances.remove(instance)

    def _update_instances(self):
        for instance in self.instances:
            instance.update()

    def _check_in_period(self):
        return self.cpu.time % self.period == 0

    def update(self):
        self._update_instances()
        self._check_in_period() and self.create_instance()

    @property
    def is_active(self):
        return self.cpu.active_task == self
