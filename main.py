# Empresa: Software FJ - Programación (213023) - Fase 4 - Grupo 523
# Archivo: main.py
# Responsable: Yuri Natalia Ramirez Rodriguez 

# IMPORTAR CLASES EXISTENTES DEL PROYECTO

from cliente import Cliente, RegistroClientes

from servicios import (ServicioSala,ServicioEquipos,ServicioAsesoria)

from reserva import Reserva

from excepciones import (DatoInvalidoError,ClienteNoEncontradoError,ServicioNoDisponibleError,ReservaInvalidaError,OperacionNoPermitidaError)

from logger import registrar_log

# INICIO DEL PROGRAMA

print("\n" + "=" * 60)
print("       SISTEMA INTEGRAL DE GESTION SOFTWARE FJ")
print("=" * 60)

registrar_log("INFO", "Inicio del programa principal.")

# Lista interna de clientes
registro = RegistroClientes()

# Variables para almacenar los objetos creados
cliente1 = None
sala1 = None
equipos1 = None
asesoria1 = None
reserva1 = None
reserva2 = None

# OPERACION 1: REGISTRAR CLIENTE VALIDO

print("\nOPERACION 1: Registrar cliente valido")

try:

    cliente1 = Cliente(
        "Carlos Rodriguez",
        "1020304050",
        "carlos@gmail.com",
        "3104567890"
    )

    registro.agregar(cliente1)

except Exception as error:

    print("Error al registrar cliente:", error)
    registrar_log("ERROR", f"Operacion 1: {error}")

else:

    print("Cliente registrado correctamente.")
    print(cliente1.descripcion(mostrar_contacto=True))

    registrar_log("INFO", "Operacion 1: cliente registrado correctamente.")

finally:

    print("Finalizacion de operacion 1.")


# OPERACION 2: REGISTRAR CLIENTE CON CORREO INVALIDO

print("\nOPERACION 2: Registrar cliente con correo incorrecto")

try:

    cliente_invalido = Cliente("Pedro Martinez","1020304051","pedro.gmail.com","3204567890")

    registro.agregar(cliente_invalido)

except DatoInvalidoError as error:

    print("Error controlado:", error)
    registrar_log("ERROR", f"Operacion 2: correo invalido. {error}")

else:

    print("Cliente registrado correctamente.")

finally:

    print("Finalizacion de operacion 2.")


# OPERACION 3: REGISTRAR OTRO CLIENTE VALIDO

print("\nOPERACION 3: Registrar segundo cliente")

try:

    cliente2 = Cliente("Laura Gomez","1020304052","laura@gmail.com","3154567890")

    registro.agregar(cliente2)

except Exception as error:

    print("Error:", error)
    registrar_log("ERROR", f"Operacion 3: {error}")

else:

    print("Segundo cliente registrado correctamente.")
    registrar_log("INFO", "Operacion 3: segundo cliente registrado.")

finally:

    print("Finalizacion de operacion 3.")

# OPERACION 4: CREAR SERVICIO DE SALA

print("\nOPERACION 4: Crear servicio de sala")

try:

    sala1 = ServicioSala(
        tarifa_base=50000,
        capacidad=20,
        total_horas=3 )

except Exception as error:

    print("Error al crear sala:", error)
    registrar_log("ERROR", f"Operacion 4: {error}")

else:

    print("Sala creada correctamente.")
    print(sala1.obtener_descripcion())

    registrar_log("INFO", "Operacion 4: sala creada.")

finally:

    print("Finalizacion de operacion 4.")

# OPERACION 5: CREAR SERVICIO CON TARIFA NEGATIVA

print("\nOPERACION 5: Crear servicio con tarifa negativa")

try:

    sala_invalida = ServicioSala(
        tarifa_base=-50000,
        capacidad=20,
        total_horas=3)

except DatoInvalidoError as error:

    print("Error controlado:", error)
    registrar_log("ERROR", f"Operacion 5: tarifa negativa. {error}")

else:

    print("Servicio creado correctamente.")

finally:

    print("Finalizacion de operacion 5.")

# OPERACION 6: CREAR SERVICIO DE EQUIPOS

print("\nOPERACION 6: Crear servicio de alquiler de equipos")

try:

    equipos1 = ServicioEquipos(
        tarifa_base=25000,
        num_equipos=5,
        dias_alquiler=2)

except Exception as error:

    print("Error al crear servicio:", error)
    registrar_log("ERROR", f"Operacion 6: {error}")

else:

    print("Servicio de equipos creado correctamente.")
    print(equipos1.obtener_descripcion())

    registrar_log("INFO", "Operacion 6: servicio de equipos creado.")

finally:

    print("Finalizacion de operacion 6.")

# OPERACION 7: CREAR SERVICIO DE ASESORIA

print("\nOPERACION 7: Crear servicio de asesoria")

try:

    asesoria1 = ServicioAsesoria(
        tarifa_base=80000,
        area_asesoria="Contabilidad",
        sesiones=4)

except Exception as error:

    print("Error al crear asesoria:", error)
    registrar_log("ERROR", f"Operacion 7: {error}")

else:

    print("Asesoria creada correctamente.")
    print(asesoria1.obtener_descripcion())

    registrar_log("INFO", "Operacion 7: asesoria creada.")

finally:

    print("Finalizacion de operacion 7.")

# OPERACION 8: CREAR RESERVA VALIDA

print("\nOPERACION 8: Crear reserva")

