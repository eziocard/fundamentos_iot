
import serial
import time
import csv
import re
import os

# Configura el puerto serial y la velocidad de baudios
puerto = '/dev/ttyUSB0' # Cambia 'COM3' por el puerto correcto en tu sistema
velocidad = 115200 # Asegúrate de que coincide con la velocidad de tu Arduino

# Archivo CSV donde se guardarán los datos
archivo_csv = 'datos_sensores.csv'

# Abre el puerto serial
try:
    ser = serial.Serial(puerto, velocidad, timeout=1)
    print(f'Conectado a {puerto} a {velocidad} baudios')
except serial.SerialException:
    print(f'No se pudo conectar al puerto {puerto}')
    exit()

# Función para extraer los valores numéricos de las cadenas
def parse_data(data):
    # Definir patrones para extraer la información de las cadenas
    humedad_aire = re.search(r'Humedad del aire: (\d+\.\d+)', data)
    temperatura = re.search(r'Temperatura: (\d+\.\d+)', data)
    humedad_tierra = re.search(r'Humedad de la tierra: (\d+)', data)

    # Si encontramos los datos, los devolvemos en un diccionario
    datos = {}
    if humedad_aire:
        datos['humedad_aire'] = float(humedad_aire.group(1))
    if temperatura:
        datos['temperatura'] = float(temperatura.group(1))
    if humedad_tierra:
        datos['humedad_tierra'] = int(humedad_tierra.group(1))

    return datos

# Función para escribir los datos en el archivo CSV
def guardar_en_csv(datos):
    # Verifica si el archivo ya existe
    archivo_existe = os.path.exists(archivo_csv)

    # Abrir el archivo CSV en modo append para añadir datos sin sobrescribir
    with open(archivo_csv, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['humedad_aire', 'temperatura', 'humedad_tierra'])
        
        # Si el archivo no existe, escribe los encabezados
        if not archivo_existe:
            writer.writeheader()

        # Escribe los datos en una nueva fila
        writer.writerow(datos)
        print(f'Datos guardados en CSV: {datos}')

# Lee datos del serial y los guarda en el archivo CSV
while True:
    try:
        if ser.in_waiting > 0:  # Si hay datos disponibles en el buffer serial
            datos_raw = ser.readline().decode('utf-8').strip()  # Lee una línea y la decodifica

            if datos_raw:
                print(f'Datos recibidos: {datos_raw}')
                
                # Analizar y separar los datos
                parsed_data = parse_data(datos_raw)
                
                if parsed_data:
                    # Guardar los datos en el archivo CSV
                    guardar_en_csv(parsed_data)

        time.sleep(4)  # Pausa corta para evitar sobrecargar el CPU

    except KeyboardInterrupt:
        print('Interrupción manual del programa')
        break
    except Exception as e:
        print(f'Error: {e}')
        break

# Cerrar el puerto serial al finalizar
ser.close()

