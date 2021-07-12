def binary_search(e, list_of_e: list):
    rear = 0
    head = len(list_of_e) - 1

    while True:
        if head < rear:
            return None

        centre = int((head + rear) / 2)

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

    list_of[start: h_2 + 1] = temp


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


def merge_tuple_lists(list_1: list, list_2: list, e: int = 0, repetition=False):
    r_1 = 0
    r_2 = 0
    h_1 = len(list_1) - 1
    h_2 = len(list_2) - 1
    temp = []

    while r_1 <= h_1 and r_2 <= h_2:

        if list_1[r_1][e] < list_2[r_2][e]:
            temp.append(list_1[r_1])
            r_1 += 1
        elif list_1[r_1][e] > list_2[r_2][e]:
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


def merge_sort(list_of: list, merge_func=merge):
    siz = len(list_of)

    blk_siz = 1

    while blk_siz <= siz:
        block_r = 0

        while True:

            if block_r + 2 * blk_siz - 1 < siz:
                merge_func(list_of, block_r, block_r + blk_siz - 1, block_r + blk_siz, block_r + 2 * blk_siz - 1)
                block_r += 2 * blk_siz
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

    while True:
        for i in set(comparison):

            if comparison.count(i) in similarity_count:
                if i not in found_doc_id:
                    found_doc_id.append(i)

        index_of_min = comparison.index(min(comparison))

        if len(doc_ids_lists[index_of_min]) > 0:
            comparison[index_of_min] = doc_ids_lists[index_of_min].pop(0)
        else:
            break

    return found_doc_id


def heapify(arr: list, n: int, i: int):
    largest = i

    right = 2 * i + 2
    left = 2 * i + 1

    if right < n and arr[right] > arr[largest]:
        largest = right

    if left < n and arr[left] > arr[largest]:
        largest = left

    if not largest == i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heapify_tuple(arr: list, n: int, i: int, e: int):
    smallest = i

    right = 2 * i + 2
    left = 2 * i + 1

    if right < n and arr[right][e] > arr[smallest][e]:
        smallest = right

    if left < n and arr[left][e] > arr[smallest][e]:
        smallest = left

    if not smallest == i:
        arr[i], arr[smallest] = arr[smallest], arr[i]
        heapify_tuple(arr, n, smallest, e)


def heap_sort(arr: list, k=0):
    if k < 1 or k > len(arr):
        k = len(arr)

    for i in range(len(arr) // 2 - 1, -1, -1):
        heapify(arr, len(arr), i)

    for i in range(len(arr) - 1, len(arr) - 1 - k, -1):  # len(arr) - 1 - k + 1 - 1
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


def heap_sort_tuple(arr: list, e: int, k=0):
    if k < 1 or k > len(arr):
        k = len(arr)

    for i in range(len(arr) // 2 - 1, -1, -1):
        heapify_tuple(arr, len(arr), i, e)

    for i in range(len(arr) - 1, len(arr) - 1 - k, -1):  # len(arr) - 1 - k + 1 - 1
        arr[i], arr[0] = arr[0], arr[i]
        heapify_tuple(arr, i, 0, e)


if __name__ == '__main__':
    pass
