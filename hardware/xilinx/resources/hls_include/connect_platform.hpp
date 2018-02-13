#ifndef CONNECT_PLATFORM_HPP
#define  CONNECT_PLATFORM_HPP

#include "hls_stream.h"
#include "ap_int.h"

#define CMD_WIDTH   32
#define STATE_WIDTH 32

struct axiWord {
    ap_uint<64> data;
    ap_uint<8>  keep;
    ap_uint<1>  last;
};

struct sockaddr_in {
    ap_uint<16> port;
    ap_uint<32> addr;
};

struct metadata {
    sockaddr_in sourceSocket;
    sockaddr_in destinationSocket;
};

struct nwif_ports {
    ap_uint<16> selfPort;
    ap_uint<16> destPort;
};

const ap_uint<CMD_WIDTH> CMD_SUBMIT     = 0x0;
const ap_uint<CMD_WIDTH> CMD_PREPARE    = 0x1;
const ap_uint<CMD_WIDTH> CMD_RUN        = 0x2;
const ap_uint<CMD_WIDTH> CMD_PAUSE      = 0x3;
const ap_uint<CMD_WIDTH> CMD_CANCEL     = 0x4;

const ap_uint<STATE_WIDTH> S_IDLE       = 0x0;
const ap_uint<STATE_WIDTH> S_ASSIGNED   = 0x1;
const ap_uint<STATE_WIDTH> S_PREPARING  = 0x2;
const ap_uint<STATE_WIDTH> S_READY      = 0x3;
const ap_uint<STATE_WIDTH> S_RUNNING    = 0x4;
const ap_uint<STATE_WIDTH> S_CANCELLING = 0x5;

#endif
