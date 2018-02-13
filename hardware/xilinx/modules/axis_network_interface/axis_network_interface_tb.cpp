#include "polytheos_platform.hpp"
#include "axi_ethernet_mac_lite.hpp"
#include "hls_stream.h"
#include "ap_int.h"
#include "hw_echo.hpp"
#include "axis_network_interface.hpp"

using namespace hls;

int main(void)
{
    stream<axiWord>     tx_data;
    stream<metadata>    tx_meta;
    stream<axiWord>     rx_data;
    stream<metadata>    rx_meta;
    stream<ap_uint<16> > open_port_request;
    stream<ap_uint<1>  > open_port_reply;
    ap_uint<1> port_open;
    ap_uint<2> tx_state;
    ap_uint<2> rx_state;
    ap_uint<8> buf[0x2000];
    ap_uint<8> tx_header[42] = {0x1c, 0xc0, 0x35, 0x00, 0xbe, 0x02, 0x00, 0x00,
                                0x5e, 0x00, 0xfa, 0xce, 0x08, 0x00, 0x45, 0x00,
                                0x00, 0x24, 0x00, 0x00, 0x40, 0x00, 0x40, 0x11,
                                0xb7, 0x63, 0xc0, 0xa8, 0x01, 0x0b, 0xc0, 0xa8,
                                0x01, 0x0a, 0x15, 0x40, 0x15, 0x36, 0x00, 0x10,
                                0x00, 0x00};
    ap_uint<8> rx_header[42] = {0x00, 0x00, 0x5e, 0x00, 0xfa, 0xce, 0x1c, 0xc0,
                                0x35, 0x00, 0xbe, 0x02, 0x08, 0x00, 0x45, 0x00,
                                0x00, 0x24, 0x00, 0x00, 0x40, 0x00, 0x40, 0x11,
                                0xb7, 0x63, 0xc0, 0xa8, 0x01, 0x0a, 0xc0, 0xa8,
                                0x01, 0x0b, 0x15, 0x36, 0x15, 0x40, 0x00, 0x10,
                                0x00, 0x00};

    // test module
    int tx_c = 0;
    int rx_c = 0;
    int err_c = 0;
    for (int i = 0; i < 512; ++i) {
        if (rx_c < 64 && buf[RX_PING_CTRL_OFFSET] == 0) {
            for (int j = 0; j < 42; ++j) {
                buf[RX_PING_DATA_OFFSET + j] = rx_header[j];
            }
            for (int j = 42; j < 50; ++j) {
                buf[RX_PING_DATA_OFFSET + j] = (rx_c * 8 + j - 42) % 256;
            }
            for (int j = 50; j < 54; ++j) {
                buf[RX_PING_DATA_OFFSET + j] = 0;
            }
            buf[RX_PING_CTRL_OFFSET] = 1;
            ++rx_c;
        }
        network_master(buf, tx_data, tx_meta, rx_data, rx_meta, open_port_request, open_port_reply, &port_open, &tx_state, &rx_state);
        hw_echo(tx_data, tx_meta, rx_data, rx_meta, open_port_request, open_port_reply);
        if (buf[TX_PING_CTRL_OFFSET] == 1) {
            ap_uint<8> tx_data_len = buf[TX_PING_LEN_OFFSET] - 2;
            for (int j = 0; j < UDP_PAYLOAD_OFFSET; ++j) {
                if (buf[TX_PING_DATA_OFFSET + j] != tx_header[j]) {
                    ++err_c;
                    break;
                }
            }
            for (int j = UDP_PAYLOAD_OFFSET; j < tx_data_len; ++j) {
                if (buf[TX_PING_DATA_OFFSET + j] != (tx_c * 8 + j - 42) % 256) {
                    ++err_c;
                    break;
                }
            }
            buf[TX_PING_CTRL_OFFSET] = 0;
            ++tx_c;
        }
    }

    if (!tx_data.empty()) {
        ++err_c;
    }
    if (!tx_meta.empty()) {
        ++err_c;
    }
    if (!rx_data.empty()) {
        ++err_c;
    }
    if (!rx_meta.empty()) {
        ++err_c;
    }

    return err_c;
}
