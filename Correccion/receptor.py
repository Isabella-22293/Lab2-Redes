import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9090

def corregir_hamming(bits: str) -> tuple[str, bool]:
    corrected = []
    error_detected = False
    i = 0
    while i < len(bits):
        block = bits[i:i+7]
        if len(block) < 7:
            break
        b = [int(x) for x in block]
        p1, p2, d1, p3, d2, d3, d4 = b

        c1 = p1 ^ d1 ^ d2 ^ d4
        c2 = p2 ^ d1 ^ d3 ^ d4
        c3 = p3 ^ d2 ^ d3 ^ d4
        syndrome = c1*1 + c2*2 + c3*4

        if syndrome != 0:
            error_detected = True
            if syndrome <= 7:
                b[syndrome-1] ^= 1
            else:
                return ("", True)

        corrected += [b[2], b[4], b[5], b[6]]
        i += 7

    return ("".join(str(x) for x in corrected), not error_detected)

def decodificar_mensaje(bits: str) -> str:
    return ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))

def recibir_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen()

        print(f"Receptor escuchando en {SERVER_IP}:{SERVER_PORT}")
        conn, addr = s.accept()
        with conn:
            data = conn.recv(4096)
            trama = data.decode()
            print(f"Trama recibida: {trama}")

            datos, ok = corregir_hamming(trama)
            if ok:
                mensaje = decodificar_mensaje(datos)
                print(f"Mensaje recibido (corregido si era necesario): {mensaje}")
            else:
                print("Error múltiple detectado, mensaje perdido.")

if __name__ == "__main__":
    recibir_socket()
