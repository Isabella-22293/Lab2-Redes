#include <iostream>
#include <bitset>
#include <vector>
#include <random>
#include <ctime>
#include <iomanip>  // para setw

using namespace std;

// ========== CAPA PRESENTACIÓN ==========
string codificarMensaje(const string& mensaje) {
    string binario = "";
    for (char c : mensaje) {
        binario += bitset<8>(c).to_string();  // Convertir cada char a 8 bits ASCII
    }
    return binario;
}

// ========== CAPA ENLACE ==========
string calcularIntegridadHamming(const string& binario) {
    string resultado = "";
    for (size_t i = 0; i < binario.length(); i += 4) {
        string bloque = binario.substr(i, 4);
        while (bloque.length() < 4) bloque += "0";  // Padding si el bloque < 4 bits

        int d1 = bloque[0] - '0';
        int d2 = bloque[1] - '0';
        int d3 = bloque[2] - '0';
        int d4 = bloque[3] - '0';

        int p1 = d1 ^ d2 ^ d4;
        int p2 = d1 ^ d3 ^ d4;
        int p3 = d2 ^ d3 ^ d4;

        // Orden: P1 P2 D1 P3 D2 D3 D4
        resultado += to_string(p1) + to_string(p2) + to_string(d1) +
                     to_string(p3) + to_string(d2) + to_string(d3) + to_string(d4);
    }
    return resultado;
}

// ========== CAPA RUIDO ==========
string aplicarRuido(const string& trama, double probabilidad_error) {
    string resultado = trama;
    default_random_engine rng(time(0));
    uniform_real_distribution<double> dist(0.0, 1.0);

    for (char& bit : resultado) {
        if (dist(rng) < probabilidad_error) {
            bit = (bit == '0') ? '1' : '0';  // Voltear bit
        }
    }
    return resultado;
}

// ========== CAPA APLICACIÓN ==========
void emisor() {
    string mensaje;
    cout << "\n========================= EMISOR =========================\n";
    cout << "[APLICACIÓN] Ingrese el mensaje a enviar: ";
    getline(cin, mensaje);

    cout << "\n----------------------------------------------------------\n";
    string binario = codificarMensaje(mensaje);
    cout << "[PRESENTACIÓN] Binario codificado (ASCII):\n    "
         << binario << endl;

    cout << "\n----------------------------------------------------------\n";
    string trama_hamming = calcularIntegridadHamming(binario);
    cout << "[ENLACE] Trama codificada con Hamming (7,4):\n    "
         << trama_hamming << endl;

    cout << "\n----------------------------------------------------------\n";
    double prob;
    cout << "[RUIDO] Ingrese probabilidad de error (ej. 0.01 = 1%): ";
    cin >> prob;

    string trama_ruido = aplicarRuido(trama_hamming, prob);
    cout << "\n[RUIDO] Trama con posible error aplicado:\n    "
         << trama_ruido << endl;

    cout << "==========================================================\n";
}

int main() {
    emisor();
    return 0;
}
