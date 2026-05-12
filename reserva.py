# Archivo para gestionar reservas
from datetime import datetime
from cliente import Cliente
from excepciones import *
from logs import configurar_log

logger = configurar_log("reservas")


# Clase que representa una reserva hecha por un cliente
class Reserva:

    # Constructor: recibe un objeto Cliente y los datos de la reserva
    def __init__(self, cliente: Cliente, servicio, fecha_inicio, fecha_fin):

        try:
            # -------- VALIDAR CLIENTE --------
            if not isinstance(cliente, Cliente):
                raise ClienteNoValidoError()

            # -------- VALIDAR SERVICIO --------
            if not isinstance(servicio, str) or not servicio.strip():
                raise ServicioVacioError()
            
            # -------- VALIDAR FECHAS --------
            if fecha_fin <= fecha_inicio:
                raise FechaInvalidaError()

            # -------- GUARDAR DATOS --------
            self.__cliente = cliente
            self.__servicio = servicio
            self.__fecha_inicio = fecha_inicio
            self.__fecha_fin = fecha_fin
            self.__estado = "Activa"

            self.__fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # -------- ERROR --------
        except Exception as e:

            logger.error(f"Error al crear reserva: {e}")

            # Encadenamiento de excepciones
            raise ReservaInvalidaError() from e

        # -------- ÉXITO --------
        else:
            logger.info("Reserva creada correctamente")

        # -------- SIEMPRE --------
        finally:
            print("Proceso de reserva finalizado")



    # Muestra un resumen de la reserva con los datos del cliente
    def obtener_resumen(self):

        try:
            return (
                f"--- RESERVA ---\n"
                f"Cliente: {self.__cliente._Abstracta__nombres}\n"
                f"Documento: {self.__cliente._Abstracta__ndocumento}\n"
                f"Correo: {self.__cliente._Abstracta__correo}\n"
                f"Servicio: {self.__servicio}\n"
                f"Fecha inicio: {self.__fecha_inicio}\n"
                f"Fecha fin: {self.__fecha_fin}\n"
                f"Estado: {self.__estado}\n"
                f"Creada el: {self.__fecha_creacion}"
            )

        except Exception as e:
            logger.error(f"Error obteniendo resumen: {e}")
            raise



    # Cambia el estado a cancelada
    def cancelar(self):

        try:
            if self.__estado == "Cancelada":
                raise ReservaCanceladaError()

            self.__estado = "Cancelada"

        except Exception as e:
            logger.error(f"Error al cancelar reserva: {e}")
            raise

        else:
            logger.info("Reserva cancelada correctamente")
        

    # Getters para acceder a los datos desde otros archivos
    def get_cliente(self):
        return self.__cliente

    def get_servicio(self):
        return self.__servicio

    def get_estado(self):
        return self.__estado

    def get_fecha_inicio(self):
        return self.__fecha_inicio

    def get_fecha_fin(self):
        return self.__fecha_fin