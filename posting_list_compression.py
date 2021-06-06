def variable_byte(bin_n: int):

    if bin_n < 128:
        return bytearray(int.to_bytes(bin_n + 128, length=1, byteorder='big'))
    else:
        list_of_bytes = bytearray(0)
        end_byt = True
        while bin_n > 128:

            if end_byt:
                end_byt = False
                list_of_bytes = (128 + (bin_n & 127)).to_bytes(length=1, byteorder='big') + list_of_bytes
            else:
                list_of_bytes = (bin_n & 127).to_bytes(length=1, byteorder='big') + list_of_bytes

            bin_n >>= 7

        else:
            list_of_bytes = bin_n.to_bytes(length=1, byteorder='big') + list_of_bytes

        return bytearray(list_of_bytes)


def compress_posting_list(list_of_doc_ids: list) -> bytearray:

    prev = 0
    list_of_bytes = bytearray(0)

    for doc_id in list_of_doc_ids:

        list_of_bytes += variable_byte(abs(doc_id - prev))
        prev = doc_id

    return list_of_bytes


def decompress_posting_list(byt_posting_list: bytearray):
    nums = []
    holder = 0
    prev = 0

    for b in byt_posting_list:

        if b >= 128:
            nums.append(
                ((b & 127) + holder) + prev
            )
            prev = nums[-1]
            holder = 0
        else:
            holder += b
            holder <<= 7

    return nums


if __name__ == '__main__':
    pass
