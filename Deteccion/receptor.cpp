#include <iostream>
#include <string>
using namespace std;

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
int main() {
    string trama;
    cout << "Ingrese la trama con CRC: ";
    cin >> trama;   
    if (crc32_receptor(trama) == 0)
        cout << "Trama valida: sin errores." << endl;
    else
        cout << "Error detectado: trama invalida." << endl;
    return 0;
}