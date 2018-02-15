#include "connect_platform.hpp"
#include "echo_format.hpp"
#include <iostream>
#include <fstream>
#include <stdint.h>

using namespace std;

int main() {
    ifstream rxDataInFile;
    ifstream rxEventOutFile;
    ifstream txEventInFile;
    ifstream txDataOutFile;

    stream<axiWord> rxDataIn;
    stream<evWord>  rxEventOut;
    stream<evWord>  txEventIn;
    stream<axiWord> txDataOut;

    axiWord rxDataInVar;
    evWord  txEventInVar;

    evWord  rxEventOutExpected;
    axiWord txDataOutExpected;

    evWord  rxEventOutActual;
    axiWord txDataOutActual;

    uint64_t    axiWordData;
    uint16_t    axiWordKeep;
    uint16_t    axiWordLast;
    uint64_t    evWordField0;

    rxDataInFile.open("../../../../test_data/rxDataIn.dat");
    if (!rxDataInFile) {
        cout << "Error: could not open rxDataIn file" << endl;
        return -1;
    }
    rxEventOutFile.open("../../../../test_data/rxEventOut.dat");
    if (!rxEventOutFile) {
        cout << "Error: could not open rxEventOut file" << endl;
        return -1;
    }
    txEventInFile.open("../../../../test_data/txEventIn.dat");
    if (!txEventInFile) {
        cout << "Error: could not open txEventIn file" << endl;
        return -1;
    }
    txDataOutFile.open("../../../../test_data/txDataOut.dat");
    if (!txDataOutFile) {
        cout<< "Error: could not open txDataOut file" << endl;
        return -1;
    }

    // Initialize input streams
    while (rxDataInFile >> hex >> axiWordData >> axiWordKeep >> axiWordLast) {
        rxDataInVar.data = (ap_uint<64>)axiWordData;
        rxDataInVar.keep = (ap_uint<8>)axiWordKeep;
        rxDataInVar.last = (ap_uint<1>)axiWordLast;
        rxDataIn.write(rxDataInVar);
    }
    while (txEventInFile >> hex >> evWordField0) {
        txEventInVar.field0 = (ap_uint<EV_WIDTH>)evWordField0;
        txEventIn.write(txEventInVar);
    }

    // Run module
    for (int i = 0; i < 100; ++i) {
        echo_format(rxDataIn, rxEventOut, txEventIn, txDataOut);
    }

    // Check output streams
    while (txDataOutFile >> hex >> axiWordData
                                >> axiWordKeep
                                >> axiWordLast) {
        txDataOutExpected.data = (ap_uint<64>)axiWordData;
        txDataOutExpected.keep = (ap_uint<8>)axiWordKeep;
        txDataOutExpected.last = (ap_uint<1>)axiWordLast;

        if (txDataOut.empty()) {
            cout << "txDataOut doesn't have enouth data" << endl;
            return -1;
        }
        txDataOut.read(txDataOutActual);
        if (!(txDataOutExpected.data == txDataOutActual.data &&
              txDataOutExpected.keep == txDataOutActual.keep &&
              txDataOutExpected.last == txDataOutActual.last)) {
            cout << "txDataOut doesn't match" << endl;
            return -1;
        }
    }
    if (!txDataOut.empty()) {
        cout << "txDataOut has leftover data" << endl;
        return -1;
    }
    while (rxEventOutFile >> hex >> evWordField0) {
        rxEventOutExpected.field0 = (ap_uint<EV_WIDTH>)evWordField0;
        if (rxEventOut.empty()) {
            cout << "rxEventOut doesn't have enough data" << endl;
            return -1;
        }
        rxEventOut.read(rxEventOutActual);
        if (!(rxEventOutExpected.field0 == rxEventOutActual.field0)) {
            cout << "txEventOut doesn't match" << endl;
            return -1;
        }
    }
    if (!rxEventOut.empty()) {
        cout << "rxEventOut has leftover data" << endl;
        return -1;
    }

    rxDataInFile.close();
    rxEventOutFile.close();
    txEventInFile.close();
    txDataOutFile.close();

    return 0;
}
