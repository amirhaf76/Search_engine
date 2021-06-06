from unittest import TestCase
from dictionary_compression import compress_dictionary, decompress_dictionary
from search_engine import SearchEngine

import dictionary_compression as dc
import posting_list_compression as plc
import correctness_filter as cf


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


class TestSearchEngine(TestCase):
    se = SearchEngine()
    list_of_word = se.show()

    def test_search(self):
        print(self.se.search(['جوانان']))
        print(self.se.search(['جوان']))
        print(self.se.search(['جوانان', 'آب']))


class TestCorrectnessFilter(TestCase):
    se = SearchEngine()
    list_of_word = se.show()

    dict_words = {
        'اسپانسرها': [1, 23, 45],
        'بزرگتر': [1, 45, 48],
        'بزرگ': [2, 47, 100],
        'ارزشمند': [23, 43, 64],
        'ارزش': [1, 54],
        'رفتید': [3, 7, 990,3434],
        'رفته‌ام': [1,5,65,7777]
    }

    def test_replace_letters(self):

        self.assertEqual(
            'اب',
            cf.replace_letters('آب'),
        )

        self.assertEqual(
            'ابی',
            cf.replace_letters('آبي')
        )

    def test_filter_dict_from_suffix(self):
        v = list(self.dict_words.keys())
        for word in v:
            cf.filter_dict_from_suffix(word, self.dict_words)
        print(self.dict_words)

    def test_filter_verbs_in_dict(self):
        v = list(self.dict_words.keys())
        for word in v:
            cf.filter_verbs_in_dict(word, self.dict_words)
        print(self.dict_words)

    def test_filter_dictionary(self):
        cf.filter_dictionary(self.dict_words)
        print(self.dict_words)

    def test_suffix_detector_1(self):

        for word in self.list_of_word:
            res = cf.suffix_detector_1(word, self.list_of_word)
            if res is not None:
                print(word, res)

    def test_suffix_detector_2(self):

        for word in self.list_of_word:
            res = cf.suffix_detector_2(word, self.list_of_word)
            if res is not None:
                print(word, res)

    def test_suffix_detector_3(self):

        for word in self.list_of_word:
            res = cf.suffix_detector_3(word, self.list_of_word)
            if res is not None:
                print(word, res)

    def test_suffix_detector_4(self):

        for word in self.list_of_word:
            res = cf.suffix_detector_4(word, self.list_of_word)
            if res is not None:
                print(word, res)

    def test_filter_word_of_special_plural_verbs(self):

        for word in self.list_of_word:
            res = cf.filter_word_of_special_plural_verbs(word)
            if res is not None:
                print(word, res)

    def test_filter_word_as_verb(self):

        for word in self.list_of_word:
            res = cf.filter_word_as_verb(word)
            if res is not None:
                print(word, res)




if __name__ == '__main__':
    pass
