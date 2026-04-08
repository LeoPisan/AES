import ctypes
import unittest

from aes import aes


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.rijndael = ctypes.CDLL("./rijndael.so")
        self.buffer = b"\x00\x01\x02\x03\x04\x05\x06\x07"
        self.buffer += b"\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
        self.buffer_matrix = aes.bytes2matrix(self.buffer)
        self.block = ctypes.create_string_buffer(self.buffer)

    def test_sub_bytes(self):
        actual_result = self.rijndael.sub_bytes(self.block, 0)  # 0 = AES_BLOCK_128
        expected_result = aes.sub_bytes(self.buffer_matrix)
        self.assertEqual(actual_result, expected_result)


if __name__ == "__main__":
    unittest.main()
