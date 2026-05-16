# Archivo para gestionar reservas
from datetime import datetime
from cliente import Cliente
from excepciones import *
from logs import configurar_log
from servicios import servicios, Servicio

logger = configurar_log("reservas")


# Clase que representa una reserva hecha por un cliente
class Reserva:

    # Constructor: recibe un objeto Cliente y los datos de la reserva
    def __init__(self, cliente: Cliente, servicio, fecha_inicio, fecha_fin):

        try:
            # -------- VALIDAR CLIENTE --------
            if not isinstance(cliente, Cliente):
                raise ClienteNoValidoError()

            # -------- VALIDAR SERVICIO (acepta nombre o instancia) --------
            servicio_obj = None
            if isinstance(servicio, str):
                if not servicio.strip():
                    raise ServicioVacioError()
                servicio_obj = servicios.get_servicio(servicio)
            elif isinstance(servicio, Servicio):
                servicio_obj = servicio
            else:
                raise ServicioVacioError()

            # Disponibilidad
            if not servicio_obj.esta_disponible():
                raise ServicioNoDisponibleError()

            # -------- VALIDAR FECHAS --------
            if fecha_fin <= fecha_inicio:
                raise FechaInvalidaError()

            # -------- GUARDAR DATOS --------
            self.__cliente = cliente
            self.__servicio = servicio_obj
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
            # calcular duración en horas
            duration_hours = (self.__fecha_fin - self.__fecha_inicio).total_seconds() / 3600.0
            try:
                costo = self.__servicio.calcular_costo(duration_hours, impuesto=0.0, descuento=0.0)
            except Exception:
                costo = None

            return (
                f"--- RESERVA ---\n"
                f"Cliente: {self.__cliente.get_nombre()}\n"
                f"Documento: {self.__cliente.get_ndocumento()}\n"
                f"Correo: {self.__cliente.get_correo()}\n"
                f"Servicio: {self.__servicio.descripcion()}\n"
                f"Fecha inicio: {self.__fecha_inicio}\n"
                f"Fecha fin: {self.__fecha_fin}\n"
                f"Duración (horas): {round(duration_hours, 2)}\n"
                f"Costo estimado: {costo}\n"
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
