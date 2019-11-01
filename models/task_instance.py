
class TaskInstance:

    def __init__(self, task: object, deadline: int, cpu_time: int) -> None:
        self.deadline = deadline
        self.cpu_time = cpu_time
        self.task = task
        task.add_instance(self)

    def update(self):
        self.deadline -= 1
        if self.task and self.task.is_active:
            self.cpu_time -= 1
        if not self.cpu_time:
            self.finish()

    def finish(self):
        self.task.remove_instance(self)
        self.task = False