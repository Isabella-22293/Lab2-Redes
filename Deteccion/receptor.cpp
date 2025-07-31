#include <iostream>
#include <string>
#include <bitset>
using namespace std;

// ===== Capa Enlace =====
unsigned int crc32_receptor(const string& input) {
    unsigned int poly = 0x04C11DB7;
    unsigned int crc = 0;
    for (char bit : input) {
        crc ^= ((bit - '0') << 31);
        for (int i = 0; i < 8; ++i) {
            if (crc & 0x80000000)
                crc = (crc << 1) ^ poly;
            else
                crc <<= 1;
        }
    }
    return crc;
}

// ===== Capa Presentación =====
string decodificar_ascii_binario(const string& binario) {
    string mensaje;
    for (size_t i = 0; i < binario.size(); i += 8) {
        bitset<8> bits(binario.substr(i, 8));
        mensaje += char(bits.to_ulong());
    }
    return mensaje;
}

// ===== Ejecución Receptor =====
int main() {
    string trama;
    cout << "Ingrese la trama generada: ";
    cin >> trama;

    if (crc32_receptor(trama) == 0) {
        string mensaje_original = decodificar_ascii_binario(trama.substr(0, trama.size() - 32));
        cout << "[RECEPTOR] Trama valida. Mensaje: " << mensaje_original << endl;
    } else {
        cout << "[RECEPTOR] Error detectado: trama invalida." << endl;
    }

    return 0;
}