# Laboratorio 2 - Detección y Corrección de Errores

Este repositorio contiene la implementación del **Laboratorio 2**, enfocado en la aplicación de algoritmos de detección y corrección de errores en la transmisión de datos digitales.

---

## 📋 Objetivo

Implementar y probar dos tipos de esquemas de control de errores:

- **Corrección de errores** con el algoritmo **Hamming (7,4)**

Se desarrollaron dos programas para cada esquema: uno que actúa como **emisor** y otro como **receptor**. El emisor se encarga de codificar el mensaje con redundancia, y el receptor verifica o corrige los errores introducidos de forma manual.

---

## 🛠️ Requisitos

### General

- Sistema operativo: Windows, Linux o macOS
- Git (opcional, para clonar el repositorio)

### Para el Emisor (C++)

- Compilador C++ (GCC o compatible)
- Entorno como: `g++`, `Code::Blocks`, `Visual Studio`, `VSCode + MinGW`, entre otros.

### Para el Receptor (Python)

- Python 3.8 o superior
- No requiere librerías externas

---

## 🛠️ Comandos de Ejecución – Corrección de Errores con Hamming (7,4)

### 🖥️ Emisor (C++)

1. Compilar el archivo del emisor:

  - g++ hamming/emisor_hamming.cpp -o hamming_emisor

2. Ejecutar el programa:

  - ./hamming_emisor

📌 El emisor solicitará un mensaje de 4 bits (por ejemplo, 1011) y devolverá la trama de 7 bits con los bits de paridad calculados (por ejemplo, 0111011).

## 🔧 Introducir Error Manual
  Modifica manualmente uno o más bits de la trama para simular errores de transmisión.
  Ejemplo de cambio en la trama: 0111011 → 0110011 (error en el cuarto bit).

### 🖥️ Receptor (Python)

1. Ejecuta el receptor con python:

  - python Correccion/receptor.py

Adicional se tiene un archivo llamado pruebas.py, este es para automatizar las pruebas del receptor, usando tramas correctas generadas con el emisor y versiones con errores (1 o más bits alterados).
### 📝 ¿Qué hace?
  - Usa tramas generadas por el emisor.
  - Simula un error cambiando 1 o 2 bits manualmente.
  - Llama al receptor para verificar si detecta o corrige correctamente el error.
  - Muestra los resultados detallados.
