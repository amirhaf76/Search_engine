from dictionary_compression import decompress_dictionary
from posting_list_compression import decompress_posting_list
from indexing import load_posting_list, load_dictionary_bytes
from tools import intersection, binary_search


class SearchEngine:

    def __init__(self):
        dict_as_str, dict_info = load_dictionary_bytes()

        # pointer_posting_list is unsuitable for now
        temp_tuple = decompress_dictionary(dict_as_str, dict_info)
        self.__terms_list, self.__freq_list, self.__pointer_posting_list = temp_tuple

    def search(self, list_of_terms: list) -> (list, int):
        if len(list_of_terms) == 0:
            return [], 0

        elif len(list_of_terms) == 1:
            index = binary_search(list_of_terms[0], self.__terms_list)

            if index is None:
                return [], -1

            byte_posting_list = load_posting_list(list_of_terms[0])
            refs = decompress_posting_list(byte_posting_list)

            return refs, 1
        elif len(list_of_terms) > 1:
            refs = []
            for term in list_of_terms:
                index = binary_search(term, self.__terms_list)

                if index is not None:

                    byte_posting_list = load_posting_list(term)

                    refs.append(
                        (term, decompress_posting_list(byte_posting_list))
                    )

            if len(refs) == 0:
                return [], -1
            res = intersection(
                list(map(lambda t: t[1], refs))
            )

            print(list(map(lambda t: t[0], refs)))
            return res, 1

    def show(self):
        return self.__terms_list


if __name__ == '__main__':
    pass
