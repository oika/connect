#include "axi_ethernet_mac_lite.hpp"
#include "connect_platform.hpp"
#include "hls_stream.h"
#include "ap_int.h"
#include <cstring>

using namespace hls;

ap_uint<16> calc_chksum (ap_uint<8>     ver_ihl,
                         ap_uint<8>     type,
                         ap_uint<16>    len,
                         ap_uint<16>    id,
                         ap_uint<16>    fragment,
                         ap_uint<8>     ttl,
                         ap_uint<8>     protocol,
                         ap_uint<32>    src_addr,
                         ap_uint<32>    dst_addr)
{
    ap_uint<20> big_ver_ihl_type    = (ap_uint<20>)(ver_ihl, type);
    ap_uint<20> big_type            = (ap_uint<20>)len;
    ap_uint<20> big_id              = (ap_uint<20>)id;
    ap_uint<20> big_fragment        = (ap_uint<20>)fragment;
    ap_uint<20> big_ttl_protocol    = (ap_uint<20>)(ttl, protocol);
    ap_uint<20> big_src_addr0       = (ap_uint<20>)src_addr.range(31, 16);
    ap_uint<20> big_src_addr1       = (ap_uint<20>)src_addr.range(15, 0);
    ap_uint<20> big_dst_addr0       = (ap_uint<20>)dst_addr.range(31, 16);
    ap_uint<20> big_dst_addr1       = (ap_uint<20>)dst_addr.range(15, 0);

    ap_uint<20> sum = big_ver_ihl_type + big_type
                                       + big_id
                                       + big_fragment
                                       + big_ttl_protocol
                                       + big_src_addr0
                                       + big_src_addr1
                                       + big_dst_addr0
                                       + big_dst_addr1;

    sum = (ap_uint<20>)sum.range(19, 16) + (ap_uint<20>)sum.range(15, 0);

    return ~sum.range(15, 0);
}

