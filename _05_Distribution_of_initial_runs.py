# Mario Alberto Gomez Temores      21310159      15\06\24

import os
import heapq

def distribution_of_initial_runs(input_file, temp_dir, run_size):
    """
    Distribuye las corridas iniciales en archivos temporales
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"El archivo {input_file} no existe.")

    with open(input_file, 'r') as infile:
        run = []
        run_num = 0
        
        for line in infile:
            run.append(int(line.strip()))  # Leer y agregar cada linea al run actual
            if len(run) == run_size:
                run.sort()  # Ordenar el run actual
                with open(os.path.join(temp_dir, f'run_{run_num}.txt'), 'w') as outfile:
                    for item in run:
                        outfile.write(f'{item}\n')  # Escribir el run ordenado a un archivo temporal
                run = []
                run_num += 1
        
        if run:
            run.sort()  # Ordenar y escribir el ultimo run si no esta vacio
            with open(os.path.join(temp_dir, f'run_{run_num}.txt'), 'w') as outfile:
                for item in run:
                    outfile.write(f'{item}\n')

def merge_runs(temp_dir, output_file, num_runs):
    """
    Mezcla los runs ordenados en el archivo de salida
    """
    run_files = [open(os.path.join(temp_dir, f'run_{i}.txt'), 'r') for i in range(num_runs)]
    output = open(output_file, 'w')
    
    min_heap = []
    
    # Inicializar el heap con el primer elemento de cada run
    for i, f in enumerate(run_files):
        line = f.readline().strip()
        if line:
            heapq.heappush(min_heap, (int(line), i))
    
    while min_heap:
        smallest, run_index = heapq.heappop(min_heap)
        output.write(f'{smallest}\n')
        
        line = run_files[run_index].readline().strip()
        if line:
            heapq.heappush(min_heap, (int(line), run_index))
    
    for f in run_files:
        f.close()
    output.close()

def external_sort(input_file, output_file, temp_dir, run_size):
    """
    Realiza el ordenamiento externo
    """
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    distribution_of_initial_runs(input_file, temp_dir, run_size)
    
    num_runs = len([name for name in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, name))])
    
    merge_runs(temp_dir, output_file, num_runs)

# Parametros del ordenamiento externo
input_file = 'C:/ruta/completa/al/archivo/input.txt'  # Especifica la ruta completa si es necesario
output_file = 'C:/ruta/completa/al/archivo/output.txt'
temp_dir = 'C:/ruta/completa/al/directorio/temp'
run_size = 100  # Tamano del run

try:
    external_sort(input_file, output_file, temp_dir, run_size)
except FileNotFoundError as e:
    print(e)
