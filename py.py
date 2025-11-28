import pyodbc
import json

with open('Conexion.json') as archivo_config:
    config = json.load(archivo_config)
    
name_server = config["sql_server"]["name_server"]
database = config["sql_server"]["database"]
username = config["sql_server"]["username"]
password = config["sql_server"]["password"]
controlador_odbc = config["sql_server"]["controlador_odbc"]

connection_string = f'DRIVER={controlador_odbc};SERVER={name_server};DATABASE={database};UID={username};PWD={password}'

def mostrar_menu():
    print("\t** GESTOR PRESTAMOS  **") 
    print("\tOpciones:")
    print("\t1. Consultar Prestamos")
    print("\t2. Actualizar Nombre Equipo")
    print("\t3. Salir")


def actualizar_nombre_equipo(conexion):
    try:
        print("\nACTUALIZAR NOMBRE DE EQUIPO\n")
        equipo_id = int(input("Ingrese el ID del Equipo: "))
        nuevo_nombre = input("Ingrese el Nuevo Nombre: ")

        cursor = conexion.cursor()
        SENTENCIA_SQL = """
            UPDATE GENERAL.Equipos
            SET NombreEquipo = ?
            WHERE IDEquipo = ?
        """
        
        cursor.execute(SENTENCIA_SQL, nuevo_nombre, equipo_id)
        conexion.commit()
        print("\nNombre de equipo actualizado correctamente.")
    except Exception as e:
        conexion.rollback()
        print("\nError al actualizar el nombre del equipo:", e)
    finally:
        print("\n\n Proceso Actualizacion Finalizado")

        
def consultar_prestamos(conexion):
    try:
        print("\nCONSULAR PRESTAMOS\n")
        micursor = conexion.cursor()
        
        SENTENCIA_SQL = """
            EXEC Reportes.uspconsultarprestamo
                @IDUsuario = ?
        """
        persona_id = int(input("Ingrese el ID del Usuario: "))
        
        micursor.execute(SENTENCIA_SQL, (persona_id,))
        rows = micursor.fetchall()
        for row in rows:
            print(f"{row.IDUsuario}\t{row.Nombre}\t{row.Apellido}\t{row.IDPrestamo}\t{row.Fecha}\t{row.Equipo}\t{row.Valor}")
        conexion.commit()
    except Exception as e:
        print("\n \t Ocurrió un error al ejecutar el SP en SQL Server: \n\n", e)
    finally:
        print("\n\n Proceso de Consulta Finalizado")
        
# PROGRAMA PRINCIPAL
try:
    conexion = pyodbc.connect(connection_string)
except Exception as e:
    print("\n \t Ocurrió un error al conectar a SQL Server: \n\n", e)
else:
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-3): ")
        
        if opcion == '1':
            consultar_prestamos(conexion)
        elif opcion == '2':
            actualizar_nombre_equipo(conexion)
        elif opcion == '3':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
    conexion.close()
    