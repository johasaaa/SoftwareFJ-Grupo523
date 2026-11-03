class DatoInvalidoError(Exception):
    """Excepción personalizada para indicar que un dato es inválido."""
    def __init__(self, message="El dato proporcionado es inválido."):
        self.message = message
        super().__init__(self.message)

class ClienteNoEncontradoError(Exception):
    """Excepción personalizada para indicar que un cliente no fue encontrado."""
    def __init__(self, message="El cliente no fue encontrado."):
        self.message = message
        super().__init__(self.message)

class ServicioNoDisponibleError(Exception):
    """Excepción personalizada para indicar que un servicio no está disponible."""
    def __init__(self, message="El servicio solicitado no está disponible."):
        self.message = message
        super().__init__(self.message)

class ReservaInvalidaError(Exception):
    """Excepción personalizada para indicar que una reserva es inválida."""
    def __init__(self, message="La reserva es inválida."):
        self.message = message
        super().__init__(self.message)

class OperacionNoPermitidaError(Exception):
    """Excepción personalizada para indicar que una operación no está permitida."""
    def __init__(self, message="La operación no está permitida."):
        self.message = message
        super().__init__(self.message)
