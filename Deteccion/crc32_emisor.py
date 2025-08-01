import random
import zlib

# ===== Capa Presentación =====
def codificar_ascii_binario(mensaje):
    return ''.join(format(ord(c), '08b') for c in mensaje)

def decodificar_ascii_binario(binario):
    mensaje = ''
    for i in range(0, len(binario), 8):
        byte = binario[i:i+8]
        mensaje += chr(int(byte, 2))
    return mensaje

# ===== Capa Enlace (CRC32) =====
def calcular_crc32(binario):
    # Convertimos binario a bytes para usar CRC32 de zlib
    data_bytes = int(binario, 2).to_bytes(len(binario) // 8, byteorder='big')
    return format(zlib.crc32(data_bytes) & 0xFFFFFFFF, '032b')

def verificar_crc32(binario, crc_recibido):
    crc_calculado = calcular_crc32(binario)
    return crc_calculado == crc_recibido

# ===== Capa Ruido =====
def aplicar_ruido(trama, prob):
    trama_ruidosa = ''
    for bit in trama:
        if random.random() < prob:
            trama_ruidosa += '1' if bit == '0' else '0'
        else:
            trama_ruidosa += bit
    return trama_ruidosa

# ===== Simulación de envío-recepción =====
def prueba_transmision(mensaje, prob_ruido):
    # Emisor
    binario = codificar_ascii_binario(mensaje)
    crc = calcular_crc32(binario)
    trama = binario + crc

    # Ruido
    trama_con_ruido = aplicar_ruido(trama, prob_ruido)

    # Receptor
    binario_recibido = trama_con_ruido[:-32]
    crc_recibido = trama_con_ruido[-32:]
    valido = verificar_crc32(binario_recibido, crc_recibido)

    return valido, mensaje, decodificar_ascii_binario(binario_recibido)

# ===== Pruebas automáticas =====
if __name__ == "__main__":
    mensajes = ["Hola", "Redes", "CRC32", "Prueba"]
    probabilidades = [0.0, 0.01, 0.05]
    total = 0
    exitos = 0

    for msg in mensajes:
        for p in probabilidades:
            valido, original, recibido = prueba_transmision(msg, p)
            total += 1
            if valido:
                exitos += 1

            print("\n=== Prueba ===")
            print(f"Mensaje original: {original}")
            print(f"Probabilidad ruido: {p}")
            print(f"Resultado: {'OK' if valido else 'ERROR'}")
            print(f"Mensaje recibido: {recibido}")

    print("\n=== Resumen ===")
    print(f"Pruebas exitosas: {exitos}/{total}")
    print(f"Tasa de éxito: {exitos/total*100:.2f}%")
