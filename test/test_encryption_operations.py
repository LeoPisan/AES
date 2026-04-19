import ctypes
import os
import unittest

from aes import aes

MESSAGE_NUMBER = 5
KEY_NUMBER = 5


# A few helpers
def random_block():
    """Generates a random block."""
    return os.urandom(16)


def make_c_block(data):
    """Converts a Python block to a C block."""
    return (ctypes.c_ubyte * 16)(*data)

def random_key(size=16):
    return os.urandom(size)

class AesTestCase(unittest.TestCase):
    # Setup methods
    @classmethod
    def setUpClass(cls):
        cls.rijndael = ctypes.CDLL("./rijndael.so")
        # These numerous lines define the signatures of functions from the C library
        cls.rijndael.sub_bytes.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_int
        ]
        cls.rijndael.sub_bytes.restype = None
        cls.rijndael.invert_sub_bytes.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_int,
        ]
        cls.rijndael.invert_sub_bytes.restype = None
        cls.rijndael.shift_rows.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_int,
        ]
        cls.rijndael.shift_rows.restype = None
        cls.rijndael.invert_shift_rows.argtypes= [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_int,
        ]
        cls.rijndael.invert_shift_rows.restype = None
        cls.rijndael.mix_columns.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_int,
        ]
        cls.rijndael.mix_columns.restype = None
        cls.rijndael.invert_mix_columns.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_int,
        ]
        cls.rijndael.invert_mix_columns.restype = None
        cls.rijndael.add_round_key.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_int,
        ]
        cls.rijndael.add_round_key.restype = None

    def setUp(self):
        self.buffers_list = [random_block() for _ in range(MESSAGE_NUMBER)]
        self.keys_list = [random_key() for _ in range(KEY_NUMBER)]

    # Actual tests
    def test_sub_bytes_128(self):
        for buffer in self.buffers_list:
            with self.subTest(buffer=buffer.hex()):
                block = (ctypes.c_ubyte * 16)(*buffer)
                buffer_matrix = aes.bytes2matrix(buffer)

                self.rijndael.sub_bytes(block, 0)  # 0 = AES_BLOCK_128

                aes.sub_bytes(buffer_matrix)
                expected_result = aes.matrix2bytes(buffer_matrix)

                actual_result = bytes(block)
                self.assertEqual(actual_result, expected_result)

    def test_invert_sub_bytes_128(self):
        for buffer in self.buffers_list:
            with self.subTest(buffer=buffer.hex()):
                block = (ctypes.c_ubyte * 16)(*buffer)
                buffer_matrix = aes.bytes2matrix(buffer)

                self.rijndael.invert_sub_bytes(block, 0)
                aes.inv_sub_bytes(buffer_matrix)
                expected_result = aes.matrix2bytes(buffer_matrix)

                actual_result = bytes(block)
                self.assertEqual(actual_result, expected_result)

    def test_shift_rows_128(self):
        for buffer in self.buffers_list:
            with self.subTest(buffer=buffer.hex()):
                block = (ctypes.c_ubyte * 16)(*buffer)
                buffer_matrix = aes.bytes2matrix(buffer)

                self.rijndael.shift_rows(block, 0)
                aes.shift_rows(buffer_matrix)
                expected_result = aes.matrix2bytes(buffer_matrix)

                actual_result = bytes(block)
                self.assertEqual(actual_result, expected_result)

    def test_invert_shift_rows_128(self):
        for buffer in self.buffers_list:
            with self.subTest(buffer=buffer.hex()):
                block = (ctypes.c_ubyte * 16)(*buffer)
                buffer_matrix = aes.bytes2matrix(buffer)

                self.rijndael.invert_shift_rows(block, 0)
                aes.inv_shift_rows(buffer_matrix)
                expected_result = aes.matrix2bytes(buffer_matrix)

                actual_result = bytes(block)
                self.assertEqual(actual_result, expected_result)

    def test_mix_columns_128(self):
        for buffer in self.buffers_list:
            with self.subTest(buffer=buffer.hex()):
                block = (ctypes.c_ubyte * 16)(*buffer)
                buffer_matrix = aes.bytes2matrix(buffer)

                self.rijndael.mix_columns(block, 0)
                aes.mix_columns(buffer_matrix)

                expected_result = aes.matrix2bytes(buffer_matrix)
                actual_result = bytes(block)
                self.assertEqual(actual_result, expected_result)

    def test_invert_mix_columns_128(self):
        for buffer in self.buffers_list:
            with self.subTest(buffer=buffer.hex()):
                block = (ctypes.c_ubyte * 16)(*buffer)
                buffer_matrix = aes.bytes2matrix(buffer)

                self.rijndael.invert_mix_columns(block, 0)
                aes.inv_mix_columns(buffer_matrix)

                expected_result = aes.matrix2bytes(buffer_matrix)
                actual_result = bytes(block)
                self.assertEqual(actual_result, expected_result)

    def test_add_round_key_128(self):
        for buffer in self.buffers_list:
            for key in self.keys_list:
                with self.subTest(buffer=buffer.hex(), key=key.hex()):
                    block = (ctypes.c_ubyte * 16)(*buffer)
                    buffer_matrix = aes.bytes2matrix(buffer)

                    round_key = (ctypes.c_ubyte * 16)(*key)
                    round_key_matrix = aes.bytes2matrix(key)

                    self.rijndael.add_round_key(block, round_key, 0)
                    aes.add_round_key(buffer_matrix, round_key_matrix)

                    expected_result = aes.matrix2bytes(buffer_matrix)
                    actual_result = bytes(block)
                    self.assertEqual(actual_result, expected_result)
if __name__ == "__main__":
    unittest.main()
