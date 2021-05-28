import re
from indexing import per_regex
from search_engine import SearchEngine


def get_command():
    # co = re.compile(r'(?:(-\w+\s*\w+)|(\w+))')
    # co1 = re.compile(r'(?:-\w+|\w+)')
    co = re.compile(f'(-[a-zA-Z_]+)|({per_regex()})')

    se = SearchEngine()
    # print(se.show())

    while True:

        commands = input('>> ')
        print(co.findall(commands))
        terms = list(map(lambda tp: tp[1], co.findall(commands)))
        if len(terms) > 0:
            res = se.search(terms)
            print(res)

        for i in co.finditer(commands):
            print(i.group(2))
        print(co.findall(commands))

        if ('-exit', '') in co.findall(commands):
            break


if __name__ == '__main__':
    get_command()
