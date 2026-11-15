# =================================================================
# Sistema Integral de Gestión de Clientes, Servicios y Reservas
# Empresa: Software FJ - Programación (213023) - Fase 4 - Grupo 523
#
# Archivo: cliente.py
# Responsable: Johana Camila Saavedra Figueredo
#
# Contenido:
#   - Entidad: clase abstracta que representa las entidades generales
#     del sistema (Cliente, Servicio y Reserva pueden heredar de ella).
#   - Cliente: datos personales encapsulados y validaciones estrictas.
#   - RegistroClientes: lista interna para agregar, buscar y eliminar
#     clientes, con manejo de excepciones.
#   - Registro de eventos y errores en un archivo de logs.
# =================================================================

# ABC y abstractmethod permiten crear clases abstractas
from abc import ABC, abstractmethod

# logging permite escribir eventos y errores en un archivo de texto
import logging

# Excepciones personalizadas del grupo (archivo excepciones.py)
from excepciones import (
    DatoInvalidoError,
    ClienteNoEncontradoError,
    OperacionNoPermitidaError,
)

# Configuración del archivo de logs: cada evento se guarda con
# la fecha, la hora, el nivel (INFO o ERROR) y el mensaje.
logging.basicConfig(
    filename="registro_eventos.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)


# -----------------------------------------------------------------
# CLASE ABSTRACTA: Entidad
# Representa cualquier entidad general del sistema.
# No se pueden crear objetos de esta clase directamente: solo sirve
# como molde. Obliga a sus hijas a tener descripcion() y validar().
# -----------------------------------------------------------------
class Entidad(ABC):

    # Método abstracto: cada entidad debe saber describirse
    @abstractmethod
    def descripcion(self):
        pass

    # Método abstracto: cada entidad debe saber validar sus datos
    @abstractmethod
    def validar(self):
        pass


# -----------------------------------------------------------------
# CLASE Cliente (hereda de Entidad)
# Guarda los datos personales de forma encapsulada (con _ adelante)
# y valida cada dato antes de aceptarlo.
# -----------------------------------------------------------------
class Cliente(Entidad):

    # Constructor: recibe los datos y los asigna a través de las
    # propiedades, para que cada uno pase por su validación.
    def __init__(self, nombre, documento, correo, telefono):
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---------- Nombre ----------

    # @property permite CONSULTAR el dato desde afuera: cliente.nombre
    @property
    def nombre(self):
        return self._nombre

    # @nombre.setter se ejecuta al ASIGNAR el dato: cliente.nombre = "..."
    # Aquí está la validación: si el dato es inválido, se lanza un error.
    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise DatoInvalidoError("El nombre no puede estar vacío.")
        valor = valor.strip()
        # Se quitan los espacios para revisar que solo haya letras
        if not valor.replace(" ", "").isalpha():
            raise DatoInvalidoError(f"El nombre '{valor}' solo puede contener letras.")
        if len(valor) < 3:
            raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = valor

    # ---------- Documento ----------

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        texto = str(valor).strip()
        # ENCADENAMIENTO DE EXCEPCIONES: se intenta convertir a número;
        # si falla, se lanza un DatoInvalidoError "desde" (from) el error
        # original, para conservar la causa real del problema.
        try:
            int(texto)
        except ValueError as error:
            raise DatoInvalidoError(f"El documento '{texto}' solo puede contener números.") from error
        if not (6 <= len(texto) <= 10):
            raise DatoInvalidoError("El documento debe tener entre 6 y 10 dígitos.")
        self._documento = texto

    # ---------- Correo ----------

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise DatoInvalidoError("El correo no puede estar vacío.")
        valor = valor.strip().lower()
        if " " in valor:
            raise DatoInvalidoError("El correo no puede tener espacios.")
        # Debe haber exactamente una @ y un punto después de ella
        if valor.count("@") != 1:
            raise DatoInvalidoError(f"El correo '{valor}' debe tener una @.")
        usuario, dominio = valor.split("@")
        if usuario == "" or "." not in dominio:
            raise DatoInvalidoError(f"El correo '{valor}' no tiene un formato válido.")
        self._correo = valor

    # ---------- Teléfono ----------

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        texto = str(valor).strip()
        if not texto.isdigit():
            raise DatoInvalidoError(f"El teléfono '{texto}' solo puede contener números.")
        if len(texto) != 10:
            raise DatoInvalidoError("El teléfono debe tener 10 dígitos.")
        self._telefono = texto

    # ---------- Métodos de la clase abstracta ----------

    # Sobrescritura de validar(): revisa que todos los datos existan.
    # Devuelve True si el cliente está completo.
    def validar(self):
        for dato in (self._nombre, self._documento, self._correo, self._telefono):
            if not dato:
                raise DatoInvalidoError("El cliente tiene datos incompletos.")
        return True

    # Sobrescritura de descripcion() con un parámetro opcional
    # (sobrecarga): sin datos de contacto o con ellos.
    def descripcion(self, mostrar_contacto=False):
        texto = f"Cliente: {self._nombre} | Documento: {self._documento}"
        if mostrar_contacto:
            texto += f" | Correo: {self._correo} | Teléfono: {self._telefono}"
        return texto


# -----------------------------------------------------------------
# CLASE RegistroClientes
# Administra la lista interna de clientes (sin base de datos).
# -----------------------------------------------------------------
class RegistroClientes:

    # Constructor: la lista de clientes empieza vacía
    def __init__(self):
        self._clientes = []

    # Agrega un cliente nuevo. No permite documentos repetidos.
    def agregar(self, cliente):
        if not isinstance(cliente, Cliente):
            raise OperacionNoPermitidaError("Solo se pueden registrar objetos de tipo Cliente.")
        for existente in self._clientes:
            if existente.documento == cliente.documento:
                raise OperacionNoPermitidaError(
                    f"Ya existe un cliente con el documento {cliente.documento}.")
        cliente.validar()
        self._clientes.append(cliente)
        logging.info(f"Cliente registrado: {cliente.descripcion()}")

    # Busca un cliente por documento. Si no existe, lanza un error.
    def buscar(self, documento):
        for cliente in self._clientes:
            if cliente.documento == str(documento):
                return cliente
        raise ClienteNoEncontradoError(f"No existe un cliente con el documento {documento}.")

    # Elimina un cliente por documento (usa buscar, que ya valida)
    def eliminar(self, documento):
        cliente = self.buscar(documento)
        self._clientes.remove(cliente)
        logging.info(f"Cliente eliminado: {cliente.descripcion()}")

    # Devuelve la lista de descripciones de todos los clientes
    def listar(self):
        return [cliente.descripcion() for cliente in self._clientes]


# -----------------------------------------------------------------
# PRUEBAS: operaciones válidas e inválidas con manejo de excepciones.
# El programa nunca se detiene: cada error se atrapa, se muestra
# y se guarda en el archivo registro_eventos.log
# -----------------------------------------------------------------
if __name__ == "__main__":

    registro = RegistroClientes()

    # Lista de clientes de prueba: (nombre, documento, correo, teléfono)
    datos_prueba = [
        ("Laura Gómez", "1023456789", "laura.gomez@gmail.com", "3104567890"),  # válido
        ("Carlos Pérez", "52789456", "carlos@hotmail.com", "3209876543"),      # válido
        ("", "1234567", "vacio@gmail.com", "3001112233"),                      # nombre vacío
        ("Ana María", "12AB45", "ana@gmail.com", "3001112233"),                # documento con letras
        ("Pedro Ruiz", "98765432", "pedro.gmail.com", "3001112233"),           # correo sin @
        ("Sofía Díaz", "11223344", "sofia@gmail.com", "300111"),               # teléfono corto
        ("Laura Gómez", "1023456789", "otra@gmail.com", "3115556677"),         # documento repetido
    ]

    # Operaciones de registro: try / except / else / finally
    for numero, datos in enumerate(datos_prueba, start=1):
        print(f"\nOperación {numero}: registrar a {datos[0] or '(sin nombre)'}")
        try:
            cliente = Cliente(*datos)          # puede lanzar DatoInvalidoError
            registro.agregar(cliente)          # puede lanzar OperacionNoPermitidaError
        except DatoInvalidoError as error:
            print(f"  Dato inválido: {error}")
            logging.error(f"Operación {numero} - Dato inválido: {error}")
        except OperacionNoPermitidaError as error:
            print(f"  Operación no permitida: {error}")
            logging.error(f"Operación {numero} - Operación no permitida: {error}")
        else:
            # else solo se ejecuta si NO hubo ningún error
            print(f"  Registrado correctamente -> {cliente.descripcion()}")
        finally:
            # finally se ejecuta SIEMPRE, con error o sin error
            print("  Operación finalizada.")

    # Operación de búsqueda exitosa y fallida
    for documento in ("52789456", "99999999"):
        print(f"\nBuscar cliente con documento {documento}")
        try:
            encontrado = registro.buscar(documento)
        except ClienteNoEncontradoError as error:
            print(f"  {error}")
            logging.error(f"Búsqueda fallida: {error}")
        else:
            print(f"  Encontrado -> {encontrado.descripcion(mostrar_contacto=True)}")

    # Resumen final: el programa llegó hasta aquí sin detenerse
    print("\nClientes registrados:")
    for texto in registro.listar():
        print(f"  - {texto}")
    print("\nLos eventos y errores quedaron guardados en registro_eventos.log")
