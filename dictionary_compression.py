from math import log2, ceil

AVERAGE_WORD_LENGTH = 10
FREQUENCY_LENGTH = 4
POINTER_POSTING_LIST_LENGTH = 4
K_SEGMENT = 4


def calculate_pointer_term_length(length: int, per=True) -> int:
    if per:
        return ceil(log2(length * AVERAGE_WORD_LENGTH * 2) / 8)
    else:
        return ceil(log2(length * AVERAGE_WORD_LENGTH * 1) / 8)


def decompress_dictionary(dict_as_str: bytearray, dict_info: bytearray, k: int = K_SEGMENT) -> (list, list, list):
    """
    items, frequency, posting_list
    :param dict_as_str:
    :param dict_info:
    :param k:
    :return:
    """
    pointer_term_length = calculate_pointer_term_length(len(dict_as_str))
    info_pointer = 0
    items = list()
    frequency = list()
    posting_list = list()

    seg = 0
    while info_pointer < len(dict_info):

        if seg % k == 0:
            frequency.append(
                int.from_bytes(dict_info[info_pointer: info_pointer + FREQUENCY_LENGTH], 'big')
            )
            info_pointer += FREQUENCY_LENGTH

            posting_list.append(
                int.from_bytes(dict_info[info_pointer: info_pointer + POINTER_POSTING_LIST_LENGTH], 'big')
            )
            info_pointer += POINTER_POSTING_LIST_LENGTH

            info_pointer += pointer_term_length

            seg = 1

        else:

            frequency.append(
                int.from_bytes(dict_info[info_pointer: info_pointer + FREQUENCY_LENGTH], 'big')
            )
            info_pointer += FREQUENCY_LENGTH

            posting_list.append(
                int.from_bytes(dict_info[info_pointer: info_pointer + POINTER_POSTING_LIST_LENGTH], 'big')
            )
            info_pointer += POINTER_POSTING_LIST_LENGTH

            info_pointer += 1

            seg += 1

    term_pointer = 0
    while term_pointer < len(dict_as_str):
        term_len = dict_as_str[term_pointer]

        term_pointer += 1

        items.append(dict_as_str[term_pointer: term_pointer + term_len].decode())

        term_pointer += term_len

    return items, frequency, posting_list


def compress_dictionary(items: list, frequency: list, posting_list: list, k: int = K_SEGMENT) -> (bytearray, bytearray):
    """
    index block:
        frequency - pointer to posting list - pointer to term in dict_as_str (point to length of term) +
        3 * (frequency - pointer to posting list - seg)

    block size:
        FREQUENCY_LENGTH + POINTER_POSTING_LIST_LENGTH + POINTER_TERM_LENGTH
        3 * (FREQUENCY_LENGTH + POINTER_POSTING_LIST_LENGTH + 1 Byte)

    :param items:
    :param frequency:
    :param posting_list:
    :param k:
    :return:
    """
    dict_as_str = bytes(0)
    dict_info = bytes(0)

    for i in items:
        dict_as_str += len(i.encode()).to_bytes(length=1, byteorder='big')
        dict_as_str += i.encode()

    dict_as_str = bytearray(dict_as_str)

    POINTER_TERM_LENGTH = calculate_pointer_term_length(len(dict_as_str))
    current_pointer = 0
    seg = 0
    for i in items:

        dict_info += frequency[items.index(i)].to_bytes(length=FREQUENCY_LENGTH, byteorder='big')
        dict_info += posting_list[items.index(i)].to_bytes(length=POINTER_POSTING_LIST_LENGTH, byteorder='big')

        if seg % k == 0:
            dict_info += current_pointer. \
                to_bytes(length=POINTER_TERM_LENGTH, byteorder='big')  # POINTER_TERM_LENGTH bytes

            seg = 1  # 1-> seg
            current_pointer += POINTER_TERM_LENGTH
        else:
            dict_info += seg.to_bytes(length=1, byteorder='big')  # 1 byte

            seg += 1  # seg == 1, 2 , ..., k-1
            current_pointer += 1

    return dict_as_str, bytearray(dict_info)


if __name__ == '__main__':
    pass
