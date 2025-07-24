def verificar_y_corregir(trama):
    bits = [int(b) for b in trama]
    if len(bits) != 7:
        return "Trama inválida. Debe tener 7 bits."

    # Calcular los bits de paridad
    p1 = bits[0] ^ bits[2] ^ bits[4] ^ bits[6]
    p2 = bits[1] ^ bits[2] ^ bits[5] ^ bits[6]
    p3 = bits[3] ^ bits[4] ^ bits[5] ^ bits[6]

    error_pos = p1 * 1 + p2 * 2 + p3 * 4

    if error_pos == 0:
        data = [bits[2], bits[4], bits[5], bits[6]]
        return f"No se detectaron errores. Datos: {''.join(map(str, data))}"
    elif 1 <= error_pos <= 7:
        bits[error_pos - 1] ^= 1  # Corregir bit
        corrected = ''.join(map(str, bits))
        data = [bits[2], bits[4], bits[5], bits[6]]
        return (f"Se detectó y corrigió un error en la posición {error_pos}.\n"
                f"Trama corregida: {corrected}\n"
                f"Datos extraídos: {''.join(map(str, data))}")
    else:
        return "Error: posición de bit no válida."


if __name__ == "__main__":
    trama = input("Ingrese la trama Hamming (7 bits): ")
    print(verificar_y_corregir(trama))
