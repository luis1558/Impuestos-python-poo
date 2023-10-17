class Vehiculo:
    def __init__(self, modelo, valor, cilindraje, num_llantas, placa, propietario):
        self.__modelo = modelo
        self.__valor = valor
        self.__cilindraje = cilindraje
        self.__num_llantas = num_llantas
        self.__placa = placa
        self.__propietario = propietario

## getters y setters

    def get_modelo(self):
        return self.__modelo

    def set_modelo(self, modelo):
        self.__modelo = modelo

    def get_valor(self):
        return self.__valor

    def set_valor(self, valor):
        self.__modelo = valor

    def get_cilindraje(self):
        return self.__cilindraje

    def set_cilindraje(self, cilindraje):
        self.__cilindraje = cilindraje

    def get_num_llantas(self):
        return self.__num_llantas

    def set_num_llantas(self, num_llantas):
        self.__num_llantas = num_llantas

    def get_placa(self):
        return self.__placa

    def set_placa(self, placa):
        self.__placa = placa

    def get_propietario(self):
        return self.__propietario

    def set_propietario(self, propietario):
        self.__propietario = propietario