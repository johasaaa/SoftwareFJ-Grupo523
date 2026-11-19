from excepciones import (ReservaInvalidaError,OperacionNoPermitidaError,DatoInvalidoError,ServicioNoDisponibleError)

from logger import registrar_log


class Reserva:
    """
    Representa una reserva realizada por un cliente
    sobre un servicio de Software FJ.

    Permite crear, confirmar, cancelar y finalizar
    reservas mediante validaciones y excepciones.
    """

    ESTADOS_VALIDOS = ["Pendiente","Confirmada","Cancelada","Finalizada"]
def __init__(self, id_reserva, cliente, servicio, duracion):

        try:
            # Validar identificador
            if id_reserva is None or str(id_reserva).strip() == "":
                raise DatoInvalidoError(
                    "El identificador de la reserva es obligatorio.")

            # Validar cliente
            if cliente is None:
                raise DatoInvalidoError(
                    "El cliente es obligatorio para crear una reserva.")

            # Validar servicio
            if servicio is None:
                raise DatoInvalidoError(
                    "El servicio es obligatorio para crear una reserva.")

            # Validar duración
            if (
                not isinstance(duracion, (int, float))
                or isinstance(duracion, bool)
                or duracion <= 0):
                raise DatoInvalidoError(
                    "La duración debe ser un número mayor que cero.")

            # Verificar que el servicio tenga método de cálculo
            if not callable(getattr(servicio, "calcular_costo", None)):
                raise DatoInvalidoError(
                    "El servicio no tiene un método para calcular costos.")

            # Atributos de la reserva
            self._id = str(id_reserva).strip()
            self._cliente = cliente
            self._servicio = servicio
            self._duracion = duracion
            self._estado = "Pendiente"
            self._costo_total = None

            registrar_log(
                "INFO",
                f"Reserva {self._id} creada. "
                f"Cliente: {self._cliente.nombre}. "
                f"Servicio: {self._servicio.titulo}")

        except DatoInvalidoError as error:
            registrar_log(
                "ERROR",
                f"Error al crear reserva: {error}")
            raise

        except Exception as error:
            registrar_log(
                "ERROR",
                f"Error inesperado al crear reserva: {error}")

            raise ReservaInvalidaError(
                "No fue posible crear la reserva.") from error
    
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

 def confirmar(self, descuento=0, impuesto=19):

        try:
            # Verificar estado de la reserva
            if self._estado != "Pendiente":
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar la reserva {self._id}. "
                    f"Estado actual: {self._estado}.")

            # Verificar disponibilidad si el servicio
            # implementa este atributo.
            if getattr(self._servicio, "disponible", True) is False:
                raise ServicioNoDisponibleError(
                    f"El servicio {self._servicio.titulo} "
                    "no está disponible.")

            # Validar descuento
            if (
                not isinstance(descuento, (int, float))
                or isinstance(descuento, bool)
                or not 0 <= descuento <= 100):
                raise DatoInvalidoError(
                    "El descuento debe estar entre 0 y 100.")

            # Validar impuesto
            if (
                not isinstance(impuesto, (int, float))
                or isinstance(impuesto, bool)
                or not 0 <= impuesto <= 100):
                raise DatoInvalidoError(
                    "El impuesto debe estar entre 0 y 100.")

            # Calcular costo base.
            # Cada servicio implementa su propio método.
            costo_base = self._servicio.calcular_costo()

            # Validar resultado del cálculo
            if (not isinstance(costo_base, (int, float))
                or isinstance(costo_base, bool)
                or costo_base < 0):
                raise DatoInvalidoError(
                    "El costo calculado por el servicio no es válido.")

            # Aplicar descuento
            valor_descuento = costo_base * (descuento / 100)

            subtotal = costo_base - valor_descuento

            # Aplicar impuesto
            valor_impuesto = subtotal * (impuesto / 100)

            # Calcular total
            self._costo_total = round(
                subtotal + valor_impuesto, 2)

            # Confirmar reserva
            self._estado = "Confirmada"

        except (OperacionNoPermitidaError,ReservaInvalidaError,ServicioNoDisponibleError,DatoInvalidoError) 
     as error:

            registrar_log(
                "ERROR",
                f"Error al confirmar reserva {self._id}: {error}")

            raise

        except Exception as error:

            registrar_log(
                "ERROR",
                f"Error inesperado al confirmar reserva "
                f"{self._id}: {error}")

            raise ReservaInvalidaError(
                "Ocurrió un error inesperado al confirmar la reserva.") 
            from error

        else:

            registrar_log("INFO",
                f"Reserva {self._id} confirmada. "
                f"Costo total: ${self._costo_total}")

            return (f"Reserva {self._id} confirmada exitosamente. "
                f"Costo total: ${self._costo_total:,.2f}")

        finally:

            registrar_log("INFO",f"Finalizó el intento de confirmación "
                f"de la reserva {self._id}.")

 def cancelar(self):

        try:

            if self._estado in ["Cancelada", "Finalizada"]:

                raise OperacionNoPermitidaError(
                    f"No se puede cancelar la reserva {self._id} "
                    f"porque ya está '{self._estado}'.")

            self._estado = "Cancelada"

            registrar_log("INFO",
                f"Reserva {self._id} cancelada correctamente.")

            return (f"Reserva {self._id} cancelada correctamente.")

        except OperacionNoPermitidaError as error:

            registrar_log("ERROR",f"Error al cancelar reserva {self._id}: {error}")

            raise

        except Exception as error:

            registrar_log("ERROR",f"Error inesperado al cancelar reserva: {error}")

            raise ReservaInvalidaError("No fue posible cancelar la reserva.") from error

        finally:

            registrar_log("INFO",f"Finalizó el intento de cancelación "
                f"de la reserva {self._id}.")
 def finalizar(self):

        try:

            if self._estado != "Confirmada":

                raise OperacionNoPermitidaError("Solo se pueden finalizar reservas confirmadas. "
                    f"Estado actual: {self._estado}.")

            self._estado = "Finalizada"

            registrar_log("INFO",
                f"Reserva {self._id} finalizada correctamente.")

            return (f"Reserva {self._id} finalizada correctamente.")

        except OperacionNoPermitidaError as error:

            registrar_log("ERROR",f"Error al finalizar reserva {self._id}: {error}")

            raise

        except Exception as error:

            registrar_log("ERROR",
                f"Error inesperado al finalizar reserva: {error}")

            raise ReservaInvalidaError("No fue posible finalizar la reserva.") from error

        finally:

            registrar_log("INFO",
                f"Finalizó el intento de finalización "
                f"de la reserva {self._id}.")

 def mostrar_info(self):

        costo = ( f"${self._costo_total:,.2f}"
            if self._costo_total is not None
            else "No calculado")

        nombre_servicio = self._servicio.titulo

        return (f"\n========== INFORMACION DE RESERVA ==========\n"
            f"ID: {self._id}\n"
            f"Cliente: {self._cliente.nombre}\n"
            f"Servicio: {nombre_servicio}\n"
            f"Duración: {self._duracion}\n"
            f"Estado: {self._estado}\n"
            f"Costo total: {costo}\n"
            f"============================================")
