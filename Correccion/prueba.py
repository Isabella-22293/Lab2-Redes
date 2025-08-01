import random
import matplotlib.pyplot as plt
import numpy as np
from receptor import verificar_y_corregir, codificar_hamming_7_4, codificar_crc
import csv

random.seed(42)
np.random.seed(42)

# --- Parámetros de prueba ---
algoritmos = ['hamming', 'crc']
probabilidades_error = [0.001, 0.005, 0.01, 0.02, 0.05]
tamanos_mensaje = [8, 16, 32, 64, 128]
repeticiones = 10000

# --- Funciones auxiliares ---
def generar_mensaje(tamano):
    return ''.join(random.choice('01') for _ in range(tamano))

def aplicar_ruido(trama, prob):
    return ''.join(bit if random.random() > prob else ('0' if bit == '1' else '1') for bit in trama)

def calcular_tasa_codigo(algoritmo, tam):
    if algoritmo == 'hamming':
        bloques = (tam + 3) // 4  # cada 4 bits se codifican como 7
        total_codificado = bloques * 7
    elif algoritmo == 'crc':
        total_codificado = tam + 8  # 8 bits de CRC
    else:
        raise ValueError("Algoritmo no soportado para tasa de código")
    return tam / total_codificado  # tasa = mensaje útil / total transmitido

# --- Métricas ---
resultados = {
    alg: {
        p: {
            t: {'ok': 0, 'detectados': 0, 'corregidos': 0, 'fallidos': 0}
            for t in tamanos_mensaje
        }
        for p in probabilidades_error
    }
    for alg in algoritmos
}

# --- Ejecución de pruebas ---
for algoritmo in algoritmos:
    print(f"\n🔍 Ejecutando pruebas para algoritmo: {algoritmo.upper()}")
    for prob in probabilidades_error:
        for tam in tamanos_mensaje:
            for _ in range(repeticiones):
                mensaje = generar_mensaje(tam)
                if algoritmo == 'hamming':
                    trama_codificada = codificar_hamming_7_4(mensaje)
                elif algoritmo == 'crc':
                    trama_codificada = codificar_crc(mensaje)

                trama_con_errores = aplicar_ruido(trama_codificada, prob)
                resultado = verificar_y_corregir(trama_con_errores, algoritmo=algoritmo)

                if not resultado['error_detectado']:
                    # Mensaje correcto, sin errores
                    resultados[algoritmo][prob][tam]['ok'] += 1
                else:
                    # Hubo un error detectado
                    resultados[algoritmo][prob][tam]['detectados'] += 1
                    if resultado['corregido']:
                        resultados[algoritmo][prob][tam]['corregidos'] += 1
                    else:
                        resultados[algoritmo][prob][tam]['fallidos'] += 1

print("\n✅ Pruebas completadas. Generando gráficas...")

# --- Gráficas por algoritmo y tamaño de mensaje ---
for algoritmo in algoritmos:
    for tam in tamanos_mensaje:
        tasas_error = []
        tasas_corregidos = []
        tasas_fallidos = []

        for prob in probabilidades_error:
            total = repeticiones
            detectados = resultados[algoritmo][prob][tam]['detectados']
            corregidos = resultados[algoritmo][prob][tam]['corregidos']
            fallidos = resultados[algoritmo][prob][tam]['fallidos']

            tasas_error.append(detectados / total)
            tasas_corregidos.append(corregidos / total)
            tasas_fallidos.append(fallidos / total)

        plt.figure(figsize=(10, 5))
        x = probabilidades_error
        plt.plot(x, tasas_error, label='Errores detectados', marker='o')
        plt.plot(x, tasas_corregidos, label='Errores corregidos', marker='x')
        plt.plot(x, tasas_fallidos, label='Mensajes fallidos', marker='s')
        plt.xlabel("Probabilidad de error")
        plt.ylabel("Tasa")
        plt.title(f"{algoritmo.upper()} - Tamaño mensaje: {tam} bits")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"grafica_{algoritmo}_{tam}bits.png")
        plt.close()

# --- Gráfica: tasa de código vs. tasa de corrección ---
for algoritmo in algoritmos:
    tasas_codigo = []
    tasas_corregidos_prom = []

    for tam in tamanos_mensaje:
        tasa = calcular_tasa_codigo(algoritmo, tam)
        tasas_codigo.append(tasa)

        # Promedio de tasa de corrección para todas las probabilidades
        total_corr = 0
        for prob in probabilidades_error:
            corregidos = resultados[algoritmo][prob][tam]['corregidos']
            total_corr += corregidos / repeticiones
        promedio_corr = total_corr / len(probabilidades_error)
        tasas_corregidos_prom.append(promedio_corr)

    plt.figure(figsize=(8, 5))
    plt.plot(tasas_codigo, tasas_corregidos_prom, marker='o')
    plt.xlabel("Tasa de código (util / total)")
    plt.ylabel("Promedio tasa de corrección")
    plt.title(f"{algoritmo.upper()} - Tasa de código vs Corrección")
    plt.grid(True)
    plt.savefig(f"grafica_tasa_codigo_{algoritmo}.png")
    plt.close()

with open("resultados_pruebas.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Algoritmo", "Probabilidad", "Tamaño", "Correctos", "Detectados", "Corregidos", "Fallidos"])
    for algoritmo in algoritmos:
        for prob in probabilidades_error:
            for tam in tamanos_mensaje:
                met = resultados[algoritmo][prob][tam]
                writer.writerow([algoritmo, prob, tam, met["ok"], met["detectados"], met["corregidos"], met["fallidos"]])

print("\n📊 Todas las gráficas han sido generadas correctamente.")
