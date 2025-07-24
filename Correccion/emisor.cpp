#include <iostream>
#include <vector>
#include <string>

using namespace std;

vector<int> calcularHamming(vector<int> datos) {
    vector<int> hamming(7);
    hamming[2] = datos[0]; // D1
    hamming[4] = datos[1]; // D2
    hamming[5] = datos[2]; // D3
    hamming[6] = datos[3]; // D4

    // Calcular bits de paridad
    hamming[0] = hamming[2] ^ hamming[4] ^ hamming[6]; // P1
    hamming[1] = hamming[2] ^ hamming[5] ^ hamming[6]; // P2
    hamming[3] = hamming[4] ^ hamming[5] ^ hamming[6]; // P3

    return hamming;
}

int main() {
    string entrada;
    cout << "Ingrese 4 bits de datos (ej: 1011): ";
    cin >> entrada;

    if (entrada.length() != 4 || entrada.find_first_not_of("01") != string::npos) {
        cout << "Entrada inválida. Debe ingresar exactamente 4 bits (0 o 1)." << endl;
        return 1;
    }

    vector<int> datos(4);
    for (int i = 0; i < 4; ++i) {
        datos[i] = entrada[i] - '0';
    }

    vector<int> trama = calcularHamming(datos);
    cout << "Trama Hamming (7,4) generada: ";
    for (int bit : trama) {
        cout << bit;
    }
    cout << endl;

    return 0;
}
