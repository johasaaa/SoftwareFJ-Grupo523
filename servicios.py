from abc import ABC, abstractmethod

# excepcion personalizada para controlar errores especificos en los servicios
class errorservicioNoValido(Excepyion):
  def __init__(self, mensaje="el servicio presenta un vañor oparametro no valido."):
      super().__init__(mensaje)
      pass

# clase abstracta servicio (entidad base del sistema)
class servicio(ABC):
    def __init__(self, titulo: str, tarifa_base: float):
        if tarifa_base < 0:
          raise ErrordeservicioNoValido("la tarifa base no puede ser negativa.")
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
      
