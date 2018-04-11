class Encoder:

    @staticmethod
    def encode_int(integer):
        return integer.to_bytes(4, byteorder='big', signed=True)

    @staticmethod
    def encode_string(string):
        return Encoder.encode_int(len(string)) + bytearray(string, 'utf-8')