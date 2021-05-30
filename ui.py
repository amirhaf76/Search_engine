import re
from indexing import per_regex
from search_engine import SearchEngine


def get_command():
    # co = re.compile(r'(?:(-\w+\s*\w+)|(\w+))')
    # co1 = re.compile(r'(?:-\w+|\w+)')
    co = re.compile(f'(-[a-zA-Z_]+)|({per_regex()})')

    se = SearchEngine()
    # print(se.show())

    logs = {
        1: 'It was successful',
        -1: 'There isn\'t available any results!',
        0: 'There is no query'
    }

    while True:

        commands = input('>> ')
        terms = list(map(lambda tp: tp[1], co.findall(commands)))
        if len(terms) > 0:
            res, log = se.search(terms)
            if log == 1:
                print(res)
            print(logs[log])

            # Todo show content

        # for i in co.finditer(commands):
        #     print(i.group(2))
        # print(co.findall(commands))

        if ('-exit', '') in co.findall(commands):
            break


if __name__ == '__main__':
    get_command()
