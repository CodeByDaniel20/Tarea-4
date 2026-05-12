# Archivo para gestionar logs
''' Importa el módulo logging de Python, que permite registrar mensajes
 en archivos o en la consola para monitorear el funcionamiento del programa.'''
import logging


'''Define una función llamada configurar_log que recibe como parámetro
# el nombre del logger que se desea crear o configurar.'''
def configurar_log(nombre):

    '''Obtiene un logger usando el nombre proporcionado.
     Si ya existe un logger con ese nombre, lo reutiliza.'''
    logger = logging.getLogger(nombre)
    
    '''Verifica si el logger ya tiene handlers configurados.
    Esto evita agregar múltiples handlers y duplicar mensajes
    si la función se ejecuta varias veces.'''
    if not logger.handlers:

        ''' Crea un FileHandler para guardar los logs en el archivo
         llamado "software_tj.log" usando codificación UTF-8.'''
        handler = logging.FileHandler("software_tj.log", encoding="utf-8")

        ''' Configura el formato de los mensajes del log.
         %(asctime)s  -> Fecha y hora
         %(levelname)s -> Nivel del mensaje (INFO, ERROR, etc.)
         %(name)s -> Nombre del logger
         %(message)s -> Mensaje registrado'''
        handler.setFormatter(logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - [%(name)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))

        ''' Define el nivel mínimo de mensajes que se guardarán.
        INFO significa que se registrarán mensajes INFO,
        WARNING, ERROR y CRITICAL.'''
        logger.setLevel(logging.INFO)

        '''Agrega el handler al logger para que pueda escribir los mensajes en el archivo configurado.'''
        logger.addHandler(handler)
    
    '''Retorna el logger configurado para poder usarlo en otras partes del programa.'''
    
    return logger
