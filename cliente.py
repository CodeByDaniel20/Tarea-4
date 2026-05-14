from abc import ABC, abstractmethod

# Clase base 
class Abstracta(ABC):

    # Constructor que guarda la información del cliente
    def __init__(self, nombres, ndocumento, correo, telefono, usuario, contraseña):
        # Atributos privados
        self.__nombres = nombres
        self.__ndocumento = ndocumento
        self.__correo = correo
        self.__telefono = telefono
        self.__usuario = usuario
        self.__contraseña = contraseña
    
    
# Clase Cliente que hereda de Abstracta
class Cliente(Abstracta):

    # Constructor que envía los datos a la clase padre
    def __init__(self, nombres, ndocumento, correo, telefono, usuario, contraseña):
        super().__init__(nombres, ndocumento, correo, telefono, usuario, contraseña)

    def get_usuario(self):
        return self._Abstracta__usuario

    def get_contraseña(self):
        return self._Abstracta__contraseña

    # Getters adicionales para evitar acceso a atributos privados
    def get_nombre(self):
        return self._Abstracta__nombres

    def get_ndocumento(self):
        return self._Abstracta__ndocumento

    def get_correo(self):
        return self._Abstracta__correo

    def get_telefono(self):
        return self._Abstracta__telefono