from abc import ABC, abstractmethod

# Excepcion personalizada para controlar errores especificos en los servicios
class DatoInvalidoError(Exception):
     """Excepcion personalizada para indicar que un dato es invalido"""
  def __init__(self, mensaje="el dato proporcionado es invalido."):
      self.mensaje = mensaje 
      super().__init__(self.mensaje)
      
class ServicioNoDisponibleError(Exception):
     """ Excepcion personalizada paraindicar que un servicio noestabdisponible."""
     def __init__(self, mensaje="el servicio solicitado no esta disponible."):
         self.mensaje = mensaje
         super().__init__(self.mensaje)
                  

# clase abstracta servicio (entidad base del sistema)
class Servicio(ABC):
    def __init__(self, titulo: str, tarifa_base: float):
        if tarifa_base < 0:
          raise DatoInvalidoError("la tarifa base no puede ser negativa.")
        self._titulo = titulo
        self._tarifa_base = tarifa_base

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @abstractmethod
    def calcular_costo(self) -> float:
         """metodo abstracto obligatorio para calcular costos."""
         pass

    @abstractmethod
    def obtener_descripccion(self) -> str:
        """ metodo abstracto obligatorio para la descricion."""
         pass
         

# Servicio especializado: sala
class ServicioSala(Servicio):
      def __init__(self, tarifa_base: float, capacidad: int, total_horas: int):
          super().__init__("Alquiler de sala", tarifa_base)
          if capacidad <= 0 or total_horas <= 0:
               raise DatoInvalidoError("la capacidad y las horas deben ser mayores a cero.")
          self._capacidad = capacidad
          self._total_horas = total_horas

      def calcular_costo(self, porcentaje_descuento: float =0.0) -> float:
         try:
             if not (0 <= porcentaje_descuento <= 100):
                 raise ValueError("el descuento tiene que estarentre 0 y 100.")
             recargo_espacio = self._capacidad *4000
             subtotal = (self._tarifa_base * self._total_horas) + recargo_espacio
             descuento_aplicado = subtotal * (porcentaje_descuento / 100)
             return subtotal - descuento_aplicado
         except Exception as e:
              raise  DatoInvalidoError(f" error al calcular la sala: {e}")

      def obtener_descripcion(self) -> str:
          return (f"servicio: {self._titulo} | capacidad: {self._capacidad} personas"
                  f"| horas: {self._total_horas} | costo final: $ {self.calcular_costo():,.2f}")


# servicio especializado: equipos
class ServicioEquipos(Servicio):
     def __init__(self, tarifa_base: float, num_equipos: int,dias_alquiler: int):
         super().__init__("prestamo de equipos", tarifa_base)
         if num_equipos <= 0 or dias_alquiler <= 0:
             raise DatoInvalidoError("la cantidad de equipos y dias deben ser positivos")
         self._num_equipos = num_equipos
         self._dias_alquiler = dias_alquiler

     def calcular_costo(self, incluir_soporte: bool = False) -> float:
         costo_total = self._tarifa_base * self._num_equipos * self._dias_alquiler
         if incluir_soporte:
             costo_total += 15000 * self._num_equipos
             return costo_total

     def obtener_descripcion(self) -> str:
         return (f"servicio: {self._titulo} | equipos: { self._num_equipos} "
                 f"| dias: {self._dias_alquiler} | costo final: ${self.calcular_costo():,.2f}")


# servicio especializado :asesoria
class ServicioAsesoria(Servicio):
    def __init__(self, tarifa_base: float, area_asesoria: str, sesiones: int):
       super().__init__("asesoria especializada", tarifa_base)
       if not area_asesoria.strip():
           raise DatoInvalidoError("el area de asesoria no puede estar vacia.")
       if sesiones <= 0:
           raise DatoInvalidoError("las sesiones deben ser mayores a cero")
       self._area_asesoria = area_asesoria
       self._sesiones = sesiones

    def calcular_costo(self, es_paquete_empresarial: bool = False) -> float:
        total = self._tarifa_base * self._sesiones
        if es_paquete_empresarial:
            total *=0.88
        return total

    def obtener_descripcion(self) -> str:
     return (f"servicio: {self._titulo} | Area: {self._area_asesoria} "
             f"| sesiones: {self._sesiones} | costo final: ${self.calcular_costo():,.2f}")
             

       
      
