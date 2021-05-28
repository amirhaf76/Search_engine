from dictionary_compression import decompress_dictionary
from posting_list_compression import decompress_posting_list
from indexing import load_posting_list, load_dictionary_bytes
from tools import intersection, binary_search_tuple, merge_sort


class SearchEngine:

    def __init__(self):
        dict_as_str, dict_info = load_dictionary_bytes()

        # pointer_posting_list is unsuitable for now
        temp_tuple = decompress_dictionary(dict_as_str, dict_info)
        self.__terms_list, self.__freq_list, self.__pointer_posting_list = temp_tuple

    def search(self, list_of_terms: list) -> list:
        if len(list_of_terms) == 0:
            return ['There is no query!']

        elif len(list_of_terms) == 1:
            byte_posting_list = load_posting_list(list_of_terms[0])
            refs = decompress_posting_list(byte_posting_list)
            return refs
        else:
            return ['need implication']

    def show(self):
        return self.__terms_list


if __name__ == '__main__':
    pass
