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


def extract_dict_as_string(dict_as_str: bytearray, dict_info: bytearray, k: int) -> (list, list, list):
    pointer_term_length = calculate_pointer_term_length(len(dict_as_str))
    info_pointer = 0
    items = list()
    frequency = list()
    posting_list = list()

    block_siz = FREQUENCY_LENGTH + POINTER_POSTING_LIST_LENGTH + pointer_term_length + 3 * \
                (FREQUENCY_LENGTH + POINTER_POSTING_LIST_LENGTH + 1)

    seg = 0
    while len(dict_info[info_pointer:]) < block_siz:

        if seg % k == 0:
            frequency.append(dict_info[info_pointer: info_pointer + FREQUENCY_LENGTH])
            info_pointer += FREQUENCY_LENGTH

            posting_list.append(dict_info[info_pointer: info_pointer + POINTER_POSTING_LIST_LENGTH])
            info_pointer += POINTER_POSTING_LIST_LENGTH

            info_pointer += pointer_term_length

            seg = 1

        else:

            frequency.append(dict_info[info_pointer: info_pointer + FREQUENCY_LENGTH])
            info_pointer += FREQUENCY_LENGTH

            posting_list.append(dict_info[info_pointer: info_pointer + POINTER_POSTING_LIST_LENGTH])
            info_pointer += POINTER_POSTING_LIST_LENGTH

            info_pointer += 1

            seg += 1

    term_pointer = 0
    while term_pointer < len(dict_as_str):
        term_len = dict_as_str[term_pointer]

        items.append(dict_as_str[term_pointer: term_pointer + term_len])

        term_pointer += term_len

    return items, frequency, posting_list


def make_dict_as_string(items: list, frequency: list, posting_list: list, k: int = 4) -> (bytearray, bytearray):
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
            dict_info += (current_pointer + 1). \
                to_bytes(length=POINTER_TERM_LENGTH, byteorder='big')  # POINTER_TERM_LENGTH bytes

            seg = 1  # 1-> seg
        else:
            dict_info += seg.to_bytes(length=1, byteorder='big')  # 1 byte

            seg += 1  # seg == 1, 2 , ..., k-1

        current_pointer += dict_as_str[current_pointer] + 1

    return dict_as_str, bytearray(dict_info)


if __name__ == '__main__':
    pass
