class Decoder:

    @staticmethod
    def decode_int(message):
        return int.from_bytes(message, byteorder='big', signed=True)

    @staticmethod
    def decode_string(message):
        return str(message, 'utf-8')