void axis_network_interface(ap_uint<8>              *base,
                            stream<axiWord>         &tx_data,
                            stream<metadata>        &tx_meta,
                            stream<ap_uint<16> >    &tx_length,
                            stream<axiWord>         &rx_data,
                            stream<metadata>        &rx_meta,
                            stream<ap_uint<16> >    &port_open_request,
                            stream<ap_uint<1> >     &port_open_reply,
                            stream<ap_uint<1> >     &cycle_cnt_intr)
{
#pragma HLS INTERFACE axis register both port=cycle_cnt_intr
#pragma HLS INTERFACE axis register both port=port_open_reply
#pragma HLS INTERFACE axis register both port=port_open_request
#pragma HLS DATA_PACK variable=rx_meta
#pragma HLS DATA_PACK variable=tx_meta
#pragma HLS INTERFACE axis register both port=rx_meta
#pragma HLS INTERFACE axis register both port=rx_data
#pragma HLS INTERFACE axis register both port=tx_meta
#pragma HLS INTERFACE axis register both port=tx_data
#pragma HLS INTERFACE axis register both port=tx_length
#pragma HLS INTERFACE m_axi depth=1 port=base
#pragma HLS INTERFACE ap_ctrl_none port=return

    static ap_uint<1> init = 0;
    static enum TxState {TX_INIT = 0, WAIT_MAC, TX_FIRST, TX_REST, TX_WRITE} txState;
    static enum RxState {RX_READ = 0, RX_FIRST, RX_REST} rxState;

    // variables for tx
    static ap_uint<8>  tx_ping_buf[0x800];
    static ap_uint<16> tx_data_offset   = UDP_PAYLOAD_OFFSET;
    //static ap_uint<48> tx_eth_dst_addr  = 0xb827eb429b19; //raspi
    static ap_uint<48> tx_eth_dst_addr  = 0x1cc03500be02;
    //static ap_uint<48> tx_eth_dst_addr  = 0x1cc03500b81b;
    static ap_uint<48> tx_eth_src_addr  = 0x01005e00face;
    static ap_uint<16> tx_eth_type      = 0x0800;
    static ap_uint<8>  tx_ip_ver_ihl    = 0x45;
    static ap_uint<8>  tx_ip_type       = 0x0;
    static ap_uint<16> tx_ip_len;
    static ap_uint<16> tx_ip_id         = 0x0;
    static ap_uint<16> tx_ip_fragment   = 0x4000;
    static ap_uint<8>  tx_ip_ttl        = 0x40;
    static ap_uint<8>  tx_ip_protocol   = 0x11;
    static ap_uint<16> tx_ip_checksum;
    static ap_uint<32> tx_ip_src_addr;
    static ap_uint<32> tx_ip_dst_addr;
    static ap_uint<16> tx_udp_src_port;
    static ap_uint<16> tx_udp_dst_port;
    static ap_uint<16> tx_udp_len;
    static ap_uint<16> tx_udp_checksum  = 0x0;
    static ap_uint<64> tx_udp_payload;
    static ap_uint<6>  intr_cnt         = 0;
    static ap_uint<16>  wait_count = 0;

    // variables for rx
    static ap_uint<8>  rx_ping_buf[0x800];
    static ap_uint<16> rx_payload_offset    = UDP_PAYLOAD_OFFSET;
    static ap_uint<16> rx_payload_len;
    static ap_uint<16> open_port[8]        = {};
    static ap_uint<4>  n_open_ports         = 0;
    static ap_uint<32> rx_ping_ctrl;

    /* Count interrupt */

    if (!cycle_cnt_intr.empty()) {
        cycle_cnt_intr.read();
        ++intr_cnt;
    }

    /* Port open */

    if (!port_open_request.empty() && !port_open_reply.full()) {
        if (n_open_ports.bit(3)) {
            port_open_request.read();
            port_open_reply.write(0);
        } else {
            ap_uint<16> new_port = port_open_request.read();
            open_port[n_open_ports++] = new_port;
            port_open_reply.write(1);
        }
    }

    /* TX */
    switch (txState) {
        case TX_INIT: {
            for (int i = 0; i < 6; ++i) {
            #pragma HLS PIPELINE
                tx_ping_buf[ETH_DST_ADDR_OFFSET + i] = tx_eth_dst_addr.range(47 - 8 * i, 40 - 8 * i);
            }
            for (int i = 0; i < 6; ++i) {
            #pragma HLS PIPELINE
                tx_ping_buf[ETH_SRC_ADDR_OFFSET + i] = tx_eth_src_addr.range(47 - 8 * i, 40 - 8 * i);
            }
            for (int i = 0; i < 2; ++i) {
            #pragma HLS PIPELINE
                tx_ping_buf[ETH_TYPE_OFFSET + i] = tx_eth_type.range(15 - 8 * i, 8 - 8 * i);
            }
            tx_ping_buf[IP_VER_IHL_OFFSET] = tx_ip_ver_ihl;
            tx_ping_buf[IP_TYPE_OFFSET] = tx_ip_type;
            for (int i = 0; i < 2; ++i) {
            #pragma HLS PIPELINE
                tx_ping_buf[IP_ID_OFFSET + i] = tx_ip_id.range(15 - 8 * i, 8 - 8 * i);
            }
            for (int i = 0; i < 2; ++i) {
            #pragma HLS PIPELINE
                tx_ping_buf[IP_FRAGMENT_OFFSET + i] = tx_ip_fragment.range(15 - 8 * i, 8 - 8 * i);
            }
            tx_ping_buf[IP_TTL_OFFSET] = tx_ip_ttl;
            tx_ping_buf[IP_PROTOCOL_OFFSET] = tx_ip_protocol;
            for (int i = 0; i < 2; ++i) {
            #pragma HLS PIPELINE
                tx_ping_buf[UDP_CHECKSUM_OFFSET + i] = tx_udp_checksum.range(15 - 8 * i, 8 - 8 * i);
            }

            ap_uint<8> tx_ping_ctrl;
            ap_uint<8> tx_eth_src_addr_array[8];
            for (int i = 0; i < 6; ++i) {
                tx_eth_src_addr_array[i] = tx_eth_src_addr.range(47 - 8 * i, 40 - 8 * i);
            }
            for (int i = 0; i < 8; ++i) {
            #pragma HLS PIPELINE
                base[TX_PING_DATA_OFFSET + i] = tx_eth_src_addr_array[i];
            }
            tx_ping_ctrl = (ap_uint<8>)0x3;
            memcpy(base + TX_PING_CTRL_OFFSET, &tx_ping_ctrl, 1);
            txState = WAIT_MAC;
            break;
        }
        case WAIT_MAC: {
            ap_uint<8> tx_ping_ctrl;
            memcpy(&tx_ping_ctrl, base + TX_PING_CTRL_OFFSET, 1);
            if (tx_ping_ctrl.range(1, 0) == (ap_uint<2>)0) {
                txState = TX_FIRST;
            }
            break;
                       }
        case TX_FIRST:
            if (!tx_data.empty() && !tx_meta.empty() && !tx_length.empty()) {
                tx_length.read();
                tx_data_offset   = UDP_PAYLOAD_OFFSET;
                axiWord w = tx_data.read();
                for (int i = 0; i < 8; ++i) {
                    if (w.keep.bit(i)){
                        tx_ping_buf[tx_data_offset++] = w.data.range(7 + 8 * i, 8 * i);
                    }
                }

                metadata meta = tx_meta.read();
                tx_ip_src_addr = meta.sourceSocket.addr;
                tx_udp_src_port = meta.sourceSocket.port;
                tx_ip_dst_addr = meta.destinationSocket.addr;
                tx_udp_dst_port = meta.destinationSocket.port;
                for (int i = 0; i < 4; ++i) {
                #pragma HLS PIPELINE
                    tx_ping_buf[IP_SRC_ADDR_OFFSET + i] = meta.sourceSocket
                                                              .addr.range(31 - 8 * i, 24 - 8 * i);
                }
                for (int i = 0; i < 4; ++i) {
                #pragma HLS PIPELINE
                    tx_ping_buf[IP_DST_ADDR_OFFSET + i] = meta.destinationSocket
                                                              .addr.range(31 - 8 * i, 24 - 8 * i);
                }
                for (int i = 0; i < 2; ++i) {
                #pragma HLS PIPELINE
                    tx_ping_buf[UDP_SRC_PORT_OFFSET + i] = meta.sourceSocket
                                                               .port.range(15 - 8 * i, 8 - 8 * i);
                }
                for (int i = 0; i < 2; ++i) {
                #pragma HLS PIPELINE
                    tx_ping_buf[UDP_DST_PORT_OFFSET + i] = meta.destinationSocket
                                                               .port.range(15 - 8 * i, 8 - 8 * i);
                }


                if (w.last) {
                    txState = TX_WRITE;
                } else {
                    txState = TX_REST;
                }
            }
            break;
        case TX_REST:
            if (!tx_data.empty()) {
                axiWord w = tx_data.read();
                for (int i = 0; i < 8; ++i) {
                #pragma HLS PIPELINE
                    if (w.keep.bit(i)) {
                        tx_ping_buf[tx_data_offset++] = w.data.range(63 - 8 * i, 56 - 8 * i);
                    }
                }
                if (w.last) {
                    txState = TX_WRITE;
                }
            }
            break;
        case TX_WRITE:
            if (intr_cnt > 32) {
                ap_uint<8> tx_ping_ctrl;
                memcpy(&tx_ping_ctrl, base + TX_PING_CTRL_OFFSET, 1);
                if (tx_ping_ctrl.bit(0) == 0) {
                    tx_ip_len = tx_data_offset - IP_VER_IHL_OFFSET;
                    tx_udp_len = tx_data_offset - UDP_SRC_PORT_OFFSET;
                    tx_ip_checksum = calc_chksum(tx_ip_ver_ihl,
                                                 tx_ip_type,
                                                 tx_ip_len,
                                                 tx_ip_id,
                                                 tx_ip_fragment,
                                                 tx_ip_ttl,
                                                 tx_ip_protocol,
                                                 tx_ip_src_addr,
                                                 tx_ip_dst_addr);
                    for (int i = 0; i < 2; ++i) {
                    #pragma HLS PIPELINE
                        tx_ping_buf[IP_LEN_OFFSET + i] = tx_ip_len.range(15 - 8 * i, 8 - 8 * i);
                    }
                    for (int i = 0; i < 2; ++i) {
                    #pragma HLS PIPELINE
                        tx_ping_buf[UDP_LEN_OFFSET + i] = tx_udp_len.range(15 - 8 * i, 8 - 8 * i);
                    }
                    for (int i = 0; i < 2; ++i) {
                    #pragma HLS PIPELINE
                        tx_ping_buf[IP_CHECKSUM_OFFSET + i] = tx_ip_checksum.range(15 - 8 * i, 8 - 8 * i);
                    }
                    tx_data_offset += 2;

                    //memcpy(base + TX_PING_DATA_OFFSET, tx_ping_buf, 64);
                    //memcpy(base + TX_PING_DATA_OFFSET, tx_ping_buf, tx_data_offset);
                    //for (int i = 0; i < tx_data_offset; ++i) {
                    for (int i = 0; i < 64; ++i) {
                    #pragma HLS PIPELINE
                        base[(ap_uint<8>)TX_PING_DATA_OFFSET + i] = tx_ping_buf[i];
                    }
                    memcpy(base + TX_PING_LEN_OFFSET, &tx_data_offset, 1);

                    tx_ping_ctrl = ((ap_uint<7>)tx_ping_ctrl.range(7, 1), (ap_uint<1>)1);
                    memcpy(base + TX_PING_CTRL_OFFSET, &tx_ping_ctrl, 1);

                    txState = TX_FIRST;
                }
                intr_cnt = 0;
            }
            break;
    }



    /* RX */
    switch (rxState) {
        case RX_READ:
            rx_payload_offset = UDP_PAYLOAD_OFFSET;
            memcpy(&rx_ping_ctrl, base + RX_PING_CTRL_OFFSET, 1);
            if (rx_ping_ctrl.bit(0) == 1) {
                //memcpy(rx_ping_buf, base + RX_PING_DATA_OFFSET, UDP_PAYLOAD_OFFSET);
                for (ap_uint<8> i = 0; i < (ap_uint<8>)UDP_PAYLOAD_OFFSET; ++i) {
                #pragma HLS PIPELINE
                    rx_ping_buf[i] = base[RX_PING_DATA_OFFSET + i];
                }
                ap_uint<16> dst_port = (rx_ping_buf[UDP_DST_PORT_OFFSET],
                                        rx_ping_buf[UDP_DST_PORT_OFFSET + 1]);

                ap_uint<1> open = 0;
                for (int i = 0; i < 8; i++) {
                #pragma HLS PIPELINE
                    if (dst_port == open_port[i]) {
                        open = 1;
                        break;
                    }
                }
                if (open) {
                    ap_uint<16> len = (rx_ping_buf[IP_LEN_OFFSET], rx_ping_buf[IP_LEN_OFFSET + 1]);
                    rx_payload_len = len - LEN_IP_UDP_HEADER;
                    for (int i = 0; i < rx_payload_len; ++i) {
                    #pragma HLS PIPELINE
                        rx_ping_buf[UDP_PAYLOAD_OFFSET + i] = base[RX_PING_DATA_OFFSET + UDP_PAYLOAD_OFFSET + i];
                    }

                    ap_uint<3> padding = rx_payload_len.range(2, 0);
                    for (ap_uint<3> i = 0; i < padding; ++i) {
                    #pragma HLS PIPELINE
                        rx_ping_buf[UDP_PAYLOAD_OFFSET + rx_payload_len + i] = 0;
                    }

                    rxState = RX_FIRST;
                }

                rx_ping_ctrl = ((ap_uint<7>)rx_ping_ctrl.range(7, 1), (ap_uint<1>)0);
                memcpy(base + RX_PING_CTRL_OFFSET, &rx_ping_ctrl, 1);
            }
            break;
        case RX_FIRST:
            if (!rx_data.full() && !rx_meta.full()) {
                axiWord w;
                if (rx_payload_len > 8) {
                    w.data = (rx_ping_buf[rx_payload_offset+7],
                             (rx_ping_buf[rx_payload_offset+6],
                             (rx_ping_buf[rx_payload_offset+5],
                             (rx_ping_buf[rx_payload_offset+4],
                             (rx_ping_buf[rx_payload_offset+3],
                             (rx_ping_buf[rx_payload_offset+2],
                             (rx_ping_buf[rx_payload_offset+1],
                              rx_ping_buf[rx_payload_offset])))))));
                    rx_payload_offset += 8;
                    rx_payload_len -= 8;
                    w.keep = 0xff;
                    w.last = 0;
                    rxState = RX_REST;
                } else {
                    ap_uint<8> data[8];
                    w.keep = 0;
                    for (int i = 0; i < rx_payload_len; ++i) {
                        data[i] = rx_ping_buf[rx_payload_offset++];
                        w.keep |= (1 << i);
                    }
                    for (int i = rx_payload_len; i < 8; ++i) {
                        data[i] = 0;
                    }
                    w.data = (data[7],
                             (data[6],
                             (data[5],
                             (data[4],
                             (data[3],
                             (data[2],
                             (data[1],
                              data[0])))))));
                    w.last = 1;
                    rxState = RX_READ;
                }
                rx_data.write(w);

                metadata meta;
                meta.sourceSocket.addr = (rx_ping_buf[IP_SRC_ADDR_OFFSET],
                                         (rx_ping_buf[IP_SRC_ADDR_OFFSET + 1],
                                         (rx_ping_buf[IP_SRC_ADDR_OFFSET + 2],
                                          rx_ping_buf[IP_SRC_ADDR_OFFSET + 3])));
                meta.sourceSocket.port = (rx_ping_buf[UDP_SRC_PORT_OFFSET],
                                          rx_ping_buf[UDP_SRC_PORT_OFFSET + 1]);
                meta.destinationSocket.addr =  (rx_ping_buf[IP_DST_ADDR_OFFSET],
                                               (rx_ping_buf[IP_DST_ADDR_OFFSET + 1],
                                               (rx_ping_buf[IP_DST_ADDR_OFFSET + 2],
                                                rx_ping_buf[IP_DST_ADDR_OFFSET + 3])));
                meta.destinationSocket.port = (rx_ping_buf[UDP_DST_PORT_OFFSET],
                                               rx_ping_buf[UDP_DST_PORT_OFFSET + 1]);
                rx_meta.write(meta);
            }
            break;
        case RX_REST:
            if (!rx_data.full()) {
                axiWord w;
                w.data = (rx_ping_buf[rx_payload_offset+7],
                         (rx_ping_buf[rx_payload_offset+6],
                         (rx_ping_buf[rx_payload_offset+5],
                         (rx_ping_buf[rx_payload_offset+4],
                         (rx_ping_buf[rx_payload_offset+3],
                         (rx_ping_buf[rx_payload_offset+2],
                         (rx_ping_buf[rx_payload_offset+1],
                          rx_ping_buf[rx_payload_offset])))))));
                rx_payload_offset += 8;
                if (rx_payload_len > 8) {
                    rx_payload_len -= 8;
                    w.keep = 0xff;
                    w.last = 0;
                } else {
                    w.keep = 0;
                    for (int i = 0; i < rx_payload_len; ++i) {
                    #pragma HLS PIPELINE
                        w.keep |= (1 << i);
                    }
                    w.last = 1;
                    rxState = RX_READ;
                }
                rx_data.write(w);
            }
            break;
    }
}
