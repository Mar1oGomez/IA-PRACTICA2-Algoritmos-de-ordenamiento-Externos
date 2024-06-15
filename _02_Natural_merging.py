#Mario Alberto Gomez Temores 21310159   15/06/24
import os
import random

# Crear un archivo con numeros desordenados
def crear_archivo_desordenado(nombre_archivo, num_elementos, rango):
    with open(nombre_archivo, 'w') as archivo:
        for _ in range(num_elementos):
            archivo.write(f"{random.randint(0, rango)}\n")

# Leer numeros de un archivo
def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        return [int(linea.strip()) for linea in archivo]

# Escribir numeros a un archivo
def escribir_archivo(nombre_archivo, numeros):
    with open(nombre_archivo, 'w') as archivo:
        for numero in numeros:
            archivo.write(f"{numero}\n")

# Divide el archivo en dos sub-archivos basados en secuencias naturales
def dividir_archivo(nombre_archivo, nombre_sub1, nombre_sub2):
    numeros = leer_archivo(nombre_archivo)
    
    sub1 = []
    sub2 = []
    usar_sub1 = True
    
    for i in range(len(numeros)):
        if i == 0 or numeros[i] >= numeros[i-1]:
            if usar_sub1:
                sub1.append(numeros[i])
            else:
                sub2.append(numeros[i])
        else:
            usar_sub1 = not usar_sub1
            if usar_sub1:
                sub1.append(numeros[i])
            else:
                sub2.append(numeros[i])
    
    escribir_archivo(nombre_sub1, sub1)
    escribir_archivo(nombre_sub2, sub2)

# Fusiona dos archivos en uno solo, manteniendo el orden
def fusionar_archivos(nombre_sub1, nombre_sub2, nombre_salida):
    sub1 = leer_archivo(nombre_sub1)
    sub2 = leer_archivo(nombre_sub2)
    
    i, j = 0, 0
    resultado = []
    
    while i < len(sub1) and j < len(sub2):
        if sub1[i] <= sub2[j]:
            resultado.append(sub1[i])
            i += 1
        else:
            resultado.append(sub2[j])
            j += 1
    
    resultado.extend(sub1[i:])
    resultado.extend(sub2[j:])
    
    escribir_archivo(nombre_salida, resultado)

# Realiza el algoritmo de Natural Merging
def natural_merging_sort(nombre_archivo):
    nombre_sub1 = 'sub1.txt'
    nombre_sub2 = 'sub2.txt'
    nombre_salida = 'salida.txt'
    
    while True:
        dividir_archivo(nombre_archivo, nombre_sub1, nombre_sub2)
        fusionar_archivos(nombre_sub1, nombre_sub2, nombre_salida)
        
        # Leer archivos para verificar si estan completamente ordenados
        original = leer_archivo(nombre_archivo)
        salida = leer_archivo(nombre_salida)
        
        if original == salida:
            break
        
        os.replace(nombre_salida, nombre_archivo)

# Parametros para crear el archivo de prueba
nombre_archivo = 'desordenado.txt'
num_elementos = 100
rango = 1000

# Crear archivo desordenado
crear_archivo_desordenado(nombre_archivo, num_elementos, rango)

# Aplicar Natural Merging Sort
natural_merging_sort(nombre_archivo)

# Mostrar archivo ordenado
print(leer_archivo(nombre_archivo))

