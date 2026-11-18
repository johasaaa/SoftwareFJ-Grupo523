from exepciones import ReservaInvalidaError, OperacionNoPermitidaError, DatoInvalidoError
from logger import registrar_log


class Reserva:
    """
    Representa una reserva realizada por un cliente sobre un servicio.
    Incluye confirmación, cancelación y finalización con manejo de excepciones.
    """

    ESTADOS_VALIDOS = ["Pendiente", "Confirmada", "Cancelada", "Finalizada"]

    def __init__(self, id_reserva, cliente, servicio, duracion):
        if cliente is None:
            raise DatoInvalidoError("El cliente es obligatorio para crear una reserva")
        if servicio is None:
            raise DatoInvalidoError("El servicio es obligatorio para crear una reserva")
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatoInvalidoError("La duración debe ser un número mayor que 0")

        self._id = id_reserva
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "Pendiente"
        self._costo_total = None

        registrar_log("INFO", f"Reserva {self._id} creada - Cliente: {cliente.nombre} - Servicio: {servicio.nombre}")

    # Propiedades
    @property
    def id(self):
        return self._id

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    # Métodos principales
    def confirmar(self, descuento=0, impuesto=0.19):
        """Confirma la reserva y calcula el costo"""
        try:
            if self._estado != "Pendiente":
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar la reserva {self._id} porque su estado es '{self._estado}'"
                )

            if not self._servicio.disponible:
                raise ReservaInvalidaError(
                    f"No se puede confirmar: el servicio '{self._servicio.nombre}' no está disponible"
                )

            self._costo_total = self._servicio.calcular_costo(self._duracion, descuento, impuesto)
            self._estado = "Confirmada"

            registrar_log("INFO", f"Reserva {self._id} confirmada - Costo: ${self._costo_total}")
            return f"Reserva {self._id} confirmada exitosamente. Costo total: ${self._costo_total}"

        except (OperacionNoPermitidaError, ReservaInvalidaError) as e:
            registrar_log("ERROR", str(e))
            raise

    def cancelar(self):
        """Cancela la reserva si está en estado Pendiente o Confirmada"""
        try:
            if self._estado in ["Cancelada", "Finalizada"]:
                raise OperacionNoPermitidaError(
                    f"No se puede cancelar la reserva {self._id} porque ya está '{self._estado}'"
                )

            self._estado = "Cancelada"
            registrar_log("INFO", f"Reserva {self._id} cancelada")
            return f"Reserva {self._id} cancelada correctamente"

        except OperacionNoPermitidaError as e:
            registrar_log("ERROR", str(e))
            raise

    def finalizar(self):
        """Marca la reserva como finalizada"""
        try:
            if self._estado != "Confirmada":
                raise OperacionNoPermitidaError(
                    f"Solo se pueden finalizar reservas confirmadas. Estado actual: {self._estado}"
                )

            self._estado = "Finalizada"
            registrar_log("INFO", f"Reserva {self._id} finalizada")
            return f"Reserva {self._id} finalizada correctamente"

        except OperacionNoPermitidaError as e:
            registrar_log("ERROR", str(e))
            raise

    def mostrar_info(self):
        costo = f"${self._costo_total}" if self._costo_total is not None else "No calculado"
        return (f"Reserva ID: {self._id} | Cliente: {self._cliente.nombre} | "
                f"Servicio: {self._servicio.nombre} | Duración: {self._duracion}h | "
                f"Estado: {self._estado} | Costo: {costo}")
