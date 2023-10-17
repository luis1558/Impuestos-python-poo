class Impuesto:

    def calcular_impuesto_registro(Vehiculo):
        año_actual = 2023
        impuesto_registro = (Vehiculo.get_valor() * (año_actual - Vehiculo.get_modelo())) / 1000
        return round(impuesto_registro, 2)
    
    def calcular_impuesto_rodamiento(vehiculo):
        impuesto_rodamiento = (vehiculo.get_valor() / vehiculo.get_cilindraje()) * 2.5 * vehiculo.get_num_llantas()
        return round(impuesto_rodamiento)