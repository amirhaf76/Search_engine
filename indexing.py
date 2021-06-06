import re
import pandas as pd
import os

from tools import merge_lists, merge_sort
from posting_list_compression import compress_posting_list, decompress_posting_list
from dictionary_compression import compress_dictionary, decompress_dictionary, POINTER_POSTING_LIST_LENGTH
from correctness_filter import filter_dictionary

POSTING_LIST_SAVING_PATH_NAME = 'posting_lists'
DICTIONARY_SAVING_PATH_NAME = 'dict_list'

DICTIONARY_AS_STR_NAME = 'dict_as_str'
DICTIONARY_INFO_NAME = 'dict_info'


def posting_list_name_file(term: str):
    return f'{term}_posting_list'


class Token:

    def __init__(self, doc_id: int, term: str):
        self.__doc_ids = [doc_id]
        self.__term = term

    def add_doc_id(self, new_doc_id):
        self.__doc_ids.append(new_doc_id)

    def get_term(self):
        return self.__term

    def get_doc_ids(self):
        return self.__doc_ids.copy()

    def get_frequency(self):
        return len(self.__doc_ids)

    def get_frequency_of(self, doc_id: int):
        return self.__doc_ids.count(doc_id)

    def __str__(self):
        return f'<term: {self.__term}, doc_ids: {self.__doc_ids}>'

    def __repr__(self):
        return f'<term: {self.__term}, doc_ids: {self.__doc_ids}>'

    def __eq__(self, other):
        return self.__term.__eq__(other)

    def __le__(self, other):
        return self.__term.__le__(other)

    def __lt__(self, other):
        return self.__term.__lt__(other)

    def __ge__(self, other):
        return self.__term.__ge__(other)

    def __gt__(self, other):
        return self.__term.__gt__(other)


def make_index_file(c: str, data_: bytearray):

    with open(f'{c}_inverse.char', 'ab') as out_put:
        out_put.write(data_)


def per_alphabet():
    return 'آأابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ‌كءي'


def per_regex():
    return f'[{per_alphabet()}]+'


def per_num():
    return '[۱۲۳۴۵۶۷۸۹۰]+'


def make_compiler():
    return re.compile(per_regex())


def parser_dict(df: pd.DataFrame, col: str, doc_id: str, comp, num=-1) -> dict:

    if not df.__contains__(col):
        raise Exception(f'df doesn\'t have column {col}')
    elif not df.__contains__(doc_id):
        raise Exception(f'df doesn\'t have column {doc_id}')

    buff_dict = dict()

    if num == -1:
        num = len(df)

    for i in range(num):
        try:
            temp = comp.findall(df[col].iloc[i])
            for t in temp:
                if not buff_dict.__contains__(t):
                    buff_dict[t] = [int(df[doc_id].iloc[i])]
                else:
                    if not buff_dict[t].__contains__(int(df[doc_id].iloc[i])):
                        buff_dict[t].append(int(df[doc_id].iloc[i]))
        except TypeError:
            print(f'type error in source {i} - index.')

    return buff_dict


def save_dict_posting_lists(dict_of_token: dict):
    os.makedirs(POSTING_LIST_SAVING_PATH_NAME, exist_ok=True)

    for c in per_alphabet():
        os.makedirs(f'{POSTING_LIST_SAVING_PATH_NAME}\\{c}_{POSTING_LIST_SAVING_PATH_NAME}', exist_ok=True)

    for term, token in dict_of_token.items():
        path = f'{POSTING_LIST_SAVING_PATH_NAME}' + os.sep + f'{term[0]}_{POSTING_LIST_SAVING_PATH_NAME}'
        name = posting_list_name_file(term)

        if name in os.listdir(path):
            with open(path + os.sep + name, f'rb') as out_put:
                li = decompress_posting_list(bytearray(out_put.read()))
                new_list = merge_lists(li, token)

            with open(path + os.sep + name, f'wb') as out_put:
                out_put.write(compress_posting_list(new_list))
        else:
            with open(path + os.sep + name, f'wb') as out_put:
                out_put.write(compress_posting_list(token))


def save_list_dictionary(term_list: list, freq_list: list, pointer_list: list):
    os.makedirs(DICTIONARY_SAVING_PATH_NAME, exist_ok=True)
    dict_as_str, dict_info = compress_dictionary(term_list, freq_list, pointer_list)

    path = f'{DICTIONARY_SAVING_PATH_NAME}'
    name = DICTIONARY_AS_STR_NAME

    with open(path + os.sep + name, f'wb+') as out_put:
        out_put.write(dict_as_str)

    path = f'{DICTIONARY_SAVING_PATH_NAME}'
    name = DICTIONARY_INFO_NAME

    with open(path + os.sep + name, f'wb+') as out_put:
        out_put.write(dict_info)


def load_dictionary_bytes():
    """
    dict_as_str, dict_info
    :return:
    """
    dict_as_str = None
    dict_info = None

    try:
        path = f'{DICTIONARY_SAVING_PATH_NAME}'
        name = DICTIONARY_AS_STR_NAME

        fin = open(path + os.sep + name, 'rb')

        dict_as_str = fin.read()

        fin.close()

    except IOError:
        print('[Search Engine][Error] dict_as_str file isn\'t available!')

    try:
        path = f'{DICTIONARY_SAVING_PATH_NAME}'
        name = DICTIONARY_INFO_NAME

        fin = open(path + os.sep + name, 'rb')

        dict_info = fin.read()

        fin.close()

    except IOError:
        print('[Search Engine][Error] dict_info isn\'t available!')

    return bytearray(dict_as_str), bytearray(dict_info)


def load_posting_list(term: str):
    posting_list = None
    try:
        path = f'{POSTING_LIST_SAVING_PATH_NAME}' + os.sep + f'{term[0]}_{POSTING_LIST_SAVING_PATH_NAME}'
        name = posting_list_name_file(term)

        fin = open(path + os.sep + name, 'rb')

        posting_list = fin.read()

        fin.close()
    except IOError:
        print(f'[Search Engine][Error] {term} file isn\'t available!')

    return bytearray(posting_list)


def preprocess(file_name: str, num: int):
    file_in = pd.read_csv(file_name)

    read_file = 0
    term_dict = {}

    while read_file < num:

        terms_ids = parser_dict(file_in[read_file: read_file + 100], 'content', 'id', re.compile(per_regex()), 100)
        read_file += 100

        for k, v in terms_ids.items():
            if term_dict.__contains__(k):
                term_dict[k] = merge_lists(term_dict[k], v, repetition=False)
            else:
                term_dict[k] = v

        print(f'{read_file}/{num} was tokenized.')

    filter_dictionary(term_dict)
    print(f'Dictionary was filtered successfully.')

    items_list = list(term_dict.keys())
    merge_sort(items_list)

    freq_list = []
    pointer_list = []

    for t in items_list:
        freq_list.append(len(term_dict[t]))
        pointer_list.append(POINTER_POSTING_LIST_LENGTH)

    save_dict_posting_lists(term_dict)
    print(f'Posting lists were saved successfully.')

    save_list_dictionary(items_list, freq_list, pointer_list)
    print(f'Dictionary were saved successfully.')

    print(f'Pre-processing is done')


if __name__ == '__main__':
    # for i in range(100, 200+1, 100):
    preprocess('IR_Spring2021_ph12_7k.csv', 1000)
