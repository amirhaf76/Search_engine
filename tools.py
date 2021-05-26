from random import shuffle


def binary_search(e, list_of_e: list):
    rear = 0
    head = len(list_of_e) - 1

    while True:
        if head < rear:
            return None
        print(rear, head)

        centre = int((head + rear)/2)

        if list_of_e[centre] == e:
            return centre

        if head == rear:
            return None

        if e < list_of_e[centre]:
            head = centre - 1
        else:
            rear = centre + 1


def merge(list_of: list, r_1, h_1, r_2, h_2):
    start = r_1
    temp = []

    while r_1 <= h_1 and r_2 <= h_2:

        if list_of[r_1] <= list_of[r_2]:
            temp.append(list_of[r_1])
            r_1 += 1
        else:
            temp.append(list_of[r_2])
            r_2 += 1

    while r_1 <= h_1:
        temp.append(list_of[r_1])
        r_1 += 1

    while r_2 <= h_2:
        temp.append(list_of[r_2])
        r_2 += 1

    for e in temp:
        list_of[start] = e
        start += 1


def merge_sort(list_of: list):
    siz = len(list_of)

    blk_siz = 1

    while blk_siz <= siz:
        block_r = 0

        while True:

            if block_r + 2*blk_siz - 1 < siz:
                merge(list_of, block_r, block_r + blk_siz - 1, block_r + blk_siz, block_r + 2*blk_siz - 1)
                block_r += 2*blk_siz
                continue

            elif block_r + blk_siz < siz:
                merge(list_of, block_r, block_r + blk_siz - 1, block_r + blk_siz, siz - 1)
                break
            else:
                break

        blk_siz *= 2


if __name__ == '__main__':

    c = list(range(1000))
    shuffle(list(range(1000)))
    print(c)
    merge_sort(c)
    print(c)
