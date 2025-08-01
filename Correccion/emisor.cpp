#include <iostream>
#include <bitset>
#include <vector>
#include <string>
#include <random>
#include <ctime>
#include <cstring>    // memset
#include <unistd.h>   // close()
#include <arpa/inet.h>
#include <sys/socket.h>

using namespace std;

#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 9090
#define PROB_ERROR 0.005  

// ==================== PRESENTACION ====================
string codificarMensaje(const string& mensaje) {
    string binario = "";
    for (char c : mensaje) {
        binario += bitset<8>(c).to_string();
    }
    return binario;
}

// ==================== ENLACE: Hamming (7,4) ====================
vector<int> stringToBits(const string& s) {
    vector<int> bits;
    for (char c : s) bits.push_back(c - '0');
    return bits;
}

string bitsToString(const vector<int>& bits) {
    string s = "";
    for (int b : bits) s += (b ? '1' : '0');
    return s;
}

vector<int> aplicarHamming(const string& bits) {
    vector<int> in = stringToBits(bits);
    vector<int> out;
    for (size_t i = 0; i < in.size(); i += 4) {
        int d1 = in[i];
        int d2 = (i+1<in.size()) ? in[i+1] : 0;
        int d3 = (i+2<in.size()) ? in[i+2] : 0;
        int d4 = (i+3<in.size()) ? in[i+3] : 0;

        int p1 = (d1 ^ d2 ^ d4);
        int p2 = (d1 ^ d3 ^ d4);
        int p3 = (d2 ^ d3 ^ d4);

        out.push_back(p1);
        out.push_back(p2);
        out.push_back(d1);
        out.push_back(p3);
        out.push_back(d2);
        out.push_back(d3);
        out.push_back(d4);
    }
    return out;
}

// ==================== ENLACE: CRC (8 bits, polinomio 100000111) ====================
string aplicarCRC(const string& bits) {
    string mensajeExtendido = bits + string(8, '0');
    size_t len = mensajeExtendido.size();
    unsigned int polinomio = 0x107; 

    unsigned long long datos = 0;
    for (size_t i = 0; i < len; i++) {
        datos <<= 1;
        if (mensajeExtendido[i] == '1') datos |= 1;
    }

    size_t mensajeLen = bits.size();
    size_t totalLen = mensajeLen + 8;

    for (size_t i = 0; i < mensajeLen; i++) {
        if ((datos >> (totalLen - 1 - i)) & 1) {
            datos ^= (unsigned long long)polinomio << (mensajeLen - 1 - i);
        }
    }

    // Extraer CRC (últimos 8 bits)
    unsigned int crc = datos & 0xFF;

    // Construir resultado: bits originales + crc en binario 8 bits
    string crcStr = "";
    for (int i = 7; i >= 0; i--) {
        crcStr += ((crc >> i) & 1) ? '1' : '0';
    }
    return bits + crcStr;
}

// ==================== RUIDO ====================
string aplicarRuido(const string& bits) {
    string corrupto = bits;
    static default_random_engine gen(time(0));
    uniform_real_distribution<double> dist(0.0, 1.0);

    for (size_t i = 0; i < corrupto.size(); i++) {
        if (dist(gen) < PROB_ERROR) {
            corrupto[i] = (corrupto[i] == '0') ? '1' : '0';
        }
    }
    return corrupto;
}

// ==================== TRANSMISION (Linux) ====================
void enviarSocket(const string& trama) {
    int sockfd;
    struct sockaddr_in serverAddr;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("Error al crear socket");
        return;
    }

    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(SERVER_PORT);
    inet_pton(AF_INET, SERVER_IP, &serverAddr.sin_addr);

    if (connect(sockfd, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
        perror("Error al conectar con el servidor");
        close(sockfd);
        return;
    }

    send(sockfd, trama.c_str(), trama.size(), 0);
    close(sockfd);
}

// ==================== MAIN ====================
int main() {
    cout << "Ingrese mensaje a enviar: ";
    string mensaje;
    getline(cin, mensaje);

    string algoritmo;
    cout << "Seleccione algoritmo para comprobación de integridad (hamming/crc): ";
    getline(cin, algoritmo);
    if (algoritmo != "hamming" && algoritmo != "crc") {
        cout << "Algoritmo no soportado. Usando hamming por defecto.\n";
        algoritmo = "hamming";
    }

    string bits = codificarMensaje(mensaje);
    string trama;
    if (algoritmo == "hamming") {
        vector<int> hammingBits = aplicarHamming(bits);
        trama = bitsToString(hammingBits);
    } else if (algoritmo == "crc") {
        trama = aplicarCRC(bits);
    }

    cout << "Trama sin ruido: " << trama << "\n";
    string tramaRuidosa = aplicarRuido(trama);
    cout << "Trama con ruido:  " << tramaRuidosa << "\n";
    string tramaCompleta = algoritmo + ":" + tramaRuidosa;
    
    enviarSocket(tramaCompleta);
    cout << "Mensaje enviado con " << algoritmo << " y posible ruido.\n";

    return 0;
}
