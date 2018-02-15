#include "sha256_format.hpp"
#include <iostream>
#include <fstream>
#include <stdint.h>
#include "connect_platform.hpp"
#include "ap_int.h"
#include "hls_stream.h"

using namespace std;
using namespace hls;

int main() {
    stream<axiWord>         rxDataIn;
    stream<ap_uint<1024> >  rxEventOut;
    stream<ap_uint<32> >    txEventIn;
    stream<axiWord>         txDataOut;

    axiWord         rxDataInVar;
    ap_uint<1024>   rxEventOutVar;
    ap_uint<32>     txEventInVar;
    axiWord         txDataOutVar;

    rxDataInVar.data = 0x1011121314151617;
    rxDataInVar.keep = 0xff;
    for (int i = 0; i < 6; ++i) {
        for (int j = 0; j < 16; ++j) {
            rxDataInVar.data += 1;
            if (j == 0xf) {
                rxDataInVar.last = 1;
            } else {
                rxDataInVar.last = 0;
            }
            rxDataIn.write(rxDataInVar);
        }
    }

    txEventInVar = 0x0;
    for (int i = 0; i < 8; ++i) {
        txEventIn.write(txEventInVar++);
    }

    // Run module
    for (int i = 0; i < 100; ++i) {
        sha256_format(rxDataIn, rxEventOut, txEventIn, txDataOut);
    }

    while (!rxEventOut.empty()) {
    	rxEventOutVar = rxEventOut.read();
        cout << hex << rxEventOutVar << endl;
    }

    while (!txDataOut.empty()) {
    	txDataOutVar = txDataOut.read();
        cout << hex << txDataOutVar.data << ' ' << txDataOutVar.keep << ' ' << txDataOutVar.last << ' ' << endl;
    }

    return 0;
}
