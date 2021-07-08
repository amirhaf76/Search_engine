from re import compile
import pandas as pd
import os
from word_info import WordInfo

from tools import merge_lists, merge_sort
from posting_list_compression import compress_posting_list, decompress_posting_list
from dictionary_compression import compress_dictionary, POINTER_POSTING_LIST_LENGTH
from correctness_filter import filter_dictionary

SOURCE_FILE = 'IR_Spring2021_ph12_7k.csv'
SOURCE_NUMBER = 5000

POSTING_LIST_SAVING_PATH_NAME = 'posting_lists'
POSTING_LIST_WEIGHT_SAVING_PATH_NAME = 'posting_list_weights'
DICTIONARY_SAVING_PATH_NAME = 'dict_list'

DICTIONARY_AS_STR_NAME = 'dict_as_str'
DICTIONARY_INFO_NAME = 'dict_info'


def posting_list_name_file(term: str):
    return f'{term}_posting_list'


def name_of_weight_file(term: str):
    return f'{posting_list_name_file(term)}_weight'


def posting_list_segment_name(term: str):
    return f'{term[0]}_{POSTING_LIST_SAVING_PATH_NAME}'


def posting_list_weight_segment_name(term: str):
    return f'{term[0]}_{POSTING_LIST_WEIGHT_SAVING_PATH_NAME}'


def per_alphabet():
    return 'آأابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ‌كءي'


def per_regex():
    return f'[{per_alphabet()}]+'


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
                    # buff_dict[t] = [int(df[doc_id].iloc[i])]
                    buff_dict[t] = WordInfo(t)
                    buff_dict[t].add_doc_id(int(df[doc_id].iloc[i]))
                else:
                    if buff_dict[t].exist_doc_id(int(df[doc_id].iloc[i])):
                        buff_dict[t].plus_counter_of_doc(int(df[doc_id].iloc[i]))
                    else:
                        buff_dict[t].add_doc_id(int(df[doc_id].iloc[i]))

                    # if not buff_dict[t].__contains__(int(df[doc_id].iloc[i])):
                    #     buff_dict[t].append(int(df[doc_id].iloc[i]))
        except TypeError:
            print(f'type error in source {i} - index.')

    return buff_dict


def save_dict_posting_lists(dict_of_token: dict):
    os.makedirs(POSTING_LIST_SAVING_PATH_NAME, exist_ok=True)

    for c in per_alphabet():
        # Todo need refactoring
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


def compress_weights(list_of_int: list):
    stream = bytes()

    for i in list_of_int:
        if i == 0:
            stream += bytes([0])
            continue

        bytes_count = 0
        num = 0
        while not i == 0:
            temp = i & 255
            i = (i - temp) >> 8

            num += temp << (8 * bytes_count)
            bytes_count += 1

        stream += bytes_count.to_bytes(1, 'big')
        stream += num.to_bytes(bytes_count, 'big')

    return stream


def decompress_weights(stream_bytes: bytes):
    stream_bytes = bytearray(stream_bytes)
    numbers = []

    curr_p = 0
    while curr_p < len(stream_bytes):

        if stream_bytes[curr_p] == 0:
            numbers.append(0)
            curr_p += 1
            continue

        siz = stream_bytes[curr_p]
        numbers.append(
            int.from_bytes(stream_bytes[curr_p + 1:curr_p + siz + 1],
                           'big')
        )

        curr_p += siz + 1

    return numbers


def save_weights(addr: str, term: str, number_list: list):

    name = name_of_weight_file(term)

    with open(addr + os.sep + name, 'wb') as out:
        out.write(compress_weights(number_list))


def load_weights(addr: str, term: str):

    name = name_of_weight_file(term)

    with open(addr + os.sep + name, 'rb') as fin:
        return decompress_weights(fin.read())


def save_all_word_info(list_of_word_infos: list):
    for c in per_alphabet():
        os.makedirs(POSTING_LIST_WEIGHT_SAVING_PATH_NAME + os.sep +
                    posting_list_weight_segment_name(c),
                    exist_ok=True)

    for w in list_of_word_infos:
        addr = POSTING_LIST_WEIGHT_SAVING_PATH_NAME + os.sep + posting_list_weight_segment_name(w.get_word()[0])
        save_weights(addr, w.get_word(), w.get_count_each_docs())


def preprocess(file_name: str, num: int):
    file_in = pd.read_csv(file_name)

    read_file = 0
    term_dict = {}

    while read_file < num:

        terms_ids = parser_dict(file_in[read_file: read_file + 100], 'content', 'id', compile(per_regex()), 100)
        read_file += 100

        for k, v in terms_ids.items():
            if term_dict.__contains__(k):
                term_dict[k].merge_list(v.get_doc_ids(), v.get_count_each_docs())
                # term_dict[k] = merge_lists(term_dict[k], v, repetition=False)
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

    save_posting_file = dict(
        map(lambda w: (w.get_word(), w.get_doc_ids()), term_dict.values())
    )
    # save_dict_posting_lists(term_dict)
    save_dict_posting_lists(save_posting_file)
    print(f'Posting lists were saved successfully.')

    save_list_dictionary(items_list, freq_list, pointer_list)
    print(f'Dictionary were saved successfully.')

    save_all_word_info(list(term_dict.values()))
    print(f'Posting lists were saved successfully.')

    print(f'Pre-processing is done')


if __name__ == '__main__':
    preprocess(SOURCE_FILE, SOURCE_NUMBER)
