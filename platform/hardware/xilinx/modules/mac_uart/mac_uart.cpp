#include "ap_int.h"
#include <cstring>
#include "hls_stream.h"

#define RX_OFST     0x40600000
#define TX_OFST     0x40600004
#define STAT_OFST   0x40600008
#define CTRL_OFST   0x4060000c

using namespace hls;

void mac_uart(ap_uint<8>            *base,
              stream<ap_uint<48> >  &mac_addr)
{
#pragma HLS INTERFACE axis register both port=mac_addr
#pragma HLS INTERFACE m_axi depth=1 port=base
#pragma HLS INTERFACE ap_ctrl_none port=return

    static enum State {INIT, RECV} state;
    static ap_uint<16> wait_time = 0;
    static ap_uint<8> ctrl = 0x03;
    static ap_uint<8> stat;
    static ap_uint<8> data;
    static ap_uint<8> mac[6];
    static ap_uint<3> mac_count = 0;

    switch (state) {
        case INIT:
            memcpy(base + CTRL_OFST, &ctrl, 1);
            state = RECV;
            break;
        case RECV:
            if (!mac_addr.full()) {
                memcpy(&stat, base + STAT_OFST, 1);
                if (stat.bit(0) == 1) {
                    memcpy(&data, base + RX_OFST, 1);
                    mac[mac_count++] = data;
                    if (mac_count == 6) {
                        mac_addr.write((mac[0], (mac[1], (mac[2], (mac[3], (mac[4], mac[5]))))));
                        mac_count = 0;
                    }
                }
            }
            break;
    }

    return;
}
