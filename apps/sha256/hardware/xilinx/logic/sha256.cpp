#include "ap_int.h"
#include "hls_stream.h"
#include "connect_platform.hpp"
#include "sha256.hpp"
#include <iostream>

using namespace hls;
using namespace std;

ap_uint<256> calc_hash(ap_uint<32> nonce, ap_uint<1024> header)
{
    ap_uint<32>
        k[64] = {0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
                 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
                 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
                 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
                 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
                 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
                 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
                 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};
    ap_uint<32> h0 = 0x6a09e667;
    ap_uint<32> h1 = 0xbb67ae85;
    ap_uint<32> h2 = 0x3c6ef372;
    ap_uint<32> h3 = 0xa54ff53a;
    ap_uint<32> h4 = 0x510e527f;
    ap_uint<32> h5 = 0x9b05688c;
    ap_uint<32> h6 = 0x1f83d9ab;
    ap_uint<32> h7 = 0x5be0cd19;
    ap_uint<512> block[2];

    block[0] = header.range(1023, 512);
    //block[1] = (header.range(511, 416), (nonce, header.range(383, 0)));
    block[1] = header.range(511, 0) | ((ap_uint<512>)nonce << 384);
    //cout << hex << block[1] << endl;

    for (int i = 0; i < 2; ++i) {
        ap_uint<32> w[64];
        for (int j = 0; j < 16; ++j) {
            w[j] = block[i].range(511 - 32 * j, 480 - 32 * j);
        }
        for (int j = 16; j < 64; ++j) {
            ap_uint<32> s0 = (w[j - 15].range(6, 0), w[j - 15].range(31, 7))
                             ^ (w[j - 15].range(17, 0), w[j - 15].range(31, 18))
                             ^ (w[j - 15] >> 3);
            ap_uint<32> s1 = (w[j - 2].range(16, 0), w[j - 2].range(31, 17))
                             ^ (w[j - 2].range(18, 0), w[j - 2].range(31, 19))
                             ^ (w[j - 2] >> 10);
            w[j] = w[j - 16] + s0 + w[j - 7] + s1;
        }
        ap_uint<32> a = h0;
        ap_uint<32> b = h1;
        ap_uint<32> c = h2;
        ap_uint<32> d = h3;
        ap_uint<32> e = h4;
        ap_uint<32> f = h5;
        ap_uint<32> g = h6;
        ap_uint<32> h = h7;

        for (int j = 0; j < 64; ++j) {
            ap_uint<32> S1 = (e.range(5, 0), e.range(31, 6))
                             ^ (e.range(10, 0), e.range(31, 11))
                             ^ (e.range(24, 0), e.range(31, 25));
            ap_uint<32> ch = (e & f) ^ (~e & g);
            ap_uint<32> tmp1 = h + S1 + ch + k[j] + w[j];
            ap_uint<32> S0 = (a.range(1, 0), a.range(31, 2))
                             ^ (a.range(12, 0), a.range(31, 13))
                             ^ (a.range(21, 0), a.range(31, 22));
            ap_uint<32> maj = (a & b) ^ (a & c) ^ (b & c);
            ap_uint<32> tmp2 = S0 + maj;

            h = g;
            g = f;
            f = e;
            e = d + tmp1;
            d = c;
            c = b;
            b = a;
            a = tmp1 + tmp2;
        }

        h0 = h0 + a;
        h1 = h1 + b;
        h2 = h2 + c;
        h3 = h3 + d;
        h4 = h4 + e;
        h5 = h5 + f;
        h6 = h6 + g;
        h7 = h7 + h;
    }

    return (h0, (h1, (h2, (h3, (h4, (h5, (h6, h7)))))));
}

void sha256(stream<ap_uint<1024> >  &eventIn,
            stream<ap_uint<32> >    &resultOut,
            stream<ap_uint<1> >     &prepare_start,
            stream<ap_uint<1> >     &prepare_done)
            //ap_uint<256>            &final_hash)
{
#pragma HLS DATAFLOW
#pragma HLS INTERFACE ap_ctrl_none port=return

#pragma HLS INTERFACE axis register both port=eventIn
#pragma HLS INTERFACE axis register both port=resultOut
#pragma HLS INTERFACE axis register both port=prepare_start
#pragma HLS INTERFACE axis register both port=prepare_done

    static enum LogicState {LS_RUN = 0, LS_PREPARE} lState;
    static ap_uint<1>       searching = 0;
    static ap_uint<1024>    header;
    static ap_uint<32>      nonce = 0;
    static ap_uint<256>     threshold;

    if (!searching && !prepare_start.empty() && !prepare_done.full()) {
        prepare_done.write(prepare_start.read());
    }

    if (searching && !resultOut.full()) {
        ap_uint<256> final_hash;
        final_hash = calc_hash(nonce, header);
        if (final_hash < threshold) {
            resultOut.write(nonce);
            nonce = 0;
            searching = 0;
        }
        if (++nonce == 0) {
            resultOut.write(0);
            searching = 0;
        }
    } else if (!searching && !eventIn.empty()) {
        header = eventIn.read();
        //cout << hex << header << endl;
        ap_uint<32> nbits = header.range(447, 416);
        //cout << hex << nbits << endl;
        ap_uint<256> significand = (ap_uint<256>)nbits.range(23, 0);
        //cout << "significand: " << hex << significand << endl;
        ap_uint<8> exponent = nbits.range(31, 24) - 3;
        //cout << "exponent: " << dec << exponent << endl;
        //threshold = (ap_uint<256>)nbits.range(23, 0) << (8 * (nbits.range(31, 24) - 3));
        threshold = significand << (8 * exponent);
        //cout << "threshold: " << hex << threshold << endl;
        searching = 1;
    }

}
