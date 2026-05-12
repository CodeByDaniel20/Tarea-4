# Archivo para excepciones personalizadas
# ---------------- EXCEPCIÓN BASE ----------------
class SoftwareTJError(Exception):
    """Excepción base del sistema"""
    def __init__(self, mensaje):
        super().__init__(mensaje)


# ---------------- EXCEPCIONES DE REGISTRO ----------------

class NombreInvalidoError(SoftwareTJError):
    def __init__(self):
        super().__init__("Nombre inválido. Solo se permiten letras.")

class TipoDocumentoInvalidoError(SoftwareTJError):
    def __init__(self):
        super().__init__("Debe seleccionar un tipo de documento válido.")

class NumeroDocumentoInvalidoError(SoftwareTJError):
    def __init__(self):
        super().__init__("Número de documento inválido. Solo números.")

class CorreoInvalidoError(SoftwareTJError):
    def __init__(self):
        super().__init__("Correo inválido. Debe contener @ y .")

class TelefonoInvalidoError(SoftwareTJError):
    def __init__(self):
        super().__init__("Teléfono inválido. Solo números.")

class UsuarioInvalidoError(SoftwareTJError):
    def __init__(self):
        super().__init__("Usuario inválido. Solo letras.")

class ContrasenaInvalidaError(SoftwareTJError):
    def __init__(self):
        super().__init__("Contraseña inválida. Mínimo 4 caracteres.")

class ContrasenaNoCoincideError(SoftwareTJError):
    def __init__(self):
        super().__init__("Las contraseñas no coinciden.")


# ---------------- EXCEPCIONES DE LOGIN ----------------

class UsuarioLoginVacioError(SoftwareTJError):
    def __init__(self):
        super().__init__("El usuario no puede estar vacío.")

class ContrasenaLoginVaciaError(SoftwareTJError):
    def __init__(self):
        super().__init__("La contraseña no puede estar vacía.")

class UsuarioNoEncontradoError(SoftwareTJError):
    def __init__(self):
        super().__init__("Usuario o contraseña incorrectos.")
        
# Reserva
        
# ---------------- EXCEPCIONES DE RESERVA ----------------

class ServicioNoDisponibleError(SoftwareTJError):
    def __init__(self):
        super().__init__("El servicio no está disponible.")
        
class ServicioVacioError(SoftwareTJError):
    def __init__(self):
        super().__init__("El servicio no puede estar vacío.")

class FechaInvalidaError(SoftwareTJError):
    def __init__(self):
        super().__init__("La fecha de inicio no puede ser mayor a la fecha final.")

class ReservaInvalidaError(SoftwareTJError):
    def __init__(self):
        super().__init__("No se puede crear la reserva con los datos ingresados.")

class ClienteNoValidoError(SoftwareTJError):
    def __init__(self):
        super().__init__("Cliente no válido para realizar la reserva.")