import socket
import base64
import sys
import threading
from rtp_packet import RtpPacket

packet_buffer = []


def listen(port):
    # Initialize the UDP sockets and listen on specified port.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", port))
    print "LISTENING ON PORT 1111...."

    while True:

        received_rtp_data = s.recv(2480)

        if received_rtp_data:

            # Construct RTP packet
            rtp_packet = RtpPacket()
            rtp_packet.decode(received_rtp_data)

            # End of message, break off.
            if base64.b64decode(rtp_packet.payload) == "TERM":
                # print "TERM RECEIVED, BREAKING..."
                break
            else:
                # print "PACKET RECEIVED, ADDING TO QUEUE"
                packet_buffer.append(rtp_packet)

    return packet_buffer


# packets should be a list of rtp packets
def sort_packets(packets):
    return sorted(packets, key=return_sequence)


def return_sequence(e):
    return e.seqNum()


def decode_message(packets):
    output = ""
    sorted_packets = sort_packets(packets)
    for p in sorted_packets:
        output += base64.b64decode(p.get_payload())
    return output


def main(port):
    thread = threading.Thread(target=listen, args=[port])
    thread.start()
    thread.join()


if __name__ == "__main__":
    main(int(sys.argv[1]))
    print decode_message(packet_buffer)
