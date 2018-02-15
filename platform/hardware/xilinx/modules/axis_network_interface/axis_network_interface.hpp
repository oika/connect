#include "polytheos_platform.hpp"

void axis_network_interface(ap_uint<8>                  *base,
                            hls::stream<axiWord>        &tx_data,
                            hls::stream<metadata>       &tx_meta,
                            hls::stream<axiWord>        &rx_data,
                            hls::stream<metadata>       &rx_meta,
                            hls::stream<ap_uint<16> >   &open_port_request,
                            hls::stream<ap_uint<1> >    &open_port_reply);
