import re


def get_command():
    co = re.compile(r'(-\w+\s*\w+)|(\w+)')
    co1 = re.compile(r'(?:-\w+|\w+)')

    while True:

        cmds = input('>> ')
        for i in co.finditer(cmds):
            print(i.group(2))
            print(co.findall(cmds))
        if ('', 'exit') in co.findall(cmds):
            break


if __name__ == '__main__':
    get_command()