try:

    if cliente1 is None or sala1 is None:
        raise ReservaInvalidaError(
            "No se puede crear la reserva sin cliente y servicio.")

    reserva1 = Reserva(
        id_reserva="R001",
        cliente=cliente1,
        servicio=sala1,
        duracion=3)

except Exception as error:

    print("Error al crear reserva:", error)
    registrar_log("ERROR", f"Operacion 8: {error}")

else:

    print("Reserva creada correctamente.")
    print(reserva1.mostrar_info())

    registrar_log("INFO", "Operacion 8: reserva R001 creada.")

finally:

    print("Finalizacion de operacion 8.")

# OPERACION 9: CONFIRMAR RESERVA

print("\nOPERACION 9: Confirmar reserva")

try:

    if reserva1 is None:
        raise ReservaInvalidaError(
            "No existe la reserva para confirmar.")

    resultado = reserva1.confirmar(
        descuento=10,
        impuesto=19)

except Exception as error:

    print("Error al confirmar:", error)
    registrar_log("ERROR", f"Operacion 9: {error}")

else:

    print(resultado)
    registrar_log("INFO", "Operacion 9: reserva confirmada.")

finally:

    print("Finalizacion de operacion 9.")

# OPERACION 10: CANCELAR RESERVA

print("\nOPERACION 10: Cancelar reserva")

try:

    if reserva1 is None:
        raise ReservaInvalidaError(
            "No existe la reserva para cancelar.")

    resultado = reserva1.cancelar()

except Exception as error:

    print("Error al cancelar:", error)
    registrar_log("ERROR", f"Operacion 10: {error}")

else:

    print(resultado)
    registrar_log("INFO", "Operacion 10: reserva cancelada.")

finally:

    print("Finalizacion de operacion 10.")

# OPERACION 11: CANCELAR NUEVAMENTE LA MISMA RESERVA

print("\nOPERACION 11: Intentar cancelar reserva nuevamente")

try:

    if reserva1 is None:
        raise ReservaInvalidaError(
            "No existe la reserva.")

    resultado = reserva1.cancelar()

except OperacionNoPermitidaError as error:

    print("Operacion no permitida:", error)
    registrar_log("ERROR", f"Operacion 11: segunda cancelacion. {error}")

except Exception as error:

    print("Error inesperado:", error)
    registrar_log("ERROR", f"Operacion 11: {error}")

else:

    print(resultado)

finally:

    print("Finalizacion de operacion 11.")

# OPERACION 12: BUSCAR CLIENTE INEXISTENTE

print("\nOPERACION 12: Buscar cliente inexistente")

try:

    cliente_buscado = registro.buscar("9999999999")

except ClienteNoEncontradoError as error:

    print("Cliente no encontrado:", error)
    registrar_log("ERROR", f"Operacion 12: {error}")

else:

    print("Cliente encontrado:", cliente_buscado.descripcion())

finally:

    print("Finalizacion de operacion 12.")

# OPERACION 13: CREAR RESERVA CON DURACION INVALIDA

print("\nOPERACION 13: Crear reserva con duracion negativa")

try:

    reserva_invalida = Reserva(
        id_reserva="R002",
        cliente=cliente1,
        servicio=sala1,
        duracion=-5)

except DatoInvalidoError as error:

    print("Datos invalidos:", error)
    registrar_log("ERROR", f"Operacion 13: {error}")

else:

    print("Reserva creada correctamente.")

finally:

    print("Finalizacion de operacion 13.")

# OPERACION 14: FINALIZAR UNA RESERVA CONFIRMADA

print("\nOPERACION 14: Crear y finalizar una segunda reserva")

try:

    if cliente2 is None or equipos1 is None:
        raise ReservaInvalidaError(
            "No existen los datos necesarios para crear la reserva.")

    reserva2 = Reserva(
        id_reserva="R003",
        cliente=cliente2,
        servicio=equipos1,
        duracion=2)

    reserva2.confirmar(
        descuento=5,
        impuesto=19)

    resultado = reserva2.finalizar()

except Exception as error:

    print("Error al finalizar reserva:", error)
    registrar_log("ERROR", f"Operacion 14: {error}")

else:

    print(resultado)
    print(reserva2.mostrar_info())

    registrar_log("INFO", "Operacion 14: reserva R003 finalizada.")

finally:

    print("Finalizacion de operacion 14.")


# OPERACION 15: MOSTRAR CLIENTES REGISTRADOS

print("\nOPERACION 15: Consultar clientes registrados")

try:

    clientes = registro.listar()

    if not clientes:
        raise ClienteNoEncontradoError(
            "No hay clientes registrados.")

except Exception as error:

    print("Error al consultar clientes:", error)
    registrar_log("ERROR", f"Operacion 15: {error}")

else:

    print("\nCLIENTES REGISTRADOS:")

    for cliente in clientes:
        print("-", cliente)

    registrar_log("INFO", "Operacion 15: listado de clientes consultado.")

finally:

    print("Finalizacion de operacion 15.")

# RESUMEN FINAL DEL SISTEMA

print("\n" + "=" * 60)
print("       FINALIZACION DEL SISTEMA SOFTWARE FJ")
print("=" * 60)

print("Todas las operaciones de prueba fueron ejecutadas.")
print("Los errores detectados fueron controlados.")
print("Los eventos y errores quedaron registrados en logs.txt.")

registrar_log(
    "INFO",
    "Finalizacion del programa principal. "
    "Se ejecutaron las 15 operaciones.")

print("\nPrograma finalizado correctamente.")
