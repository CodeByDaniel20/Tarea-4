# Archivo para gestionar servicios - versión orientada a objetos
from excepciones import *
from abc import ABC, abstractmethod
import math


def formatear_cop(valor):
	"""Formatea un número como moneda COP sin decimales."""
	return f"$ {valor:,.0f} COP".replace(",", ".")


class Servicio(ABC):
	"""Clase abstracta que representa un servicio genérico."""

	def __init__(self, nombre: str, disponible: bool = True, base_cost: float = 0.0):
		self._nombre = nombre
		self._disponible = bool(disponible)
		self._base_cost = float(base_cost)

	def get_nombre(self):
		return self._nombre

	def esta_disponible(self):
		return self._disponible

	def set_disponible(self, disponible: bool):
		self._disponible = bool(disponible)

	@abstractmethod
	def calcular_costo(self, duration_hours: float, impuesto: float = 0.0, descuento: float = 0.0):
		"""Calcula el costo del servicio según la duración y parámetros opcionales.

		Debe devolver el costo final (float).
		"""

	@abstractmethod
	def descripcion(self):
		"""Descripción textual del servicio."""


class Sala(Servicio):
	def __init__(self, nombre="Sala", disponible=True, base_cost_per_hour=120000.0):
		super().__init__(nombre, disponible, base_cost_per_hour)

	def calcular_costo(self, duration_hours: float, impuesto: float = 0.0, descuento: float = 0.0):
		cost = self._base_cost * max(0.0, duration_hours)
		cost = cost * (1 + float(impuesto))
		cost = cost * (1 - float(descuento))
		return round(cost, 2)

	def descripcion(self):
		return f"Sala - {self._nombre} (por hora: {formatear_cop(self._base_cost)})"


class AlquilerEquipo(Servicio):
	def __init__(self, nombre="AlquilerEquipo", disponible=True, base_cost_per_day=300000.0):
		# store base_cost as per-day
		super().__init__(nombre, disponible, base_cost_per_day)

	def calcular_costo(self, duration_hours: float, impuesto: float = 0.0, descuento: float = 0.0):
		days = math.ceil(max(0.0, duration_hours) / 24.0)
		cost = self._base_cost * days
		cost = cost * (1 + float(impuesto))
		cost = cost * (1 - float(descuento))
		return round(cost, 2)

	def descripcion(self):
		return f"Alquiler de Equipo - {self._nombre} (por día: {formatear_cop(self._base_cost)})"


class Asesoria(Servicio):
	def __init__(self, nombre="Asesoria", disponible=True, base_cost_per_hour=150000.0):
		super().__init__(nombre, disponible, base_cost_per_hour)

	def calcular_costo(self, duration_hours: float, impuesto: float = 0.0, descuento: float = 0.0):
		cost = self._base_cost * max(0.0, duration_hours)
		# ejemplo de regla polimórfica: descuento por horas largas
		if duration_hours >= 4:
			cost *= 0.9  # 10% descuento por sesión larga
		cost = cost * (1 + float(impuesto))
		cost = cost * (1 - float(descuento))
		return round(cost, 2)

	def descripcion(self):
		return f"Asesoría especializada - {self._nombre} (por hora: {formatear_cop(self._base_cost)})"


class Servicios:
	"""Gestor simple que mantiene instancias de servicios por nombre."""

	def __init__(self):
		self._servicios = {
			"Sala": Sala(nombre="Sala", disponible=True, base_cost_per_hour=120000.0),
			"AlquilerEquipo": AlquilerEquipo(nombre="AlquilerEquipo", disponible=True, base_cost_per_day=300000.0),
			"Asesoria": Asesoria(nombre="Asesoria", disponible=True, base_cost_per_hour=150000.0),
		}

	def listar(self):
		return list(self._servicios.keys())

	def esta_disponible(self, servicio_name: str):
		if servicio_name not in self._servicios:
			raise ServicioNoDisponibleError()
		return self._servicios[servicio_name].esta_disponible()

	def set_disponibilidad(self, servicio_name: str, disponible: bool):
		if servicio_name not in self._servicios:
			raise ServicioNoDisponibleError()
		self._servicios[servicio_name].set_disponible(disponible)

	def get_servicio(self, servicio_name: str) -> Servicio:
		if servicio_name not in self._servicios:
			raise ServicioNoDisponibleError()
		return self._servicios[servicio_name]


# Instancia global de uso simple (mantengo la variable `servicios` para compatibilidad)
servicios = Servicios()
