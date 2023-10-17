class Propietario:
    def __init__(self, identificacion, nombre):
        self.__identificacion = identificacion
        self.__nombre = nombre

    #metodos Setters y Getters

    def get_identificacion(self):
        return self.__identificacion
    
    def set_identificacion(self, identificacion):
        self.__identificacion=identificacion

    def get_nombre(self):
        return self.__nombre 
    
    def set_nombre(self, nombre):
        self.__nombre=nombre