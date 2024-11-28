import json
import os
import pymysql
from types import MappingProxyType
from datetime import datetime

datos_entrada = {"usuario": "admin_hospital", "contraseña": "test1234"}
contraseña = "contraseña.json"
with open(contraseña, "w") as file:
    json.dump(datos_entrada, file)

try:
    with open("contraseña.json") as archivo:
        datos = json.load(archivo)
        # Hacer inmutables los datos cargados
        datos = MappingProxyType(datos)
except Exception as e:
    print(f"Error al cargar el archivo de configuración: {e}")

while True:
    try:
        usuario = input("Ingrese el usuario: ")
        contrasena = input("Ingrese la contraseña: ")
        if usuario == datos["usuario"] and contrasena == datos["contraseña"]:
            print("Ingreso exitoso")
            break
        else:
            print("Usuario o Contraseña no válidos")
    except Exception as a:
        print(f"Error: {a}")
        break
Carpeta="Queries"
if not os.path.exists(Carpeta):
    os.mkdir(Carpeta)  
try:
    connection = pymysql.connect(
        host='localhost',
        user='informatica1',
        password='bio123',
        database='mgeneral_hospital'
    )

except pymysql.MySQLError as e:
    print(f"Error al conectar con MySQL: {e}")
    connection = None

if connection:
    try:
        # Tabla de médicos
        medicos = [
            {"nombre": "Ana", "apellido": "González", "especialidad": "Cardiología", "correo": "11@mail"},
            {"nombre": "Luis", "apellido": "Martínez", "especialidad": "Pediatría", "correo": "2@mail"},
            {"nombre": "Elena", "apellido": "Sánchez", "especialidad": "Endocrinología", "correo": "3@mail"}
        ]
        create_medicos_query = """
        CREATE TABLE IF NOT EXISTS medicos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            especialidad VARCHAR(100) NOT NULL,
            correo VARCHAR(150) UNIQUE NOT NULL
        );
        """
        insertar_medicos_query = """
        INSERT INTO medicos (nombre, apellido, especialidad, correo)
        VALUES (%s, %s, %s, %s)
        """
        
        
        with connection.cursor() as cursor:
            cursor.execute(create_medicos_query)
            connection.commit()
            print(f"Tabla 'medicos' creada exitosamente.")

        with connection.cursor() as cursor:
            cursor.executemany(insertar_medicos_query, 
                               [(m['nombre'], m['apellido'], m['especialidad'], m['correo']) for m in medicos])
            connection.commit()
            print(f"{len(medicos)} registros de médicos insertados exitosamente.")

        # Tabla de pacientes
        pacientes = [
            {"nombre": "Maria", "apellido": "Rodriguez", "nacimiento": "1980-03-15", "genero": "F", "direccion": "Dir1"},
            {"nombre": "Juan", "apellido": "Pérez", "nacimiento": "1995-07-22", "genero": "M", "direccion": "Dir2"},
            {"nombre": "Laura", "apellido": "Gómez", "nacimiento": "1972-11-05", "genero": "F", "direccion": "Dir3"}
        ]
        create_pacientes_query = """
        CREATE TABLE IF NOT EXISTS pacientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            nacimiento VARCHAR(20) NOT NULL,
            genero CHAR(1) NOT NULL,
            direccion VARCHAR(200) UNIQUE NOT NULL
        );
        """
        insertar_pacientes_query = """
        INSERT INTO pacientes (nombre, apellido, nacimiento, genero, direccion)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        # Crear la tabla de pacientes
        with connection.cursor() as cursor:
            cursor.execute(create_pacientes_query)
            connection.commit()
            print(f"Tabla 'pacientes' creada exitosamente.")

        # Insertar los datos de pacientes
        with connection.cursor() as cursor:
            cursor.executemany(insertar_pacientes_query, 
                               [(p['nombre'], p['apellido'], p['nacimiento'], p['genero'], p['direccion']) for p in pacientes])
            connection.commit()
            print(f"{len(pacientes)} registros de pacientes insertados exitosamente.")

        # Tabla de historias médicas
        historias_medicas = [
            {"id_paciente": 1, "fecha_visita": "2023-01-10", "diagnostico": "Migraña", "tratamiento": "Acetaminofén", "notas": "Seguimiento"},
            {"id_paciente": 2, "fecha_visita": "2023-02-05", "diagnostico": "Dolor muscular", "tratamiento": "Paracetamol", "notas": "Nota2"},
            {"id_paciente": 3, "fecha_visita": "2023-03-20", "diagnostico": "Cansancio", "tratamiento": "Descanso", "notas": "Nota3"}
        ]
        create_historias_query = """
        CREATE TABLE IF NOT EXISTS historias_medicas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_paciente INT NOT NULL,
            fecha_visita VARCHAR(20) NOT NULL,
            diagnostico VARCHAR(255) NOT NULL,
            tratamiento VARCHAR(255) NOT NULL,
            notas VARCHAR(255) NOT NULL,
            FOREIGN KEY (id_paciente) REFERENCES pacientes(id)
        );
        """
        insertar_historias_query = """
        INSERT INTO historias_medicas (id_paciente, fecha_visita, diagnostico, tratamiento, notas)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        # Crear la tabla de historias médicas
        with connection.cursor() as cursor:
            cursor.execute(create_historias_query)
            connection.commit()
            print(f"Tabla 'historias_medicas' creada exitosamente.")

        # Insertar los datos de historias médicas
        with connection.cursor() as cursor:
            cursor.executemany(insertar_historias_query, 
                               [(h['id_paciente'], h['fecha_visita'], h['diagnostico'], h['tratamiento'], h['notas']) for h in historias_medicas])
            connection.commit()
            print(f"{len(historias_medicas)} registros de historias médicas insertados exitosamente.")

        # Tabla de citas médicas
        citas_medicas = [
            {"id_paciente": 1, "id_medico": 1, "fecha_cita": "2023-04-10", "hora_cita": "10:00 AM", "razon_cita": "Seguimiento cardiológico"},
            {"id_paciente": 2, "id_medico": 3, "fecha_cita": "2023-04-15", "hora_cita": "2:30 PM", "razon_cita": "Examen de tiroides"},
            {"id_paciente": 3, "id_medico": 2, "fecha_cita": "2023-04-18", "hora_cita": "11:15 AM", "razon_cita": "Control pediátrico"}
        ]
        create_citas_query = """
        CREATE TABLE IF NOT EXISTS citas_medicas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_paciente INT NOT NULL,
            id_medico INT NOT NULL,
            fecha_cita VARCHAR(20) NOT NULL,
            hora_cita VARCHAR(20) NOT NULL,
            razon_cita VARCHAR(255) NOT NULL
        );
        """
        insertar_citas_query = """
        INSERT INTO citas_medicas (id_paciente, id_medico, fecha_cita, hora_cita, razon_cita)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        # Crear la tabla de citas médicas
        with connection.cursor() as cursor:
            cursor.execute(create_citas_query)
            connection.commit()
            print(f"Tabla 'citas_medicas' creada exitosamente.")

        # Insertar los datos de citas médicas
        with connection.cursor() as cursor:
            cursor.executemany(insertar_citas_query, 
             [(c['id_paciente'], c['id_medico'], c['fecha_cita'], c['hora_cita'], c['razon_cita']) for c in citas_medicas])
            connection.commit()
            print(f"{len(citas_medicas)} registros de citas médicas insertados exitosamente.")

        while True:
            try:
                print('Bienvenido al sistema')
                menu=input(''' Ingrese la opción que desea:
                        1-Consultar
                        2-Añadir
                        3-Editar
                        4-Eliminar
                        5-Salir
                        ''')
                if menu=='1':
                    def consultar():
                        
                        tablas_validas = ["medicos", "pacientes", "citas_medicas", "historias_medicas"]
                        print(tablas_validas)
                        tabla = input('Ingrese el nombre de la tabla que desea consultar: ').lower()
                        try:
                            id_c = int(input('Ingrese el id que desea consultar: '))
                        except ValueError:
                            print('El id debe ser un número')
                            return

                        if tabla not in tablas_validas:
                            print(f"La tabla '{tabla}' no es válida")
                            return

                        query = f"SELECT * FROM {tabla} WHERE id = %s"
                        with connection.cursor() as cursor:
                            try:
                                cursor.execute(query, (id_c,))
                                resultados = cursor.fetchall()
                                if not resultados:
                                    print('El id no existe en la tabla')

                                # Ahora se reemplaza el bloque con los diccionarios personalizados
                                if tabla == "medicos":
                                    datos_dict = [
                                        {"id": medico[0], "nombre": medico[1], "apellido": medico[2],
                                        "especialidad": medico[3], "correo": medico[4]}
                                        for medico in resultados]

                                elif tabla == "pacientes":
                                    datos_dict = [
                                        {"id": paciente[0], "nombre": paciente[1], "apellido": paciente[2],
                                        "nacimiento": paciente[3], "genero": paciente[4], "direccion": paciente[5]}
                                        for paciente in resultados]

                                elif tabla == "citas_medicas":
                                    datos_dict = [
                                        {"id_cita": cita[0], "id_paciente": cita[1], "id_medico": cita[2],
                                        "fecha_cita": cita[3], "hora_cita": cita[4], "razon_cita": cita[5]}
                                        for cita in resultados]

                                elif tabla == "historias_medicas":
                                    datos_dict = [
                                        {"id_historias": historia[0], "id_paciente": historia[1], "fecha_visita": historia[2],
                                        "diagnostico": historia[3], "tratamiento": historia[4], "notas": historia[5]}
                                        for historia in resultados]

                                else:
                                    print('La tabla no se encuentra')

                                # Imprimir los resultados como JSON
                                print(json.dumps(datos_dict, indent=4))

                                # Guardar en archivo JSON
                                contador = 0
                                archivo_nombre = f'Queries/{tabla}_{contador}.json'
                                # Asegurarse de que el archivo no exista, si ya existe, aumentar el contador
                                while os.path.exists(archivo_nombre):
                                    contador += 1
                                    archivo_nombre = f'Queries/{tabla}_{contador}.json'

                                # Guardar el archivo
                                with open(archivo_nombre, "w", encoding="utf-8") as archivo:
                                    json.dump(datos_dict, archivo, indent=4)
                                print("Información guardada correctamente")
                            except Exception as e:
                                print(f"Error: {e}")

                    consultar()
                elif menu=='2':
                    def añadir():
                        try:
                            tabla2 = input('Ingrese la tabla a la que desea añadir información: ').lower()

                            if tabla2 == 'medicos':
                                nombre = input('Ingrese el nombre del médico que desea añadir: ')
                                apellido = input('Ingrese el apellido del médico que desea añadir: ')
                                especialidad = input('Ingrese la especialidad del médico que desea añadir: ')
                                correo = input('Ingrese el correo del médico que desea añadir: ')
                                query2 = """
                                INSERT INTO medicos (nombre, apellido, especialidad, correo)
                                VALUES (%s, %s, %s, %s)
                                """
                                with connection.cursor() as cursor:
                                    cursor.execute(query2, (nombre, apellido, especialidad, correo))
                                    connection.commit()
                                    print("Datos añadidos exitosamente.")

                            elif tabla2 == 'pacientes':
                                nombre = input('Ingrese el nombre del paciente que desea añadir: ')
                                apellido = input('Ingrese el apellido del paciente que desea añadir: ')
                                nacimiento = input('Ingrese el nacimiento del paciente que desea añadir: ')
                                genero = input('Ingrese el genero del paciente que desea añadir: ')
                                direccion = input('Ingrese la direccion del paciente que desea añadir: ')
                                query2 = """
                                INSERT INTO pacientes (nombre, apellido, nacimiento, genero, direccion)
                                VALUES (%s, %s, %s, %s, %s)
                                """
                                with connection.cursor() as cursor:
                                    cursor.execute(query2, (nombre, apellido, nacimiento, genero, direccion))
                                    connection.commit()
                                print("Datos añadidos exitosamente.")

                            elif tabla2 == 'historias_medicas':
                                try:
                                    id_paciente = int(input('Ingrese el id del paciente: '))
                                    fecha_visita = input('Ingrese la fecha de visita en formato yyyy-mm-dd: ')
                                    diagnostico = input('Ingrese el diagnóstico: ')
                                    tratamiento = input('Ingrese el tratamiento: ')
                                    notas = input('Ingrese las notas: ')

                                    # Ahora insertamos el id_paciente en la tabla
                                    query2 = """
                                    INSERT INTO historias_medicas (id_paciente, fecha_visita, diagnostico, tratamiento, notas)
                                    VALUES (%s, %s, %s, %s, %s)
                                    """
                                    
                                    with connection.cursor() as cursor:
                                        cursor.execute(query2, (id_paciente, fecha_visita, diagnostico, tratamiento, notas))
                                        connection.commit()
                                    print("Datos añadidos exitosamente.")

                                except Exception as e:
                                    print(f"Error al insertar historia médica: {e}")

                            elif tabla2 == 'citas_medicas':
                                id_paciente = int(input('Ingrese el id del paciente: '))
                                id_medico=int(input('Ingrese el id del medico: '))
                                fecha_cita = input('Ingrese la fecha de cita (yyyy-mm-dd): ')
                                hora_cita = input('Ingrese la hora de cita: ')
                                razon_cita = input('Ingrese la razón de la cita: ')
                                query2 = """
                                INSERT INTO citas_medicas (id_paciente, id_medico, fecha_cita, hora_cita, razon_cita)
                                VALUES (%s, %s, %s, %s, %s)
                                """
                                with connection.cursor() as cursor:
                                    cursor.execute(query2, (id_paciente, id_medico, fecha_cita, hora_cita, razon_cita))
                                    connection.commit()
                                print("Datos añadidos exitosamente.")

                        except Exception as e:
                            print(f'Error: {e}')

                    añadir()

                elif menu=='3':
                    def editar():
                        tabla3=input('Ingrese la tabla que desea editar: ').lower()
                        if tabla3=='medicos':
                            id_medico=input('Ingrese el id del médico que desea modificar: ')
                            columna=input('Ingrese la columna que desea editar: ').lower()
                            nuevo_valor = input('Ingrese el nuevo valor: ')
                            sql = f"UPDATE `{tabla3}`  SET `{columna}` = %s WHERE id = %s"
                            valores = (nuevo_valor, id_medico)
                            with connection.cursor() as cursor:
                                cursor.execute(sql, valores)
                                connection.commit()

                        elif tabla3=='pacientes':
                            id_m=input('Ingrese el id del paciente que desea modificar: ')
                            columna=input('Ingrese la columna que desea editar: ').lower()
                            nuevo_valor = input('Ingrese el nuevo valor: ')
                            sql = f"UPDATE `{tabla3}`  SET `{columna}` = %s WHERE id = %s"
                            valores = (nuevo_valor, id_m)
                            with connection.cursor() as cursor:
                                cursor.execute(sql, valores)
                                connection.commit()

                        elif tabla3=='historias_medicas':
                            id_m=input('Ingrese el id de la historia médica que desea modificar: ')
                            columna=input('Ingrese la columna que desea editar: ').lower()
                            nuevo_valor = input('Ingrese el nuevo valor: ')
                            sql = f"UPDATE `{tabla3}`  SET `{columna}` = %s WHERE id = %s"
                            valores = (nuevo_valor, id_m)
                            with connection.cursor() as cursor:
                                cursor.execute(sql, valores)
                                connection.commit()

                        elif tabla3=='citas_medicas':
                            id_m=input('Ingrese el id de la cita médica que desea modificar: ')
                            columna=input('Ingrese la columna que desea editar: ').lower()
                            nuevo_valor = input('Ingrese el nuevo valor: ')
                            sql = f"UPDATE `{tabla3}`  SET `{columna}` = %s WHERE id = %s"
                            valores = (nuevo_valor, id_m)
                            with connection.cursor() as cursor:
                                cursor.execute(sql, valores)
                                connection.commit()

                        print(f"{cursor.rowcount} registro(s) actualizado(s).")
                    editar()
                        
                elif menu=='4':
                    def eliminar():
                        tablas_validas = ["medicos", "pacientes", "citas_medicas", "historias_medicas"]
                        print(tablas_validas)
                        tabla4=input('Ingrese la tabla donde está la info que desea eliminar: ').lower()
                        id_eliminar=input('Ingrese el id que desea eliminar: ')
                        sql= f" DELETE FROM {tabla4} WHERE id= %s"
                        valores_el=(id_eliminar)
                        with connection.cursor() as cursor:
                            cursor.execute(sql, valores_el)
                            connection.commit()
                        print('Dato eliminado correctamente')
                    eliminar()

                elif menu=='5':
                    print('Saliste del sistema')
                    break
            except:
                print('Ingrese una opción válida')
    except Exception as e:
        print(f"Error en la conexión: {e}")
        
    finally:
        connection.close()
        print("Conexión cerrada.")