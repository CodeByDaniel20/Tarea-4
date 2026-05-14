# Archivo para gestionar servicios

from excepciones import *


class Servicios:
	"""Gestión mínima de servicios: listado y disponibilidad."""

	def __init__(self):
		# Diccionario de ejemplo: nombre -> disponible (bool)
		self._servicios = {
			"Limpieza": True,
			"Mantenimiento": True,
			"Transporte": False,
		}

	def listar(self):
		"""Devuelve la lista de servicios disponibles (nombres)."""
		return list(self._servicios.keys())

	def esta_disponible(self, servicio):
		"""Comprueba si un servicio existe y está disponible.

		Lanza `ServicioNoDisponibleError` si el servicio no existe
		o si está marcado como no disponible.
		"""
		if servicio not in self._servicios:
			raise ServicioNoDisponibleError()

		return self._servicios[servicio]

	def set_disponibilidad(self, servicio, disponible: bool):
		if servicio not in self._servicios:
			raise ServicioNoDisponibleError()
		self._servicios[servicio] = bool(disponible)


# Instancia global de uso simple
servicios = Servicios()
