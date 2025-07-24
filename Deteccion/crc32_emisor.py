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

# Ejecución de prueba
if __name__ == "__main__":
    mensaje = "11010011101100"
    resultado = crc32_emisor(mensaje)
    print("Trama con CRC:", resultado)
