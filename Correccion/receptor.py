import socket

# ------------------- CONFIG -------------------
SERVER_IP = "127.0.0.1"
SERVER_PORT = 9090

# ------------------- CODIFICADORES -------------------
def codificar_hamming_7_4(bits):
    def hamming_7_4(b):
        d = list(map(int, b))
        p1 = d[0] ^ d[1] ^ d[3]
        p2 = d[0] ^ d[2] ^ d[3]
        p3 = d[1] ^ d[2] ^ d[3]
        return f"{p1}{p2}{d[0]}{p3}{d[1]}{d[2]}{d[3]}"

    if len(bits) % 4 != 0:
        bits += '0' * (4 - len(bits) % 4)

    return ''.join(hamming_7_4(bits[i:i+4]) for i in range(0, len(bits), 4))


def codificar_crc(bits, polinomio='100000111'):
    bits = bits + '0' * (len(polinomio) - 1)
    bits = list(bits)
    polinomio = list(polinomio)

    for i in range(len(bits) - len(polinomio) + 1):
        if bits[i] == '1':
            for j in range(len(polinomio)):
                bits[i + j] = str(int(bits[i + j]) ^ int(polinomio[j]))

    crc = ''.join(bits[-(len(polinomio) - 1):])
    return ''.join(bits[:-(len(polinomio) - 1)] + list(crc))

# ------------------ HAMMING -------------------
def corregir_hamming(bits: str) -> tuple[str, bool, bool]:
    """
    Devuelve (mensaje_bits, error_detectado, corregido)
    - error_detectado: True si se detectó al menos un error
    - corregido: True si los errores detectados fueron corregidos
    """
    corrected = []
    error_detectado = False
    corregido = True  # asumimos corregible hasta encontrar un error múltiple
    i = 0
    while i < len(bits):
        block = bits[i:i+7]
        if len(block) < 7:
            break
        b = [int(x) for x in block]
        p1, p2, d1, p3, d2, d3, d4 = b

        # Calcular síndrome
        c1 = p1 ^ d1 ^ d2 ^ d4
        c2 = p2 ^ d1 ^ d3 ^ d4
        c3 = p3 ^ d2 ^ d3 ^ d4
        syndrome = c1*1 + c2*2 + c3*4

        if syndrome != 0:
            error_detectado = True
            if syndrome <= 7:
                b[syndrome-1] ^= 1  # corregir 1 bit
            else:
                corregido = False  # error múltiple no corregible

        corrected += [b[2], b[4], b[5], b[6]]
        i += 7

    # corregido solo si había error y lo corregimos
    return ("".join(str(x) for x in corrected), error_detectado, corregido)


# ------------------- CRC ----------------------
def corregir_crc(bits: str, polinomio='100000111') -> tuple[str, bool, bool]:
    """
    Devuelve (mensaje_bits, error_detectado, corregido)
    - CRC no corrige, solo detecta
    - corregido=True si no hubo error (mensaje intacto)
    """
    valido = codificar_crc(bits, polinomio)
    if valido:
        return (bits[:-8], False, True)  # sin error → corregido=True
    else:
        return ("", True, False)  # error detectado y no corregido


# ------------- Función universal --------------
def verificar_y_corregir(trama: str, algoritmo: str = 'hamming') -> dict:
    if algoritmo == 'hamming':
        datos, error_detectado, corregido = corregir_hamming(trama)
        return {
            'error_detectado': error_detectado,
            'corregido': corregido,
            'mensaje': datos
        }
    elif algoritmo == 'crc':
        datos, error_detectado, corregido = corregir_crc(trama)
        return {
            'error_detectado': error_detectado,
            'corregido': corregido,
            'mensaje': datos
        }
    else:
        raise ValueError("Algoritmo no soportado")

# --------------- Utilidades -------------------
def decodificar_mensaje(bits: str) -> str:
    mensaje = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        mensaje += chr(int(byte, 2))
    return mensaje

# --------------- Socket RX --------------------
def recibir_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen()
        print(f"Receptor escuchando en {SERVER_IP}:{SERVER_PORT}")
        conn, addr = s.accept()
        with conn:
            data = conn.recv(4096)
            tramaCompleta = data.decode()
            print(f"Trama recibida: {tramaCompleta}")

            if ':' not in tramaCompleta:
                print("Formato incorrecto. No se recibió el algoritmo.")
                return

            algoritmo, trama = tramaCompleta.split(':', 1)
            resultado = verificar_y_corregir(trama, algoritmo=algoritmo)
            if not resultado['error_detectado']:
                mensaje = decodificar_mensaje(resultado['mensaje'])
                print(f"Mensaje recibido sin errores: {mensaje}")
            elif resultado['corregido']:
                mensaje = decodificar_mensaje(resultado['mensaje'])
                print(f"Mensaje corregido exitosamente: {mensaje}")
            else:
                print("Error múltiple detectado o no corregible. Mensaje perdido.")

# --------------- Ejecutar como script ---------
if __name__ == "__main__":
    recibir_socket()
