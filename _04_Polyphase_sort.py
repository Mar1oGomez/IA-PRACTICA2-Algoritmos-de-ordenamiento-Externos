#Mario Alberto Gomez Temores     21310159     15\06\24
import heapq  # Importamos heapq para manejar una cola de prioridad (min-heap)
import os     # Importamos os para operaciones del sistema de archivos

def polyphase_sort(input_file, output_file, temp_dir, num_files):
    """
    Funcion principal para realizar el ordenamiento Polyphase.
    input_file: archivo de entrada con datos desordenados.
    output_file: archivo de salida para datos ordenados.
    temp_dir: directorio temporal para archivos intermedios.
    num_files: numero de archivos temporales a usar.
    """

    # Funcion para dividir el archivo de entrada en runas (subsecuencias ordenadas)
    def create_initial_runs():
        runs = []  # Lista para almacenar los nombres de los archivos temporales
        with open(input_file, 'r') as f:
            data = f.readlines()
            chunk_size = len(data) // num_files + 1  # Tamano de cada runa
            for i in range(num_files):
                chunk = data[i * chunk_size:(i + 1) * chunk_size]
                chunk.sort()  # Ordenamos cada runa
                temp_filename = os.path.join(temp_dir, f'temp_run_{i}.txt')
                with open(temp_filename, 'w') as temp_file:
                    temp_file.writelines(chunk)
                runs.append(temp_filename)
        return runs

    # Funcion para fusionar las runas en el archivo de salida
    def merge_runs(runs):
        min_heap = []  # Min-heap para fusionar
        file_handlers = [open(run, 'r') for run in runs]  # Abrimos los archivos temporales

        # Inicializamos el heap con el primer elemento de cada runa
        for i, fh in enumerate(file_handlers):
            line = fh.readline().strip()
            if line:
                heapq.heappush(min_heap, (line, i))

        with open(output_file, 'w') as out_file:
            while min_heap:
                smallest, i = heapq.heappop(min_heap)  # Extraemos el elemento mas pequeno
                out_file.write(smallest + '\n')  # Lo escribimos en el archivo de salida
                next_line = file_handlers[i].readline().strip()
                if next_line:
                    heapq.heappush(min_heap, (next_line, i))  # Anadimos el siguiente elemento de la runa

        # Cerramos todos los archivos temporales
        for fh in file_handlers:
            fh.close()

    # Ejecutamos las funciones
    runs = create_initial_runs()  # Creamos las runas iniciales
    merge_runs(runs)  # Fusionamos las runas

    # Eliminamos los archivos temporales
    for run in runs:
        os.remove(run)

# Ejemplo de uso
input_file = 'input.txt'
output_file = 'sorted_output.txt'
temp_dir = 'temp_files'
num_files = 3

# Crear un archivo de entrada de ejemplo si no existe
if not os.path.exists(input_file):
    with open(input_file, 'w') as f:
        f.writelines(f"{i}\n" for i in range(100, 0, -1))  # Escribir numeros del 100 al 1

# Creamos el directorio temporal si no existe
os.makedirs(temp_dir, exist_ok=True)

# Llamamos a la funcion de ordenamiento Polyphase
polyphase_sort(input_file, output_file, temp_dir, num_files)

# Eliminamos el directorio temporal
os.rmdir(temp_dir)
