from dictionary_compression import decompress_dictionary
from posting_list_compression import decompress_posting_list
from indexing import load_posting_list, load_dictionary_bytes
from correctness_filter import filter_word
from tools import intersection, binary_search

SEARCH_ENGINE_LOG = {
        2: 'There is no intersection between results!',
        1: 'It was successful',
        -1: 'There isn\'t available any results!',
        0: 'There is no query'
}


class SearchEngine:

    def __init__(self):
        dict_as_str, dict_info = load_dictionary_bytes()

        # pointer_posting_list is unsuitable for now
        temp_tuple = decompress_dictionary(dict_as_str, dict_info)

        self.__terms_list, self.__freq_list, self.__pointer_posting_list = temp_tuple

    def search(self, list_of_terms: list) -> (list, int):
        """
        result and log number
        :param list_of_terms:
        :return:
        """
        if len(list_of_terms) == 0:
            return [], SEARCH_ENGINE_LOG[0]

        # one word
        elif len(list_of_terms) == 1:
            return self.search_one_word(list_of_terms[0])

        # more than one word
        elif len(list_of_terms) > 1:
            return self.search_multi_word(list_of_terms)

    def show(self):
        return self.__terms_list

    def search_one_word(self, term: str):
        term = filter_word(term, self.__terms_list)

        if term is None:
            return [], SEARCH_ENGINE_LOG[-1]

        index = binary_search(term, self.__terms_list)

        if index is None:
            return [], SEARCH_ENGINE_LOG[-1]

        # byte_posting_list = load_posting_list(list_of_terms[0])
        # refs = decompress_posting_list(byte_posting_list)
        refs = load_posting_list(term)

        return refs, 1

    def search_multi_word(self, list_of_terms: list):
        refs = []
        for term in list_of_terms:

            term = filter_word(term, self.__terms_list)
            if term is None:
                continue

            index = binary_search(term, self.__terms_list)

            if index is None:
                continue

            # byte_posting_list = load_posting_list(term)

            refs.append(
                # (term, decompress_posting_list(byte_posting_list))
                (term, load_posting_list(term))
            )

        if len(refs) == 0:
            return [], -1

        res = intersection(
            list(map(lambda t: t[1], refs))
        )

        if len(res) == 0:
            return res, 2

        return res, 1


if __name__ == '__main__':
    pass
