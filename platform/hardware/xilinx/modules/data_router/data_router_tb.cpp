#include "data_router.hpp"
#include <iostream>
#include <fstream>
#include <stdint.h>

using namespace std;

int main() {
    ifstream rxDataInFile;
    ifstream rxMetadataInFile;
    ifstream rxDataOutFile;
    ifstream txDataInFile;
    ifstream txDataOutFile;
    ifstream txMetadataOutFile;
    ifstream txLengthOutFile;
    ifstream commandOutFile;
    ifstream portsOutFile;
    ifstream commandReplyInFile;

    //const uint32_t self_addr = 0x01010101;
    //const uint32_t dest_addr = 0x01010102;
    //const uint16_t tm_port   = 5440;
    //const uint16_t self_port = 5441;
    //const uint16_t dest_port = 5442;
    //const ap_uint<32> self_addr = 0x01010101;
    //const ap_uint<16> dest_addr = 0x01010102;
    //const ap_uint<16> tm_port   = 5440;
    //const ap_uint<16> self_port = 5441;
    //const ap_uint<16> dest_port = 5442;

    stream<axiWord>             rxDataIn;
    stream<metadata>            rxMetadataIn;
    stream<axiWord>             rxDataOut;
    stream<axiWord>             txDataIn;
    stream<axiWord>             txDataOut;
    stream<metadata>            txMetadataOut;
    stream<ap_uint<16> >        txLengthOut;
    stream<ap_uint<CMD_WIDTH> > commandOut;
    stream<nwif_ports>          portsOut;
    stream<bool>                commandReplyIn;

    axiWord         rxDataInData;
    metadata        rxMetadataInData;
    axiWord         txDataInData;
    bool            commandReplyInData;

    axiWord                 rxDataOutExpected;
    axiWord                 txDataOutExpected;
    metadata                txMetadataOutExpected;
    ap_uint<16>             txLengthOutExpected;
    ap_uint<CMD_WIDTH>    commandOutExpected;
    nwif_ports              portsOutExpected;

    axiWord                 rxDataOutActual;
    axiWord                 txDataOutActual;
    metadata                txMetadataOutActual;
    ap_uint<16>             txLengthOutActual;
    ap_uint<CMD_WIDTH>    commandOutActual;
    nwif_ports              portsOutActual;

    uint64_t        axiWordData;
    uint16_t        axiWordKeep;
    uint16_t        axiWordLast;
    uint16_t        srcPort;
    uint32_t        srcAddr;
    uint32_t        destAddr;
    uint32_t        command;
    uint16_t        selfPort;
    uint16_t        destPort;
    uint16_t        length;

    rxDataInFile.open("../../../../test_data/rxDataIn.dat");
    if (!rxDataInFile) {
        cout << "Error: could not open rxDataIn file" << endl;
        return -1;
    }
    rxMetadataInFile.open("../../../../test_data/rxMetadataIn.dat");
    if (!rxMetadataInFile) {
        cout << "Error: could not open rxMetadataIn file" << endl;
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
    txMetadataOutFile.open("../../../../test_data/txMetadataOut.dat");
    if (!txMetadataOutFile) {
        cout << "Error: could not open txMetadataOut file" << endl;
        return -1;
    }
    txLengthOutFile.open("../../../../test_data/txLengthOut.dat");
    if (!txLengthOutFile) {
        cout << "Error: could not open txLengthOutFile file" << endl;
        return -1;
    }
    commandOutFile.open("../../../../test_data/commandOut.dat");
    if (!commandOutFile) {
        cout << "Error: could not open commandOut file" << endl;
        return -1;
    }
    portsOutFile.open("../../../../test_data/portsOut.dat");
    if (!portsOutFile) {
        cout << "Error: could not open portsOut file" << endl;
        return -1;
    }
    commandReplyInFile.open("../../../../test_data/commandReplyIn.dat");
    if (!commandReplyInFile) {
        cout << "Error: could not open commandReplyIn file" << endl;
        return -1;
    }

    // Initialize RX input streams
    while (rxDataInFile >> hex >> axiWordData >> axiWordKeep >> axiWordLast) {
        rxDataInData.data = (ap_uint<64>)axiWordData;
        rxDataInData.keep = (ap_uint<8>)axiWordKeep;
        rxDataInData.last = (ap_uint<1>)axiWordLast;
        rxDataIn.write(rxDataInData);
    }
    while (rxMetadataInFile >> hex >> srcPort
                                   >> srcAddr
                                   >> destPort
                                   >> destAddr) {

        rxMetadataInData.sourceSocket.port = srcPort;
        rxMetadataInData.sourceSocket.addr = srcAddr;
        rxMetadataInData.destinationSocket.port = destPort;
        rxMetadataInData.destinationSocket.addr = destAddr;
        rxMetadataIn.write(rxMetadataInData);
    }
    while (commandReplyInFile >> hex >> commandReplyInData) {
        commandReplyIn.write(commandReplyInData);
    }

    // Run RX functionality
    for (int i = 0; i < 20; ++i) {
        data_router(rxDataIn, rxMetadataIn, rxDataOut,
                    txDataIn, txDataOut, txMetadataOut, txLengthOut,
                    commandOut, portsOut, commandReplyIn);
    }

    // Check input streams
    if (!rxDataIn.empty()) {
        cout << "rxDataIn has leftover data" << endl;
        return -1;
    }
    if (!rxMetadataIn.empty()) {
        cout << "rxMetadataIn has leftover data" << endl;
        return -1;
    }
    if (!commandReplyIn.empty()) {
        cout << "commandReplyIn has leftover data" << endl;
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
    while (commandOutFile >> hex >> command) {
        commandOutExpected = (ap_uint<CMD_WIDTH>)command;
        if (commandOut.empty()) {
            cout << "commandOut doesn't have enough data" << endl; 
            return -1;
        }
        commandOut.read(commandOutActual);
        if (!(commandOutExpected == commandOutActual)) {
            cout << "commandOut doesn't match" << endl;
            return -1;
        }
    }
    if (!commandOut.empty()) {
        cout << "commandOut has leftover data" << endl;
        return -1;
    }
    while (portsOutFile >> hex >> selfPort >> destPort) {
        portsOutExpected.selfPort = (ap_uint<16>)selfPort;
        portsOutExpected.destPort = (ap_uint<16>)destPort;
        if (portsOut.empty()) {
            cout << "portsOut doesn't have enough data" << endl;
            return -1;
        }
        portsOut.read(portsOutActual);
        if (!(portsOutExpected.selfPort == portsOutActual.selfPort &&
              portsOutExpected.destPort == portsOutActual.destPort)) {
            cout << "portsOut doesn't match" << endl;
            return -1;
        }
    }
    if (!portsOut.empty()) {
        cout << "portsOut has leftover data" << endl;
        return -1;
    }

    // Initialize TX input streams
    while (txDataInFile >> hex >> axiWordData >> axiWordKeep >> axiWordLast) {
        txDataInData.data = (ap_uint<64>)axiWordData;
        txDataInData.keep = (ap_uint<8>)axiWordKeep;
        txDataInData.last = (ap_uint<1>)axiWordLast;
        txDataIn.write(txDataInData);
    }

    // Run TX functionality
    for (int i = 0; i < 20; ++i) {
        DataRouter(rxDataIn, rxMetadataIn, rxDataOut,
                   txDataIn, txDataOut, txMetadataOut, txLengthOut,
                   commandOut, portsOut, commandReplyIn);
    }

    // Check TX input streams
    if (!txDataIn.empty()) {
        cout << "txDataIn has leftover data" << endl;
        return -1;
    }

    // Check TX output streams
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
        return -1;
    }

    while (txMetadataOutFile >> hex >> srcPort
                                    >> srcAddr
                                    >> destPort
                                    >> destAddr) {
        txMetadataOutExpected.sourceSocket.port = (ap_uint<16>)srcPort;
        txMetadataOutExpected.sourceSocket.addr = (ap_uint<32>)srcAddr;
        txMetadataOutExpected.destinationSocket.port = (ap_uint<16>)destPort;
        txMetadataOutExpected.destinationSocket.addr = (ap_uint<32>)destAddr;
        if (txMetadataOut.empty()) {
            cout << "txMetadataOut doesn't have enough data" << endl; 
            return -1;
        }
        txMetadataOut.read(txMetadataOutActual);
        if (!(txMetadataOutExpected.sourceSocket.port == txMetadataOutActual.sourceSocket.port &&
              txMetadataOutExpected.sourceSocket.addr == txMetadataOutActual.sourceSocket.addr &&
              txMetadataOutExpected.destinationSocket.port == txMetadataOutActual.destinationSocket.port &&
              txMetadataOutExpected.destinationSocket.addr == txMetadataOutActual.destinationSocket.addr)) {
            cout << "txMetadataOut doesn't match" << endl;
            return -1;
        }
    }
    if (!txMetadataOut.empty()) {
        cout << "txMetadataOut has leftover data" << endl;
        return -1;
    }

    while (txLengthOutFile >> hex >> length) {
        txLengthOutExpected = (ap_uint<16>)length;
        if (txLengthOut.empty()) {
            cout << "txLengthOut doesn't have enough data" << endl; 
            return -1;
        }
        txLengthOut.read(txLengthOutActual);
        if (!(txLengthOutExpected == txLengthOutActual)) {
            cout << "txLengthOut doesn't match" << endl;
            return -1;
        }
    }
    if (!txLengthOut.empty()) {
        cout << "txLengthOut has leftover data" << endl;
        return -1;
    }


    return 0;
}
