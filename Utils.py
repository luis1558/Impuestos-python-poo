from Propietario import Propietario
from Vehiculo import Vehiculo
from Impuesto import Impuesto
import psycopg2

class Utils:
    def __init__(self):
        self.propietarios = []
        self.vehiculos = []

        # Configuración de la base de datos
        self.conn = psycopg2.connect(
            host="localhost",
            database="impuesto",
            user="postgres",
            password="Sabbag2022"
        )
        self.cursor = self.conn.cursor()

        # Crear la tabla si no existe
        self.cursor.execute("CREATE TABLE IF NOT EXISTS propietario_vehiculo (id SERIAL PRIMARY KEY, identificacion INT, nombre VARCHAR(255), modelo INT, cilindraje FLOAT, num_llantas INT, placa VARCHAR(255), impuesto_registro FLOAT, impuesto_rodamiento FLOAT)")
        self.conn.commit()

    def __del__(self):
        # Cerrar la conexión cuando se destruye la instancia
        self.conn.close()

    def cargar_datos_desde_bd(self):
        # Consultar registros desde la base de datos y cargar en propietarios y vehiculos
        self.cursor.execute("SELECT * FROM propietario_vehiculo")
        propietarios_registrados = self.cursor.fetchall()

        for item in propietarios_registrados:
            identificacion, nombre = item
            propietario = Propietario(identificacion, nombre)
            self.propietarios.append(propietario)

        self.cursor.execute("SELECT modelo, cilindraje, num_llantas, placa, impuesto_registro, impuesto_rodamiento FROM propietario_vehiculo")
        vehiculos_registrados = self.cursor.fetchall()

        for item in vehiculos_registrados:
            modelo, cilindraje, num_llantas, placa, impuesto_registro, impuesto_rodamiento = item
            vehiculo = Vehiculo(modelo, 0, cilindraje, num_llantas, placa, None)
            self.vehiculos.append(vehiculo)

    def registrar_propietario(self):
        # Solicitar datos del propietario
        identificacion = int(input("Ingrese la identificación del propietario: "))
        nombre = input("Ingrese el nombre del propietario: ")
        propietario = Propietario(identificacion, nombre)

        # Agregar propietario a la lista
        self.propietarios.append(propietario)
        
        print("Registro exitoso del propietario.")

    def registrar_vehiculo(self):
        # Solicitar datos del vehículo
        modelo = int(input("Ingrese el modelo del vehículo: "))
        valor = int(input("Ingrese el valor del vehiculo: "))
        cilindraje = float(input("Ingrese el cilindraje del vehículo: "))
        num_llantas = int(input("Ingrese el número de llantas del vehículo: "))
        placa = input("Ingrese la placa del vehículo: ")

        # Registrar el vehiculo
        vehiculo = Vehiculo(modelo, valor, cilindraje, num_llantas, placa, None)
        self.vehiculos.append(vehiculo)

        print("Registro exitoso del vehículo.")

    def vincular_vehiculo_a_propietario(self):
        # Mostrar propietarios disponibles
        print("Propietarios disponibles:")
        for i, propietario in enumerate(self.propietarios, 1):
            print(f"{i}. {propietario.get_nombre()} (Identificación: {propietario.get_identificacion()})")

        # Solicitar al usuario seleccionar un propietario
        opcion_propietario = int(input("Seleccione el número del propietario: "))
        if 1 <= opcion_propietario <= len(self.propietarios):
            propietario = self.propietarios[opcion_propietario - 1]

            # Mostrar vehículos disponibles
            print("Vehículos disponibles:")
            for i, vehiculo in enumerate(self.vehiculos, 1):
                print(f"{i}. Placa: {vehiculo.get_placa()}, Modelo: {vehiculo.get_modelo()}")

            # Solicitar al usuario seleccionar un vehículo
            opcion_vehiculo = int(input("Seleccione el número del vehículo: "))
            if 1 <= opcion_vehiculo <= len(self.vehiculos):
                vehiculo = self.vehiculos[opcion_vehiculo - 1]
                
                # Vincular el vehículo al propietario
                vehiculo.set_propietario(propietario)
                sql = "INSERT INTO propietario_vehiculo (identificacion, nombre, modelo, cilindraje, num_llantas, placa, impuesto_registro, impuesto_rodamiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                data = (
                    str(vehiculo.get_propietario().get_identificacion()),
                    vehiculo.get_propietario().get_nombre(),
                    str(vehiculo.get_modelo()),
                    str(vehiculo.get_cilindraje()),
                    str(vehiculo.get_num_llantas()),
                    vehiculo.get_placa(),
                    str(Impuesto.calcular_impuesto_registro(vehiculo)),
                    str(Impuesto.calcular_impuesto_rodamiento(vehiculo))
                                                                        )
                self.cursor.execute(sql, data)

                print("Vinculación exitosa.")
            else:
                print("Número de vehículo no válido.")
        else:
            print("Número de propietario no válido.")

    def visualizar_propietarios_vehiculos(self):
        # Cargar datos desde la base de datos antes de mostrar
        self.cargar_datos_desde_bd()

        # Mostrar información de propietarios y vehículos
        for i, propietario in enumerate(self.propietarios, 1):
            print(f"\nPropietario {i}:")
            print(f"Identificación: {propietario.get_identificacion()}, Nombre: {propietario.get_nombre()}")

            # Obtener vehículos desde la base de datos para el propietario actual
            self.cursor.execute("SELECT modelo, cilindraje, num_llantas, placa, impuesto_registro, impuesto_rodamiento FROM propietario_vehiculo WHERE identificacion = %s", (propietario.get_identificacion(),))
            vehiculos_propietario_bd = self.cursor.fetchall()

            if vehiculos_propietario_bd:
                for j, vehiculo_data in enumerate(vehiculos_propietario_bd, 1):
                    modelo, cilindraje, num_llantas, placa, impuesto_registro, impuesto_rodamiento = vehiculo_data
                    vehiculo = Vehiculo(modelo, 0, cilindraje, num_llantas, placa, None)
                    print(f"\tVehículo {j}:")
                    print(f"\tModelo: {vehiculo.get_modelo()}, Placa: {vehiculo.get_placa()}")
                    print(f"\tImpuesto de Registro: ${impuesto_registro:.2f}")
                    print(f"\tImpuesto de Rodamiento: ${impuesto_rodamiento:.2f}")
            else:
                print("\tNo tiene vehículos registrados.")

    def menu_principal(self):
        while True:
            print("\n----- Menu Principal -----")
            print("1. Registrar Propietario")
            print("2. Registrar Vehiculo")
            print("3. Vincular Vehiculo a Propietario")
            print("4. Visualizar Propietarios y Vehiculos")
            print("5. Salir")

            opcion = input("Ingrese el numero de la opcion deseada: ")

            if opcion == "1":
                self.registrar_propietario()
            elif opcion == "2":
                self.registrar_vehiculo()
            elif opcion == "3":
                self.vincular_vehiculo_a_propietario()
            elif opcion == "4":
                self.visualizar_propietarios_vehiculos()
            elif opcion == "5":
                print("Saliendo del programa. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, elija una opción válida.")

if __name__ == "__main__":
    utils = Utils()
    utils.menu_principal()
