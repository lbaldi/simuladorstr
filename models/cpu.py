class Cpu:

    def __init__(self, name: str) -> None:
        self._name = self._time = self._tasks = False
        self.name = name
        self._tasks = []

    def __str__(self):
        return self.name

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

    def update(self):
        self._time += 1
        self._update_tasks()

    @property
    def active_task(self):
        pass
        # @TODO
        # Aca va la logica de buscar entre las tareas quien deberia ejecutarse
        # Para este caso que no tiene prioridad voy a buscar dentro de todas las tareas
        # aquella que tenga la instancia con menor deadline