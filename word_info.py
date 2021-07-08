

class WordInfo:

    def __init__(self, word: str):
        self.__word = word
        self.__doc_ids = []
        self.__count_each_docs = []

    def get_word(self):
        return self.__word

    def set_word(self, word):
        self.__word = word

    def get_doc_ids(self):
        return self.__doc_ids.copy()

    def exist_doc_id(self, doc_id: int):
        return doc_id in self.__doc_ids

    def get_count_each_docs(self):
        return self.__count_each_docs.copy()

    def plus_counter_of_doc(self, doc_id: int):
        index = self.__doc_ids.index(doc_id)
        self.__count_each_docs[index] += 1

    def add_doc_id(self, doc_id):
        self.__doc_ids.append(doc_id)
        self.__count_each_docs.append(1)

    def merge_list(self, docs_ids: list, counters: list):
        list_1 = list(zip(docs_ids, counters))
        list_2 = list(zip(self.__doc_ids, self.__count_each_docs))

        res = []

        t1 = list_1.pop(0)
        t2 = list_2.pop(0)
        while True:

            if t1[0] < t2[0]:
                res.append(t1)
                if len(list_1) > 0:
                    t1 = list_1.pop(0)
                else:
                    res.append(t2)
                    res += list_2
                    break

            elif t1[0] > t2[0]:
                res.append(t2)
                if len(list_2) > 0:
                    t2 = list_2.pop(0)
                else:
                    res.append(t1)
                    res += list_1
                    break
            else:
                res.append((t1[0], t1[1] + t2[1]))
                if len(list_1) > 0 and len(list_2) > 0:
                    t1 = list_1.pop(0)
                    t2 = list_2.pop(0)
                else:
                    if len(list_1) > 0:
                        res += list_1
                    elif len(list_2) > 0:
                        res += list_2
                    break

        self.__doc_ids = list(
            map(lambda t: t[0], res)
        )
        self. __count_each_docs = list(
            map(lambda t: t[1], res)
        )

    def __len__(self):
        return len(self.__doc_ids)

    def __repr__(self):
        return f'<{self.__word}:{list(zip(self.__doc_ids, self.__count_each_docs))}>'



