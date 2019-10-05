from models.cpu import Cpu


class Task:

    def __init__(self, name: str, cpu: Cpu, deadline: int, period: int, cpu_time: int) -> None:
        self._name = self._cpu = self._deadline = self._period = self._cpu_time = False
        self.name = name
        self.cpu = cpu
        self.deadline = deadline
        self.period = period
        self.cpu_time = cpu_time

        # @TODO
        # Se debe borrar es solo para probar la arquitectura de notificaciones.
        self.time = 0

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
        if value < 0:
            raise ValueError('Deadline cant be negative.')
        self._deadline = value
        self._check_deadline_and_cpu_time(self.deadline, self.cpu_time)

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value: int):
        if value < 0:
            raise ValueError('Period cant be negative')
        self._period = value

    @property
    def cpu_time(self):
        return self._cpu_time

    @cpu_time.setter
    def cpu_time(self, value: int):
        if value < 0:
            raise ValueError('Cpu Time cant be negative')
        self._cpu_time = value
        self._check_deadline_and_cpu_time(self.deadline, self.cpu_time)

    def _check_deadline_and_cpu_time(self, deadline, cpu_time):
        if cpu_time > deadline:
            raise ValueError('Cpu Time cant be greater than Deadline')

    # @TODO
    # Aca deberiamos actualizar el estado de la tarea en base a la señal del cpu
    # En todos los casos se deberia decrementar el deadline actual
    # En caso de ser la tarea activa deberia incrementar el cpu_time actual
    # Si una tarea llega a tener cpu_time real al cpu_time base la tarea deberia finalizar
    # Si una tarea llega a deadline real 0 y aun el cpu_time real no llega al cpu_time base, falla la simulacion.
    # Falta agregar al modelo deadline real y cpu_time real o ver si gestionamos esto desde una nueva clase TaskInstance
    # Solo para probar vamos a agregar un atribute time en la tarea e incrementarlo
    def update(self):
        self.time += 1
        print('NAME {} TIME {}'.format(self, self.time))