import random

# ===== Capa Aplicación =====
def solicitar_mensaje():
    mensaje = input("Ingrese el mensaje a enviar: ")
    return mensaje

# ===== Capa Presentación =====
def codificar_ascii_binario(mensaje):
    return ''.join(format(ord(c), '08b') for c in mensaje)

# ===== Capa Enlace (CRC32) =====
def crc32_emisor(data_binaria):
    polinomio = 0x104C11DB7
    data = data_binaria + '0' * 32
    data = list(map(int, data))

    for i in range(len(data_binaria)):
        if data[i] == 1:
            for j in range(33):
                data[i + j] ^= (polinomio >> (32 - j)) & 1

    crc = ''.join(map(str, data[-32:]))
    return data_binaria + crc

# ===== Capa Ruido =====
def aplicar_ruido(trama, prob_error=0.01):
    trama_lista = list(trama)
    for i in range(len(trama_lista)):
        if random.random() < prob_error:
            trama_lista[i] = '0' if trama_lista[i] == '1' else '1'
    return ''.join(trama_lista)

# ===== Ejecución Emisor =====
if __name__ == "__main__":
    mensaje = solicitar_mensaje()
    binario = codificar_ascii_binario(mensaje)
    trama_crc = crc32_emisor(binario)
    trama_con_ruido = aplicar_ruido(trama_crc, prob_error=0.02)

    print("\n[EMISOR] Trama generada:", trama_crc)
    print("[EMISOR] Trama con ruido:", trama_con_ruido)
