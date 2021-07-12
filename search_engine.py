from dictionary_compression import decompress_dictionary
from indexing import load_posting_list, load_dictionary_bytes, load_docs_siz
from correctness_filter import filter_word
from tools import intersection, binary_search, heap_sort_tuple
from tfidf import cosine_score

SEARCH_ENGINE_LOG = {
        2: 'There is no intersection between results!',
        1: 'It was successful',
        -1: 'There isn\'t available any results!',
        0: 'There is no query'
}


class SearchEngine:

    def __init__(self):
        dict_as_str, dict_info = load_dictionary_bytes()

        temp_tuple = decompress_dictionary(dict_as_str, dict_info)

        self.__terms_list, self.__freq_list, self.__pointer_posting_list = temp_tuple

        self.__docs_siz = dict(load_docs_siz())

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
        """
        return res, log
        :param term:
        :return: res, log
        """
        term = filter_word(term, self.__terms_list)

        if term is None:
            return [], -1

        index = binary_search(term, self.__terms_list)

        if index is None:
            return [], -1

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

            refs.append(
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

    def score_search_base(self, list_of_terms: list, k: int):
        """
        result and log number, k == 0 return all docs in order of max score
        :param k:
        :param list_of_terms:
        :return:
        """
        if len(list_of_terms) == 0:
            return [], SEARCH_ENGINE_LOG[0]

        # one word
        elif len(list_of_terms) == 1:
            return self.score_search_base_one_word(list_of_terms[0], k)

        # more than one word
        elif len(list_of_terms) > 1:
            return self.score_search_base_multi_word(list_of_terms, k)

    def score_search_base_one_word(self, term: str, k: int):
        term = filter_word(term, self.__terms_list)

        if term is None:
            return [], -1

        index = binary_search(term, self.__terms_list)

        if index is None:
            return [], -1

        r = cosine_score([term], self.__docs_siz)
        r = list(r.items())
        heap_sort_tuple(r, 1, k)

        return list(
            map(lambda x: x[0], r[-1 * k:])
        ), 1

    def score_search_base_multi_word(self, terms: list, k: int):
        refs = []
        for term in terms:

            term = filter_word(term, self.__terms_list)
            if term is None:
                continue

            index = binary_search(term, self.__terms_list)

            if index is None:
                continue

            refs.append(
                term
            )

        if len(refs) == 0:
            return [], -1

        r = cosine_score(refs, self.__docs_siz)
        r = list(r.items())
        heap_sort_tuple(r, 1, k)

        return list(
            map(lambda x: x[0], r[-1 * k:])
        ), 1


if __name__ == '__main__':
    pass
