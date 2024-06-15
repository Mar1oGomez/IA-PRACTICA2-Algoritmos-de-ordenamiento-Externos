#Mario Alberto Gomez Temores 21310159   15/06/24
import heapq
import os

def create_initial_runs(input_file, run_size, output_dir):
    """
    Divide el archivo de entrada en varias sub-listas (runs) de tamano run_size, 
    las ordena y las guarda en archivos separados.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    run_index = 0
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), run_size):
            current_run = lines[i:i + run_size]
            current_run.sort()
            run_file = os.path.join(output_dir, f'run_{run_index}.txt')
            with open(run_file, 'w') as run:
                run.writelines(current_run)
            run_index += 1

def merge_files(input_files, output_file):
    """
    Fusiona varios archivos ordenados en uno solo utilizando un heap de minimos.
    """
    min_heap = []
    file_pointers = []
    
    # Abrimos todos los archivos y leemos la primera linea de cada uno
    for i, file in enumerate(input_files):
        f = open(file, 'r')
        file_pointers.append(f)
        line = f.readline()
        if line:
            heapq.heappush(min_heap, (line, i))

    with open(output_file, 'w') as output:
        while min_heap:
            # Extraemos el elemento minimo del heap
            min_line, file_index = heapq.heappop(min_heap)
            output.write(min_line)
            
            # Leemos la siguiente linea del archivo de donde provino el minimo
            next_line = file_pointers[file_index].readline()
            if next_line:
                heapq.heappush(min_heap, (next_line, file_index))
    
    # Cerramos todos los archivos
    for f in file_pointers:
        f.close()

def external_sort(input_file, output_file, run_size, num_ways):
    """
    Implementa el ordenamiento externo usando Balanced Multiway Merging.
    """
    # Crear sub-listas iniciales ordenadas (runs)
    run_dir = 'runs'
    create_initial_runs(input_file, run_size, run_dir)
    
    # Listar todos los archivos de sub-listas (runs)
    run_files = [os.path.join(run_dir, f) for f in os.listdir(run_dir)]
    
    # Fusionar los archivos de sub-listas en el archivo de salida
    merge_files(run_files, output_file)
    
    # Limpiar archivos temporales de sub-listas
    for file in run_files:
        os.remove(file)
    os.rmdir(run_dir)

# Crear un archivo de prueba
with open('data.txt', 'w') as f:
    f.writelines(f"{i}\n" for i in range(1000, 0, -1))

# Ejemplo de uso
input_file = 'data.txt'
output_file = 'sorted_data.txt'
run_size = 100  # Tamano de cada sub-lista
num_ways = 10   # Numero de vias para la fusion (no se usa en esta implementacion basica)

external_sort(input_file, output_file, run_size, num_ways)

