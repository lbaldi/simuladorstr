class TaskInstance:

    def __init__(self, task: object, deadline: int, cpu_time: int) -> None:
        self.deadline = deadline
        self.cpu_time = cpu_time
        self.task = task
        task.add_instance(self)

    def update(self):
        self.deadline -= 1
        # Si la instancia tiene una tarea y es la tarea activa
        # consumo un uso de cpu
        if self.task and self.task.is_active:
            self.cpu_time -= 1
        if self.deadline == 0 and self.cpu_time > 0:
            raise Exception('Task Instance couldnt be resolved')

    def sigkill(self):
        if not self.cpu_time:
            self.finish()

    def finish(self):
        self.task.remove_instance(self)
        self.task = False
