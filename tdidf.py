from math import log10
from os import sep
from indexing import POSTING_LIST_SAVING_PATH_NAME, DICTIONARY_SAVING_PATH_NAME, load_weights, load_posting_list
from indexing import DICTIONARY_INFO_NAME, DICTIONARY_AS_STR_NAME, load_docs_siz
from indexing import posting_list_name_file, posting_list_segment_name, SOURCE_NUMBER
from indexing import posting_list_weight_segment_name, POSTING_LIST_WEIGHT_SAVING_PATH_NAME, name_of_weight_file

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


def get_posting_list_addr_and_name(word: str):
    """
    return address and file's name
    :param word:
    :return: address, file's name
    """
    return (
            POSTING_LIST_SAVING_PATH_NAME + sep + posting_list_segment_name(word),
            posting_list_name_file(word)
    )


def get_weights_addr_and_name(word: str):
    return (
            POSTING_LIST_WEIGHT_SAVING_PATH_NAME + sep + posting_list_weight_segment_name(word),
            name_of_weight_file(word)
    )


def get_docs(addr: str, file_name: str):

    with open(addr + sep + file_name, 'rb') as fin:
        return decompress_posting_list(bytearray(fin.read()))


def cosine_score(q_terms: list, doc_siz):
    scores = dict()
    lengths = dict()

    for q in q_terms:
        weight_list_addr, weight_list_name = get_weights_addr_and_name(q)

        q_posting_list = load_posting_list(q)
        q_posting_list_siz = len(q_posting_list)
        q_weights = load_weights(weight_list_addr, weight_list_name)

        q_weight_in_query = calculate_tdidf(q_terms.count(q), q_posting_list_siz, SOURCE_NUMBER)

        for i in range(q_posting_list_siz):
            if scores.__contains__(q_posting_list[i]):
                scores[q_posting_list[i]] += calculate_tdidf(
                    q_weights[i],
                    q_posting_list_siz,
                    SOURCE_NUMBER
                ) * q_weight_in_query
            else:
                scores[q_posting_list[i]] = calculate_tdidf(
                    q_weights[i],
                    q_posting_list_siz,
                    SOURCE_NUMBER
                ) * q_weight_in_query

    for i in scores.keys():
        lengths[i] = doc_siz[i-1]

    for key in scores.keys():
        scores[key] = scores[key]/lengths[key]

    return scores



