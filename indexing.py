import re
import pandas as pd
import time
from tools import merge_sort, merge_list_tuple
import os

DICT_SAVING_PATH_NAME = 'dictLib'


class Token:

    def __init__(self, doc_id: int, term: str):
        self.__doc_ids = [doc_id]
        self.__term = term

    def add_doc_id(self, new_doc_id):
        self.__doc_ids.append(new_doc_id)

    def get_term(self):
        return self.__term

    def get_doc_ids(self):
        return self.__doc_ids.copy()

    def get_frequency(self):
        return len(self.__doc_ids)

    def get_frequency_of(self, doc_id: int):
        return self.__doc_ids.count(doc_id)

    def __str__(self):
        return f'<term: {self.__term}, doc_ids: {self.__doc_ids}>'

    def __repr__(self):
        return f'<term: {self.__term}, doc_ids: {self.__doc_ids}>'

    def __eq__(self, other):
        return self.__term.__eq__(other)

    def __le__(self, other):
        return self.__term.__le__(other)

    def __lt__(self, other):
        return self.__term.__lt__(other)

    def __ge__(self, other):
        return self.__term.__ge__(other)

    def __gt__(self, other):
        return self.__term.__gt__(other)


def index_file(c: str, data_: bytearray):

    with open(f'{c}_inverse.char', 'ab') as out_put:
        out_put.write(data_)


def per_alphabet():
    return 'آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئء'


def per_regex():
    return f'[{per_alphabet()}]+'


def per_num():
    return '[۱۲۳۴۵۶۷۸۹۰]+'


def cp():
    return re.compile(per_regex())


def index_block():
    pass


def parser_dict(df: pd.DataFrame, col: str, doc_ic: str, comp, num=-1) -> dict:
    buff_dict = dict()

    if num == -1:
        num = len(df)

    for i in range(num):
        temp = comp.findall(df[col].iloc[i])
        for t in temp:
            if not buff_dict.__contains__(t):
                buff_dict[t] = Token(int(df[doc_ic].iloc[i]), t)
            else:
                buff_dict[t].add_doc_id(int(df[doc_ic].iloc[i]))

    return buff_dict


def parser_list(df: pd.DataFrame, col: str, doc_id: str, comp, num=-1) -> list:

    if not df.__contains__(col):
        raise Exception(f'df doesn\'t have column {col}')
    elif not df.__contains__(doc_id):
        raise Exception(f'df doesn\'t have column {doc_id}')

    list_of_term_id = list()

    if num == -1:
        num = len(df)

    for i in range(num):
        tokens = comp.findall(df[col].iloc[i])
        for t in tokens:
            list_of_term_id.append(
                (t, int(df[doc_id].iloc[i]))
            )

    return list_of_term_id


def storing(dict_of_token: dict):
    os.makedirs(DICT_SAVING_PATH_NAME, exist_ok=True)

    for c in per_alphabet():
        os.makedirs(f'{DICT_SAVING_PATH_NAME}\\{c}_{DICT_SAVING_PATH_NAME}', exist_ok=True)

    for term, token in dict_of_token.items():
        with open(f'{DICT_SAVING_PATH_NAME}\\'
                  f'{term[0]}_{DICT_SAVING_PATH_NAME}\\{term}_posting_list.txt', 'at') as out_put:
            out_put.write(','.join(map(lambda x: str(x), term.get_doc_ids())))


if __name__ == '__main__':
    # print(per_alpha())

    fin = pd.read_csv('IR_Spring2021_ph12_7k.csv')

    start = time.time()
    p = parser_list(fin, 'content', 'id', re.compile(per_regex()), 30)
    merge_sort(p, merge_func=merge_list_tuple)
    print(time.time() - start)
    print(p)
    # oo = list(map(lambda x: len(x.get_doc_ids()), p.values()))
    # print(oo)
    # s, t = make_dict_as_string(list(p.keys()), len(p.keys())*[5],
    #                            oo)

