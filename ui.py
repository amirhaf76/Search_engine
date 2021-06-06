import re
from pandas import DataFrame, read_csv
from indexing import per_regex
from search_engine import SearchEngine, SEARCH_ENGINE_LOG
from time import time


SOURCE_FILE_NAME = 'IR_Spring2021_ph12_7k.csv'


def get_source(file_name: str) -> DataFrame:
    return read_csv(file_name)


def show_result(df: DataFrame, lis_of_id: list, brief=True):

    for doc__id in lis_of_id:
        info = df.iloc[doc__id-1]
        print(f'id: {info["id"]}')

        if brief:
            print(f'content:\n{df[df["id"]==doc__id]["content"].to_string(index=False)}')
        else:
            print(f'content:\n{info["content"]}')

        print(f'url: {info["url"]}')

        print(40 * '_')


def get_command():
    co = re.compile(f'(-[a-zA-Z_]+)|({per_regex()})')

    se = SearchEngine()
    src = get_source(SOURCE_FILE_NAME)

    while True:

        inputs = input('>> ')
        cmd_parts = co.findall(inputs)

        terms = []
        commands = []

        for cmd, term in cmd_parts:
            if not term == '':
                terms.append(term)
            elif not cmd == '':
                commands.append(cmd)

        if len(terms) > 0:

            start_time = time()
            res, log = se.search(terms)
            end_time = time()

            if log == 1:
                if '-full' in commands:
                    show_result(src, res, brief=False)
                else:
                    show_result(src, res)

            print(f'{SEARCH_ENGINE_LOG[log]}\nruntime: {end_time - start_time:.10f}')

        if '-exit' in commands:
            break


if __name__ == '__main__':
    get_command()
