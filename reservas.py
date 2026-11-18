
import logging
import uuid
from datetime import datetime

# CONFIGURACIÓN DEL ARCHIVO DE REGISTRO DE ERRORES

logging.basicConfig(
    filename="logs_reservas.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# EXCEPCIONES PERSONALIZADAS

class ErrorReserva(Exception):
    """Excepción general del sistema de reservas."""
    pass


class DatosReservaInvalidos(ErrorReserva):
    """Se presenta cuando los datos de la reserva son incorrectos."""
    pass


class ReservaNoPermitida(ErrorReserva):
    """Se presenta cuando una operación no está permitida."""
    pass


class ServicioNoDisponible(ErrorReserva):
    """Se presenta cuando el servicio no está disponible."""
    pass

# CLASE RESERVA

class Reserva:

    def __init__(self, cliente, servicio, duracion):

        try:
            # Validar que exista un cliente y un servicio
            if cliente is None:
                raise DatosReservaInvalidos(
                    "El cliente no puede estar vacío."
                )

            if servicio is None:
                raise DatosReservaInvalidos(
                    "El servicio no puede estar vacío."
                )

            # Validar la duración
            if not isinstance(duracion, (int, float)) or isinstance(duracion, bool):
                raise DatosReservaInvalidos(
                    "La duración debe ser un número."
                )

            if duracion <= 0:
                raise DatosReservaInvalidos(
                    "La duración debe ser mayor que cero."
                )

            # Encapsulamiento de atributos
            self.__id = str(uuid.uuid4())[:8]
            self.__cliente = cliente
            self.__servicio = servicio
            self.__duracion = duracion
            self.__estado = "Pendiente"
            self.__fecha_creacion = datetime.now()
            self.__costo = 0

        except DatosReservaInvalidos as error:
            logging.exception("Error al crear una reserva.")
            raise

        except Exception as error:
            logging.exception("Error inesperado al crear la reserva.")
            raise ErrorReserva(
                "No fue posible crear la reserva."
            ) from error

    # PROPIEDADES PARA CONSULTAR LOS DATOS

    @property
    def id(self):
        return self.__id

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    # MÉTODO PARA CONFIRMAR LA RESERVA

    def confirmar(self):

        try:
            if self.__estado != "Pendiente":
                raise ReservaNoPermitida(
                    "Solo se pueden confirmar reservas pendientes."
                )

            # Validar los parámetros del servicio
            if hasattr(self.__servicio, "validar_parametros"):

                resultado = self.__servicio.validar_parametros(
                    self.__duracion
                )

                if resultado is False:
                    raise ServicioNoDisponible(
                        "El servicio no acepta los parámetros indicados."
                    )

            self.__estado = "Confirmada"

            print(f"Reserva {self.__id} confirmada correctamente.")

            return True

        except ErrorReserva as error:
            logging.exception("Error al confirmar la reserva.")
            raise

        except Exception as error:
            logging.exception("Error inesperado al confirmar.")
            raise ErrorReserva(
                "No se pudo confirmar la reserva."
            ) from error
          
    # MÉTODO PARA CANCELAR LA RESERVA

    def cancelar(self):

        try:
            if self.__estado == "Cancelada":
                raise ReservaNoPermitida(
                    "La reserva ya se encuentra cancelada."
                )

            if self.__estado == "Finalizada":
                raise ReservaNoPermitida(
                    "No se puede cancelar una reserva finalizada."
                )

            self.__estado = "Cancelada"
            self.__costo = 0

            print(f"Reserva {self.__id} cancelada correctamente.")

            return True

        except ErrorReserva as error:
            logging.exception("Error al cancelar la reserva.")
            raise

        except Exception as error:
            logging.exception("Error inesperado al cancelar.")
            raise ErrorReserva(
                "No se pudo cancelar la reserva."
            ) from error

    # MÉTODO PARA PROCESAR LA RESERVA

    def procesar(self, impuesto=0, descuento=0):

        try:
            # Verificar que la reserva esté confirmada
            if self.__estado != "Confirmada":
                raise ReservaNoPermitida(
                    "La reserva debe estar confirmada para procesarse."
                )

            # Validar impuesto y descuento
            if not isinstance(impuesto, (int, float)) or isinstance(impuesto, bool):
                raise DatosReservaInvalidos(
                    "El impuesto debe ser numérico."
                )

            if not isinstance(descuento, (int, float)) or isinstance(descuento, bool):
                raise DatosReservaInvalidos(
                    "El descuento debe ser numérico."
                )

            if impuesto < 0 or impuesto > 100:
                raise DatosReservaInvalidos(
                    "El impuesto debe estar entre 0 y 100."
                )

            if descuento < 0 or descuento > 100:
                raise DatosReservaInvalidos(
                    "El descuento debe estar entre 0 y 100."
                )

            # Obtener el costo mediante polimorfismo
            costo_base = self.__servicio.calcular_costo(
                self.__duracion
            )

            if not isinstance(costo_base, (int, float)) or isinstance(costo_base, bool):
                raise DatosReservaInvalidos(
                    "El costo calculado no es válido."
                )

            if costo_base < 0:
                raise DatosReservaInvalidos(
                    "El costo no puede ser negativo."
                )

            # Aplicar descuento e impuesto
            valor_descuento = costo_base * (descuento / 100)
            subtotal = costo_base - valor_descuento
            valor_impuesto = subtotal * (impuesto / 100)

            self.__costo = round(subtotal + valor_impuesto, 2)

            # Cambiar estado
            self.__estado = "Finalizada"

            print("\nRESERVA PROCESADA EXITOSAMENTE")
            print("--------------------------------")
            print(f"Identificador: {self.__id}")
            print(f"Costo base: ${costo_base:,.2f}")
            print(f"Descuento: {descuento}%")
            print(f"Impuesto: {impuesto}%")
            print(f"Total a pagar: ${self.__costo:,.2f}")
            print(f"Estado: {self.__estado}")

            return self.__costo

        except ErrorReserva as error:
            logging.exception("Error al procesar la reserva.")
            raise

        except Exception as error:
            logging.exception("Error inesperado durante el procesamiento.")
            raise ErrorReserva(
                "Ocurrió un error al procesar la reserva."
            ) from error

        else:
            print("Procesamiento terminado correctamente.")

        finally:
            print("Finalizó el intento de procesamiento de la reserva.")

    # MÉTODO PARA CONSULTAR LA INFORMACIÓN

    def mostrar_informacion(self):

        print("\n========= INFORMACIÓN DE LA RESERVA =========")
        print(f"ID: {self.__id}")
        print(f"Cliente: {self.__cliente}")
        print(f"Servicio: {self.__servicio}")
        print(f"Duración: {self.__duracion}")
        print(f"Estado: {self.__estado}")
        print(f"Costo: ${self.__costo:,.2f}")
        print(f"Fecha: {self.__fecha_creacion}")
        print("=============================================")
