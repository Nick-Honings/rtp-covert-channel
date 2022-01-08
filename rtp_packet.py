from time import time

HEADER_SIZE = 12


class RtpPacket:
    header = bytearray(HEADER_SIZE)

    def __init__(self):
        self.payload = None

    def encode(self, version, padding, extension, cc, seq_num, marker, pt, ssrc, payload):
        header = bytearray(HEADER_SIZE)
        timestamp = int(time())
        # Encode the RTP packet
        # Fill the header bytearray with RTP header fields
        header[0] = (header[0] | version << 6) & 0xC0  # 2 bits
        header[0] = (header[0] | padding << 5)  # 1 bit
        header[0] = (header[0] | extension << 4)  # 1 bit
        header[0] = (header[0] | (cc & 0x0F))  # 4 bits
        header[1] = (header[1] | marker << 7)  # 1 bit
        header[1] = (header[1] | (pt & 0x7f))  # 7 bits
        header[2] = (seq_num & 0xFF00) >> 8  # 16 bits total, this is first 8
        header[3] = (seq_num & 0xFF)  # second 8
        header[4] = (timestamp >> 24)  # 32 bit timestamp
        header[5] = (timestamp >> 16) & 0xFF
        header[6] = (timestamp >> 8) & 0xFF
        header[7] = (timestamp & 0xFF)
        header[8] = (ssrc >> 24)  # 32 bit ssrc
        header[9] = (ssrc >> 16) & 0xFF
        header[10] = (ssrc >> 8) & 0xFF
        header[11] = ssrc & 0xFF

        # Set RtpPacket's header and payload.
        self.header = header
        self.payload = payload

    def decode(self, byte_stream):
        """Decode the RTP packet."""
        self.header = bytearray(byte_stream[:HEADER_SIZE])
        self.payload = byte_stream[HEADER_SIZE:]

    def version(self):
        """Return RTP version."""
        return int(self.header[0] >> 6)

    def seqNum(self):
        """Return sequence (frame) number."""
        seq_num = self.header[2] << 8 | self.header[3]
        return int(seq_num)

    def timestamp(self):
        """Return timestamp."""
        timestamp = self.header[4] << 24 | self.header[5] << 16 | self.header[6] << 8 | self.header[7]
        return int(timestamp)

    def payload_type(self):
        """Return payload type."""
        pt = self.header[1] & 127
        return int(pt)

    def get_payload(self):
        """Return payload."""
        return self.payload

    def get_packet(self):
        """Return RTP packet."""
        return self.header + self.payload
