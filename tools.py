from random import shuffle
import time


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


def binary_search_tuple(e, list_of_e: list, index=0):
    rear = 0
    head = len(list_of_e) - 1

    while True:
        if head < rear:
            return None
        print(rear, head)

        centre = int((head + rear)/2)

        if list_of_e[centre][index] == e:
            return centre

        if head == rear:
            return None

        if e < list_of_e[centre][index]:
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

    list_of[start: h_2+1] = temp


def merge_lists(list_1: list, list_2: list, repetition=False):
    r_1 = 0
    r_2 = 0
    h_1 = len(list_1) - 1
    h_2 = len(list_2) - 1
    temp = []

    while r_1 <= h_1 and r_2 <= h_2:

        if list_1[r_1] < list_2[r_2]:
            temp.append(list_1[r_1])
            r_1 += 1
        elif list_1[r_1] > list_2[r_2]:
            temp.append(list_2[r_2])
            r_2 += 1
        else:
            temp.append(list_1[r_1])
            r_1 += 1
            if not repetition:
                r_2 += 1

    while r_1 <= h_1:
        temp.append(list_1[r_1])
        r_1 += 1

    while r_2 <= h_2:
        temp.append(list_2[r_2])
        r_2 += 1

    return temp


def merge_list_tuple(list_of: list, r_1, h_1, r_2, h_2, comp_index=0):
    start = r_1
    temp = []

    while r_1 <= h_1 and r_2 <= h_2:

        if list_of[r_1][comp_index] <= list_of[r_2][comp_index]:
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

    list_of[start: h_2+1] = temp


def merge_sort(list_of: list, merge_func=merge):
    siz = len(list_of)

    blk_siz = 1

    while blk_siz <= siz:
        block_r = 0

        while True:

            if block_r + 2*blk_siz - 1 < siz:
                merge_func(list_of, block_r, block_r + blk_siz - 1, block_r + blk_siz, block_r + 2*blk_siz - 1)
                block_r += 2*blk_siz
                continue

            elif block_r + blk_siz < siz:
                merge_func(list_of, block_r, block_r + blk_siz - 1, block_r + blk_siz, siz - 1)
                break
            else:
                break

        blk_siz *= 2


def intersection(doc_ids_lists: list, similarity_count=None):

    comparison = list()
    found_doc_id = []

    if similarity_count is None:
        similarity_count = [len(doc_ids_lists)]

    for doc_lst in doc_ids_lists:
        if len(doc_lst) > 0:
            comparison.append(doc_lst.pop(0))
    print('start', comparison)

    while True:
        for i in set(comparison):

            if comparison.count(i) in similarity_count:
                if i not in found_doc_id:
                    print(comparison.count(i), i)
                    found_doc_id.append(i)

        print(f'min: {min(comparison)}')
        index_of_min = comparison.index(min(comparison))

        if len(doc_ids_lists[index_of_min]) > 0:
            comparison[index_of_min] = doc_ids_lists[index_of_min].pop(0)
            print(comparison[index_of_min], comparison)
        else:
            print(comparison)
            print('end')
            break

    return found_doc_id


if __name__ == '__main__':

    # a = merge_lists_without_repetition(list(range(0, 50, 2)), list(range(0, 40, 5)))
    # print(a)

    a = [list(range(11)),
         list(range(0, 11, 2)),
         list(range(0, 11, 3))]
    print(a)
    b = intersection(a)
    print(b)

    # c = list(range(100))
    # t = 20*list('timeo'.__iter__())
    # # shuffle(c)
    # shuffle(t)
    # z = list(zip(t, c))
    # print(z)
    # s = time.time()
    # merge_sort(z, merge_func=merge_list_tuple)
    # print(time.time() - s)
    # print(z)
