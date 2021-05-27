from unittest import TestCase
import posting_list_compression as plc
from dictionary_compression import compress_dictionary, decompress_dictionary
import dictionary_compression as dc


class TestPostingListCompression(TestCase):
    __test_id = [2, 12, 27, 127, 1127, 4127]

    # def test_all(self):
    #     self.test_variable_byte()
    #     self.test_compress_posting_list()
    #     self.test_decompress_posting_list()

    def test_variable_byte(self):
        self.assertEqual(bytearray(b'\x82'), plc.variable_byte(2))
        self.assertEqual(bytearray(b'\x8f'), plc.variable_byte(15))
        self.assertEqual(bytearray(b'\x21\x9d'), plc.variable_byte(4253))
        print('variable_byte is successful.')

    def test_compress_posting_list(self):
        p = plc.compress_posting_list(self.__test_id)

        res_id = bytearray(b'\x82\x8a\x8f\xe4\x07\xe8\x17\xB8')
        self.assertEqual(res_id, p)

        print('compress_posting_list is successful.')

    def test_decompress_posting_list(self):
        p = plc.compress_posting_list(self.__test_id)
        p = plc.decompress_posting_list(p)

        self.assertEqual(self.__test_id.copy(), p)

        print('decompress_posting_list is successful.')


class TestDictionaryCompression(TestCase):
    __items = ['سلام', 'خوبی', 'چطوری', 'ااامشکل']
    __freq_list = [469, 60090, 4, 235]
    __posting_list = [256, 8188, 125, 2]
    __pointer_to_dict_as_list = [0, 9, 18, 29, 44]

    # def test_all(self):
    #     self.test_compress_dictionary()
    #     self.test_decompress_dictionary()

    def test_compress_dictionary(self):
        dict_as_string, dict_info = compress_dictionary(self.__items,
                                                        self.__freq_list,
                                                        self.__posting_list)
        curr_p = 0

        pointer_len = dc.calculate_pointer_term_length(len(dict_as_string))
        seg = 0
        for i in range(4):
            self.assertEqual(
                dict_info[curr_p: curr_p + dc.FREQUENCY_LENGTH],
                int.to_bytes(self.__freq_list[i],
                             length=dc.FREQUENCY_LENGTH,
                             byteorder='big')
            )

            curr_p += dc.FREQUENCY_LENGTH

            self.assertEqual(
                dict_info[curr_p: curr_p + dc.POINTER_POSTING_LIST_LENGTH],
                int.to_bytes(self.__posting_list[i],
                             length=dc.POINTER_POSTING_LIST_LENGTH,
                             byteorder='big')
            )

            curr_p += dc.POINTER_POSTING_LIST_LENGTH

            if seg % dc.K_SEGMENT == 0:
                self.assertEqual(
                    self.__pointer_to_dict_as_list[i],
                    int.from_bytes(dict_info[curr_p: curr_p + pointer_len],
                                   byteorder='big')
                )
                curr_p += pointer_len
                seg = 1
            else:
                self.assertEqual(
                    seg,
                    int.from_bytes(dict_info[curr_p: curr_p + 1],
                                   byteorder='big')
                )
                curr_p += 1
                seg += 1

        print('compress_dictionary is successful.')

    def test_decompress_dictionary(self):
        dict_as_string, dict_info = compress_dictionary(self.__items,
                                                        self.__freq_list,
                                                        self.__posting_list)
        items, frequency, posting_list = decompress_dictionary(dict_as_string, dict_info)

        self.assertEqual(items, self.__items)
        self.assertListEqual(frequency, self.__freq_list)
        self.assertListEqual(posting_list, self.__posting_list)

        print('decompress_dictionary is successful.')


if __name__ == '__main__':
    pass
