
class TaskInstance:

    def __init__(self, task: object, deadline: int, cpu_time: int) -> None:
        self.deadline = deadline
        self.cpu_time = cpu_time
        self.task = task
        task.add_instance(self)

    def update(self):
        self.deadline -= 1
        if self.task.is_active:
            self.cpu_time -= 1
        # @TODO
        # Si llego a 0 me deberia borrar
