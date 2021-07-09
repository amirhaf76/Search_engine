from unittest import TestCase
from dictionary_compression import compress_dictionary, decompress_dictionary
from search_engine import SearchEngine
from tools import *
from random import randint

import dictionary_compression as dc
import posting_list_compression as plc
import correctness_filter as cf
from word_info import WordInfo


class TestPostingListCompression(TestCase):
    __test_id = [2, 12, 27, 127, 1127, 4127]

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
        print(self.se.search(['اب']))
        print(self.se.search(['جوان']))
        print(self.se.search(['جوان']))
        print(self.se.search(['شنا', 'آب']))


class TestCorrectnessFilter(TestCase):
    se = SearchEngine()
    list_of_word = se.show()

    dict_words = {
        'اسپانسرها': [1, 23, 45],
        'بزرگتر': [1, 45, 48],
        'بزرگ': [2, 47, 100],
        'ارزشمند': [23, 43, 64],
        'ارزش': [1, 54],
        'رفتید': [3, 7, 990, 3434],
        'رفته‌ام': [1, 5, 65, 7777]
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


class TestTools(TestCase):

    def test_merge_lists(self):
        temp = list(range(0, 10))
        temp1 = list(range(0, 10))
        print(merge_lists(temp, temp1))


class TestTDIDF(TestCase):

    def test_get_words_from_dict(self):
        from tdidf import get_words_from_dict
        temp = get_words_from_dict()
        self.assertIsNotNone(temp)
        self.assertTrue(isinstance(temp, list))
        print(f'test_get_words_from_dict is successful.')

    def test_get_addr_and_name(self):
        from tdidf import get_posting_list_addr_and_name
        from tdidf import POSTING_LIST_SAVING_PATH_NAME, posting_list_segment_name, posting_list_name_file
        from tdidf import get_words_from_dict
        from os import listdir, sep

        w = get_words_from_dict()[0]
        addr, name = get_posting_list_addr_and_name(w)
        self.assertEqual(POSTING_LIST_SAVING_PATH_NAME + sep + posting_list_segment_name(w),
                         addr)
        self.assertEqual(name, posting_list_name_file(w))
        self.assertTrue(name in listdir(addr))

        print(f'{self.test_get_addr_and_name.__name__} is successful.')

        return addr, name

    def test_get_docs(self):
        from tdidf import get_docs
        addr, name = self.test_get_addr_and_name()
        print(get_docs(addr, name))

    def test_compress_weights(self):
        from tdidf import compress_weights
        numbers = [0, 3072, 3092, 1, 0, 2621460, 78, 6]
        numbers_in_bytes = [b'\x00',
                            b'\x02', b'\x0C\x00',
                            b'\x02', b'\x0C\x14',
                            b'\x01', b'\x01',
                            b'\x00',
                            b'\x03', b'\x28\x00\x14',
                            b'\x01', b'\x4E',
                            b'\x01', b'\x06']
        stream_bytes = bytes()
        for b in numbers_in_bytes:
            stream_bytes += b

        self.assertEqual(stream_bytes, compress_weights(numbers))

    def test_decompress_weights(self):
        from tdidf import compress_weights, decompress_weights
        from random import randint
        numbers = [0, 3072, 3092, 1, 0, 2621460, 78, 6]

        self.assertEqual(numbers,
                         decompress_weights(compress_weights(numbers)))

        numbers = list(randint(0, 3000000) for _ in range(100))
        self.assertEqual(numbers,
                         decompress_weights(compress_weights(numbers)))

    def test_save_and_load_weights(self):
        from os import makedirs, removedirs, remove, listdir, sep
        from tdidf import save_weights, load_weights
        from random import randint

        numbers = list(randint(0, 3000000) for _ in range(100))

        addr = f'{self.test_get_addr_and_name.__name__}'
        word = 'word'

        makedirs(addr, exist_ok=True)
        save_weights(addr, word, numbers)

        try:
            self.assertEqual(numbers, load_weights(addr, word))
        except Exception as e:
            print(e)

        for f in listdir(addr):
            remove(addr + sep + f)
        removedirs(addr)

    def test_calculate_all_score_of_posting_list(self):
        from tdidf import calculate_all_score_of_posting_list
        calculate_all_score_of_posting_list()


class TestWordInfo(TestCase):

    def test_word_info_class(self):
        self._word = 'word'
        self._word_info = WordInfo(self._word)

        self.assertEqual(self._word, self._word_info.get_word())
        self.assertEqual([], self._word_info.get_doc_ids())
        self.assertEqual([], self._word_info.get_count_each_docs())

        doc_ids = [45, 787, 2, 6, 8, 12, 82, 46]
        doc_ids.sort()
        counters = [12, 42, 1, 1, 2, 7, 100, 660]

        for doc_id in doc_ids:
            self._word_info.add_doc_id(doc_id)

        for i in range(len(counters)):
            for _ in range(counters[i]-1):
                self._word_info.plus_counter_of_doc(doc_ids[i])

        self.assertEqual(doc_ids, self._word_info.get_doc_ids())
        self.assertEqual(counters, self._word_info.get_count_each_docs())

        doc_ids1 = [10, 33, 56, 8, 2342, 2]
        doc_ids1.sort()
        counters1 = [1, 7878, 455, 87, 55, 1]

        self._word_info.merge_list(doc_ids1, counters1)

        new_docs = self._word_info.get_doc_ids()
        new_docs.sort()
        self.assertEqual(new_docs, self._word_info.get_doc_ids())

        new_counters = self._word_info.get_count_each_docs()

        join_counters = [13, 42, 7879, 455, 1, 87, 2, 7, 55, 100, 660, 1]
        join_docs = doc_ids + doc_ids1
        join_docs.sort()
        for i in range(len(doc_ids) + len(doc_ids1)):
            index = new_docs.index(join_docs[i])
            self.assertEqual(join_counters[index], new_counters[index])











if __name__ == '__main__':
    pass
