#include "window_aggregation.hpp"
#include <iostream>
#include <fstream>
#include <stdint.h>

using namespace std;
using namespace hls;

int main()
{
    ifstream eventInFile;
    ifstream resultOutFile;
    ifstream commandInFile;
    ifstream stateOutFile;

    stream<ap_uint<64> >            eventIn;
    stream<ap_uint<64> >            resultOut;
    stream<ap_uint<CMD_WIDTH> >     commandIn;
    stream<ap_uint<STATE_WIDTH> >   stateOut;

    ap_uint<64>         eventInVar;
    ap_uint<CMD_WIDTH>  commandInVar;

    ap_uint<64>             resultOutExpected;
    ap_uint<STATE_WIDTH>    stateOutExpected;

    ap_uint<64>             resultOutActual;
    ap_uint<STATE_WIDTH>    stateOutActual;

    uint64_t    event;
    uint64_t    result;
    uint32_t    command;
    uint32_t    state;

    eventInFile.open("../../../../test_data/eventIn.dat");
    if (!eventInFile) {
        cout << "Error: could not open eventIn file" << endl;
        return -1;
    }
    resultOutFile.open("../../../../test_data/resultOut.dat");
    if (!resultOutFile) {
        cout << "Error: could not open resultOut file" << endl;
        return -1;
    }
    commandInFile.open("../../../../test_data/commandIn.dat");
    if (!commandInFile) {
        cout << "Error: could not open commandIn file" << endl;
        return -1;
    }
    stateOutFile.open("../../../../test_data/stateOut.dat");
    if (!stateOutFile) {
        cout << "Error: could not open stateOutfile" << endl;
        return -1;
    }


    for (int i = 0; i < 17; ++i) {
        eventInFile >> hex >> event;
        eventInVar = (ap_uint<64>)event;
        eventIn.write(eventInVar);
    }
    for (int i = 0 ; i < 8; ++i) {
        commandInFile >> hex >> command;
        commandInVar = (ap_uint<CMD_WIDTH>)command;
        commandIn.write(command);
    }
    for (int i = 0; i < 60; ++i) {
        window_aggregation(eventIn, resultOut, commandIn, stateOut);
    }


    for (int i = 0; i < 13; ++i) {
        eventInFile >> hex >> event;
        eventInVar = (ap_uint<64>)event;
        eventIn.write(eventInVar);
    }
    for (int i = 0 ; i < 2; ++i) {
        commandInFile >> hex >> command;
        commandInVar = (ap_uint<CMD_WIDTH>)command;
        commandIn.write(command);
    }
    for (int i = 0; i < 30; ++i) {
        window_aggregation(eventIn, resultOut, commandIn, stateOut);
    }


    for (int i = 0 ; i < 3; ++i) {
        commandInFile >> hex >> command;
        commandInVar = (ap_uint<CMD_WIDTH>)command;
        commandIn.write(command);
    }
    for (int i = 0; i < 20; ++i) {
        window_aggregation(eventIn, resultOut, commandIn, stateOut);
    }

    // Check if all the input data was used
    if (!eventIn.empty()) {
        cout << "eventIn has leftover data" << endl;
        return -1;
    }
    if (!commandIn.empty()) {
        cout << "commandIn has leftover data" << endl;
        return -1;
    }

    // Check output streams
    while (resultOutFile >> hex >> result) {
        resultOutExpected = (ap_uint<64>)result;
        if (resultOut.empty()) {
            cout << "resultOut doesn't have enough data" << endl;
            return -1;
        }
        resultOutActual = resultOut.read();
        if (!(resultOutExpected == resultOutActual)) {
            cout << "resultOut doesn't match" << endl;
            return -1;
        }
    }
    if (!resultOut.empty()) {
        cout << "resultOut has leftover data" << endl;
        return -1;
    }
    while (stateOutFile >> hex >> state) {
        stateOutExpected = (ap_uint<STATE_WIDTH>)state;
        if (stateOut.empty()) {
            cout << "stateOut doesn't have enough data" << endl;
            return -1;
        }
        stateOutActual = stateOut.read();
        if (!(stateOutExpected == stateOutActual)) {
            cout << "stateOut doesn't match" << endl;
            return -1;
        }

    }
    if (!stateOut.empty()) {
        cout << "stateOut has leftover data" << endl;
        return -1;
    }

    eventInFile.close();
    resultOutFile.close();
    commandInFile.close();
    stateOutFile.close();

    return 0;
}
