#Mario Alberto Gomez Temores 21310159   15/06/24
import os

def create_initial_runs(input_file, run_size, output_prefix):
    """
    Divide el archivo de entrada en multiples archivos de ejecucion ordenados.
    
    :param input_file: Nombre del archivo de entrada.
    :param run_size: Numero de elementos en cada ejecucion.
    :param output_prefix: Prefijo de los archivos de ejecucion de salida.
    """
    try:
        with open(input_file, 'r') as file:
            data = file.readlines()  # Leer todas las lineas del archivo.
    except FileNotFoundError:
        print(f"Error: El archivo {input_file} no existe.")
        return
    except IOError:
        print(f"Error: No se pudo leer el archivo {input_file}.")
        return

    data = [int(line.strip()) for line in data]  # Convertir las lineas en enteros.
    run_count = 0
    for i in range(0, len(data), run_size):
        run = data[i:i + run_size]  # Dividir los datos en bloques.
        run.sort()  # Ordenar cada ejecucion.
        with open(f'{output_prefix}_{run_count}.txt', 'w') as run_file:
            run_file.write('\n'.join(map(str, run)))  # Escribir la ejecucion ordenada.
        run_count += 1  # Incrementar el contador de ejecuciones.

def merge_files(output_file, run_files):
    """
    Fusiona multiples archivos de ejecucion ordenados en un solo archivo de salida ordenado.
    
    :param output_file: Nombre del archivo de salida.
    :param run_files: Lista de nombres de archivos de ejecucion.
    """
    files = []
    try:
        files = [open(run_file, 'r') for run_file in run_files]  # Abrir todos los archivos de ejecucion.
    except IOError as e:
        print(f"Error: No se pudo abrir uno de los archivos de ejecucion: {e}")
        return

    lines = [f.readline().strip() for f in files]  # Leer la primera linea de cada archivo.

    with open(output_file, 'w') as out_file:
        while any(lines):  # Mientras haya lineas no vacias.
            valid_lines = [(int(line), idx) for idx, line in enumerate(lines) if line]  # Filtrar y convertir a enteros.
            if not valid_lines:
                break
            min_value, min_index = min(valid_lines)  # Encontrar el valor minimo y su indice.
            out_file.write(f"{min_value}\n")  # Escribir el valor minimo en el archivo de salida.
            new_line = files[min_index].readline().strip()  # Leer la siguiente linea del archivo correspondiente.
            lines[min_index] = new_line  # Actualizar la lista de lineas.

    for f in files:
        f.close()  # Cerrar todos los archivos.

def external_sort(input_file, output_file, run_size):
    """
    Funcion principal para ordenar externamente un archivo grande.
    
    :param input_file: Nombre del archivo de entrada.
    :param output_file: Nombre del archivo de salida.
    :param run_size: Tamano de cada ejecucion en elementos.
    """
    output_prefix = 'run'
    create_initial_runs(input_file, run_size, output_prefix)  # Crear las ejecuciones iniciales.

    run_files = [f'{output_prefix}_{i}.txt' for i in range(len(os.listdir('.')) - 2)]  # Lista de archivos de ejecucion.

    # Filtrar solo los archivos que comienzan con el prefijo y terminan con '.txt'
    run_files = [f for f in os.listdir('.') if f.startswith(output_prefix) and f.endswith('.txt')]

    # Asegurarse de que hay archivos de ejecucion creados antes de fusionar
    if not run_files:
        print("Error: No se encontraron archivos de ejecucion para fusionar.")
        return

    merge_files(output_file, run_files)  # Fusionar los archivos de ejecucion.

    # Limpiar archivos de ejecucion temporales.
    for run_file in run_files:
        os.remove(run_file)  # Eliminar los archivos temporales.

# Ejemplo de uso
input_file = 'large_file.txt'
output_file = 'sorted_file.txt'
run_size = 100  # Tamano de cada ejecucion

external_sort(input_file, output_file, run_size)  # Llamar a la funcion principal.
