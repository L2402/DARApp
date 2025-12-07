import time


class Command:
    def execute(self):
        raise NotImplementedError()


class PlayCommand(Command):
    def __init__(self, reproductor, url):
        self.reproductor = reproductor
        self.url = url

    def execute(self):
        self.reproductor.reproducir(self.url)


class PauseCommand(Command):
    def __init__(self, reproductor):
        self.reproductor = reproductor

    def execute(self):
        self.reproductor.pausar()


class StopCommand(Command):
    def __init__(self, reproductor):
        self.reproductor = reproductor

    def execute(self):
        self.reproductor.detener()


class RepeatCommand(Command):
    def __init__(self, reproductor):
        self.reproductor = reproductor

    def execute(self):
        self.reproductor.repetir()


class AddToCommand(Command):
    def __init__(self, reproductor, cancion):
        self.reproductor = reproductor
        self.cancion = cancion

    def execute(self):
        # Usa el método existente para preguntar dónde agregar la canción
        self.reproductor.pregunta(self.cancion)


class ControlInvoker:
    def __init__(self):
        self._commands = {}

    def set_command(self, key, command):
        self._commands[key] = command

    def handle(self, key):
        cmd = self._commands.get(key)
        if cmd:
            cmd.execute()
            # Pequeño retardo opcional para evitar múltiples ejecuciones por rebote de tecla
            time.sleep(0.12)