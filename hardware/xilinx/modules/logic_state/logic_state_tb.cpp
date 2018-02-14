#include "logic_state.hpp"
#include <iostream>
#include <fstream>
#include <stdint.h>

using namespace std;
using namespace hls;

int main() {
    ifstream rxDataInFile;
    ifstream rxDataOutFile;
    ifstream txDataInFile;
    ifstream txDataOutFile;
    ifstream commandInFile;
    ifstream stateOutFile;
    ifstream prepare_start_file;
    ifstream prepare_done_file;

    stream<axiWord>                 rxDataIn;
    stream<axiWord>                 rxDataOut;
    stream<axiWord>                 txDataIn;
    stream<axiWord>                 txDataOut;
    stream<ap_uint<CMD_WIDTH> >     commandIn;
    stream<ap_uint<STATE_WIDTH> >   stateOut;
    stream<ap_uint<1> >             prepare_start;
    stream<ap_uint<1> >             prepare_done;

    axiWord                 rxDataInData;
    axiWord                 txDataInData;
    ap_uint<CMD_WIDTH>      commandInData;
    ap_uint<1>              prepare_done_data;

    axiWord                 rxDataOutExpected;
    axiWord                 txDataOutExpected;
    ap_uint<STATE_WIDTH>    stateOutExpected;
    ap_uint<1>              prepare_start_expected;

    axiWord                 rxDataOutActual;
    axiWord                 txDataOutActual;
    ap_uint<STATE_WIDTH>    stateOutActual;
    ap_uint<1>              prepare_start_actual;

    uint64_t    axiWordData;
    uint16_t    axiWordKeep;
    uint16_t    axiWordLast;
    uint32_t    command;
    uint32_t    state;
    uint16_t    done;
    uint16_t    start;

    rxDataInFile.open("../../../../test_data/rxDataIn.dat");
    if (!rxDataInFile) {
        cout << "Error: could not open rxDataIn file" << endl;
        return -1;
    }
    rxDataOutFile.open("../../../../test_data/rxDataOut.dat");
    if (!rxDataOutFile) {
        cout << "Error: could not open rxDataOut file" << endl;
        return -1;
    }
    txDataInFile.open("../../../../test_data/txDataIn.dat");
    if (!txDataInFile) {
        cout << "Error: could not open txDataIn file" << endl;
        return -1;
    }
    txDataOutFile.open("../../../../test_data/txDataOut.dat");
    if (!txDataOutFile) {
        cout << "Error: could not open txDataOut file" << endl;
        return -1;
    }
    commandInFile.open("../../../../test_data/commandIn.dat");
    if (!commandInFile) {
        cout << "Error: could not open commandIn file" << endl;
        return -1;
    }
    stateOutFile.open("../../../../test_data/stateOut.dat");
    if (!stateOutFile) {
        cout << "Error: could not open stateOUt file" << endl;
        return -1;
    }
    prepare_start_file.open("../../../../test_data/prepare_start.dat");
    if (!prepare_start_file) {
        cout << "Error: could not open prepare_start file" << endl;
        return -1;
    }
    prepare_done_file.open("../../../../test_data/prepare_done.dat");
    if (!prepare_done_file) {
        cout << "Error: could not open prepare_done file" << endl;
        return -1;
    }

    // Initialize RX input streams
    while (rxDataInFile >> hex >> axiWordData >> axiWordKeep >> axiWordLast) {
        rxDataInData.data = (ap_uint<64>)axiWordData;
        rxDataInData.keep = (ap_uint<8>)axiWordKeep;
        rxDataInData.last = (ap_uint<1>)axiWordLast;
        rxDataIn.write(rxDataInData);
    }
    while (txDataInFile >> hex >> axiWordData >> axiWordKeep >> axiWordLast) {
        txDataInData.data = (ap_uint<64>)axiWordData;
        txDataInData.keep = (ap_uint<8>)axiWordKeep;
        txDataInData.last = (ap_uint<1>)axiWordLast;
        txDataIn.write(txDataInData);
    }
    while (commandInFile >> hex >> command) {
        commandIn.write((ap_uint<32>)command);
    }
    while (prepare_done_file >> hex >> done) {
        prepare_done.write((ap_uint<1>)done);
    }

    // Run RX functionality
    for (int i = 0; i < 30; ++i) {
        logic_state(rxDataIn, rxDataOut, txDataIn, txDataOut,
                    commandIn, stateOut, prepare_start, prepare_done);
    }

    // Check input streams
    if (!rxDataIn.empty()) {
        cout << "rxDataIn has leftover data" << endl;
        return -1;
    }
    if (!txDataIn.empty()) {
        cout << "txDataIn has leftover data" << endl;
        return -1;
    }
    if (!commandIn.empty()) {
        cout << "commandIn has leftover data" << endl;
        return -1;
    }
    if (!prepare_done.empty()) {
        cout << "prepare_done has leftover data" << endl;
        return -1;
    }

    // Check RX output streams
    while (rxDataOutFile >> hex >> axiWordData
                                >> axiWordKeep
                                >> axiWordLast) {
        rxDataOutExpected.data = (ap_uint<64>)axiWordData;
        rxDataOutExpected.keep = (ap_uint<8>)axiWordKeep;
        rxDataOutExpected.last = (ap_uint<1>)axiWordLast;

        if (rxDataOut.empty()) {
            cout << "rxDataOut doesn't have enough data" << endl; 
            return -1;
        }
        rxDataOut.read(rxDataOutActual);
        if (!(rxDataOutExpected.data == rxDataOutActual.data &&
              rxDataOutExpected.keep == rxDataOutActual.keep &&
              rxDataOutExpected.last == rxDataOutActual.last)) {
            cout << "rxDataOut doesn't match" << endl;
            return -1;
        }
    }
    if (!rxDataOut.empty()) {
        cout << "rxDataOut has leftover data" << endl;
        rxDataOut.read(rxDataOutActual);
        return -1;
    }
    while (txDataOutFile >> hex >> axiWordData
                                >> axiWordKeep
                                >> axiWordLast) {
        txDataOutExpected.data = (ap_uint<64>)axiWordData;
        txDataOutExpected.keep = (ap_uint<8>)axiWordKeep;
        txDataOutExpected.last = (ap_uint<1>)axiWordLast;

        if (txDataOut.empty()) {
            cout << "txDataOut doesn't have enough data" << endl; 
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
        txDataOut.read(txDataOutActual);
        return -1;
    }

    while (stateOutFile >> hex >> state) {
        stateOutExpected = (ap_uint<32>)state;
        if (stateOut.empty()) {
            cout << "stateOut doesn't have enough data" << endl;
            return -1;
        }
        stateOut.read(stateOutActual);
        if (stateOutExpected != stateOutActual) {
            cout << "stateOut doesn't match" << endl;
            return -1;
        }
    }
    if (!stateOut.empty()) {
        cout << "stateOut has leftover data" << endl;
        return -1;
    }

    while (prepare_start_file >> hex >> start) {
        prepare_start_expected = (ap_uint<1>)start;
        if (prepare_start.empty()) {
            cout << "prepare_start doesn't have enough data" << endl;
            return -1;
        }
        prepare_start.read(prepare_start_actual);
        if (prepare_start_expected != prepare_start_actual) {
            cout << "prepare_start doesn't match" << endl;
            return -1;
        }
    }
    if (!prepare_start.empty()) {
        cout << "prepare_start has leftover data" << endl;
        return -1;
    }

    return 0;
}
