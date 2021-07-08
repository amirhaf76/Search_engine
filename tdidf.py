from math import log10
from os import sep
from pandas import read_csv
from re import compile
from indexing import POSTING_LIST_SAVING_PATH_NAME, DICTIONARY_SAVING_PATH_NAME, SOURCE_FILE
from indexing import DICTIONARY_INFO_NAME, DICTIONARY_AS_STR_NAME
from indexing import posting_list_name_file, posting_list_segment_name, per_regex, name_of_weight_file
from correctness_filter import filter_word
from posting_list_compression import decompress_posting_list
from dictionary_compression import decompress_dictionary


def calculate_tdidf(tf: int, df: int, number_of_docs: int) -> float:
    """

    :param tf: term frequency
    :param df: number of the documents which have term t
    :param number_of_docs: total number of the documents
    :return: td-idf weight
    """
    return (1+log10(tf)) * log10(number_of_docs / df)


def get_words_from_dict():

    with open(DICTIONARY_SAVING_PATH_NAME + sep + DICTIONARY_AS_STR_NAME, 'rb') as fin:
        dict_as_str = fin.read()

    with open(DICTIONARY_SAVING_PATH_NAME + sep + DICTIONARY_INFO_NAME, 'rb') as fin:
        dict_info = fin.read()

    items, frq, psl = decompress_dictionary(bytearray(dict_as_str), bytearray(dict_info))

    return items


def get_addr_and_name(word: str):
    """
    return address and file's name
    :param word:
    :return: address, file's name
    """
    return (
            POSTING_LIST_SAVING_PATH_NAME + sep + posting_list_segment_name(word),
            posting_list_name_file(word)
    )


def get_docs(addr: str, file_name: str):

    with open(addr + sep + file_name, 'rb') as fin:
        return decompress_posting_list(bytearray(fin.read()))




def calculate_all_score_of_posting_list():

    # CSV file
    df = read_csv(SOURCE_FILE)
    df = df.set_index('id', drop=False)

    if not list(df.columns) == ['id', 'content', 'url']:
        print(f'[Error] {SOURCE_FILE} doesn\'t have certain columns!!!')
        return False

    words = get_words_from_dict()

    if words is None:
        return False

    per_com = compile(per_regex())

    for w in words:
        w_addr, w_name_inv = get_addr_and_name(w)

        w_docs = get_docs(w_addr, w_name_inv)

        if w_docs is None:
            print(f'[Error][tdidf.py][65] file "{w_name_inv}" wasn\'t in {w_addr}')
            break

        tf_s = []

        for wd in w_docs:
            content = per_com.findall(df.at[wd, 'content'])

            w = filter_word(w, words)

            if w is None:
                break

            for i in range(len(content)):
                content[i] = filter_word(content[i], words)

            tf = content.count(w)
            tf_s.append(tf)

        # save_weights(w_addr, w, tf_s)
        # print(w_addr)
        # print(w)
        # print(name_of_weight_file(w))
        # print(w_docs)
        # print(tf_s)
        # print(load_weights(w_addr, w))
        # break

    return True


#
#
# # CSV file
#     df = read_csv(SOURCE_FILE)
#     df = df.set_index('id', drop=False)
#
#     if not list(df.columns) == ['id', 'content', 'url']:
#         print(f'[Error] {SOURCE_FILE} doesn\'t have certain columns!!!')
#         return False
#
#     words = get_words_from_dict()
#
#     if words is None:
#         return False
#
#     per_com = compile(per_regex())
#
#     for w in words[100:]:
#         w_addr, w_name_inv = get_addr_and_name(w)
#
#         w_docs = get_docs(w_addr, w_name_inv)
#
#         if w_docs is None:
#             print(f'[Error][tdidf.py][65] file "{w_name_inv}" wasn\'t in {w_addr}')
#             break
#
#         tf_s = []
#         cm = compile(w)
#
#         for wd in w_docs:
#             content = per_com.findall(df.at[wd, 'content'])
#
#             w = filter_word(w, words)
#             tf = len(
#                 cm.findall(df.at[wd, 'content'])
#             )
#             tf_s.append(tf)
#
#         save_weights(w_addr, w, tf_s)
#         print(w_addr)
#         print(w)
#         print(name_of_weight_file(w))
#         print(tf_s)
#         print(load_weights(w_addr, w))
#         break
