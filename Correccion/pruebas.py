from receptor import verificar_y_corregir

def alterar_bit(trama, posiciones):
    bits = list(trama)
    for pos in posiciones:
        if 0 <= pos < len(bits):
            bits[pos] = '1' if bits[pos] == '0' else '0'
    return ''.join(bits)

mensajes = {
    "1011": "0111011",
    "0001": "1000001",
    "1111": "0001111",
    "0100": "1001100",
    "1100": "0111100",
    "0011": "1000011"
}

print("===== PRUEBAS AUTOMATIZADAS DEL RECEPTOR HAMMING (7,4) =====")

for datos, trama in mensajes.items():
    print(f"\nMensaje original: {datos}")
    print(f"Trama original : {trama}")

    # Prueba sin errores
    print("\n[1] Sin errores:")
    print(verificar_y_corregir(trama))

    # Prueba con 1 error
    print("\n[2] Con 1 error:")
    trama_1_error = alterar_bit(trama, [2])  
    print(f"Trama modificada: {trama_1_error}")
    print(verificar_y_corregir(trama_1_error))

    # Prueba con 2 errores
    print("\n[3] Con 2 errores:")
    trama_2_errores = alterar_bit(trama, [2, 6]) 
    print(f"Trama modificada: {trama_2_errores}")
    print(verificar_y_corregir(trama_2_errores))

