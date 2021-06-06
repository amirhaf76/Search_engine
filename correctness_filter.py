import re
from tools import merge_lists, binary_search

TYPES_SUFFIX = [
    ['ه‌ام', 'ه‌ای', 'ه', 'ه‌ایم', 'ه‌اید', 'ه‌اند'],
    ['یم', 'ید', 'ند'],
    ['م', 'ی'],
    ['د']
]

SUFFIX_1 = [
    '‌ها',  # with half-space
    '‌های',  # with half-space
    '‌هایی',  # with half-space
    'ها',
    'های',
    'هایی',

]

SUFFIX_2 = [
    '‌تر',  # with half-space
    '‌ترین',  # with half-space
    'تر',
    'ترین',
]

SUFFIX_3 = [
    'ات',
    'گین',
    'اسا',
    'مند',
]

SUFFIX_4 = [
    'شان',
    'یان',
    'مان',
    'ان'
]

REPLACEMENT_LETTER = {
    'آ': 'ا',
    'ي': 'ی'
}


def replace_letters(word: str):
    new_word = False
    for letter in REPLACEMENT_LETTER.keys():
        if not word.count(letter) == 0:
            word = word.replace(letter, REPLACEMENT_LETTER[letter])
            new_word = True

    if new_word:
        return word
    else:
        return None


def suffix_detector_1(txt: str, ref_list: list):
    for s in SUFFIX_1:
        if s in txt[-1 * len(s):]:
            root = txt[:-1 * len(s)]
            search_res = binary_search(root, ref_list)
            if search_res is not None:
                return root

    return None


def suffix_detector_2(txt: str, ref_list: list):
    for c in SUFFIX_2:
        if c in txt[-1 * len(c):]:
            root = txt[:-1 * len(c)]
            search_res = binary_search(root, ref_list)
            if len(root) > 2 and search_res is not None:
                return root

    return None


def suffix_detector_3(txt: str, ref_list: list):
    for c in SUFFIX_3:
        if c in txt[-1 * len(c):]:
            root = txt[:-1 * len(c)]
            search_res = binary_search(root, ref_list)
            if len(root) > 2 and search_res is not None:
                return root

    return None


def suffix_detector_4(txt: str, ref_list: list):
    for c in SUFFIX_4:
        if c in txt[-1 * len(c):]:
            root = txt[:-1 * len(c)]
            search_res = binary_search(root, ref_list)
            if len(root) > 3 and search_res is not None:
                return root

    return None


SUFFIX_FUNCTIONS = [
    suffix_detector_1,
    suffix_detector_2,
    suffix_detector_3,
    suffix_detector_4,
]


def complex_words_detector(txt: str):
    if '\u200c' in txt:
        index = txt.index('\u200c')

        return txt[:index], txt[index + 1:]

    return None


def read_file(file_name: str):
    with open(f'{file_name}', 'rb') as f:
        words = (f.read().decode(encoding='utf-8'))
    c = re.compile(r'\w+')

    return c.findall(words)


def removable_words():
    return read_file('removable_words')


def common_base_form_verbs():
    return read_file('common_base_form_verbs')


def common_imp_verbs():
    return read_file('common_imp_verbs')


def common_special_plural_verbs():
    temp = read_file('common_special_plural_verbs')

    return dict(
        list((temp[i + 1], temp[i]) for i in range(0, len(temp), 2))
    )


CBF_ROOTS = common_base_form_verbs()
CIV_ROOTS = common_imp_verbs()
CSP = common_special_plural_verbs()
REMOVABLE_WORDS = removable_words()


def base_form_verb_detector(verb: str, roots: list):
    if len(verb) < 3:
        return None

    if verb in roots:
        return verb

    if verb[:2] == 'می':
        verb = verb[2:]

    if verb[0] == '\u200c':
        verb = verb[1:]

    for suffix in TYPES_SUFFIX[0] + TYPES_SUFFIX[1] + TYPES_SUFFIX[2]:
        temp_verb = verb
        if verb[-1 * len(suffix):] == suffix:
            temp_verb = verb[:-1 * len(suffix)]

        if f'{temp_verb}ن' in roots:
            return roots[roots.index(f'{temp_verb}ن')]

    return None


def imperative_verb_detector(verb: str, roots: list):
    if len(verb) < 3:
        return None

    if verb in roots:
        return verb

    if verb[:2] == 'می':
        verb = verb[2:]
    else:
        return None

    if verb[0] == '\u200c':
        verb = verb[1:]

    for suffix in TYPES_SUFFIX[1] + TYPES_SUFFIX[2] + TYPES_SUFFIX[3]:
        temp_verb = verb

        if verb[-1 * len(suffix):] == suffix:
            temp_verb = verb[:-1 * len(suffix)]

        if f'ب{temp_verb}' in roots:
            return roots[roots.index(f'ب{temp_verb}')]

    return None


def merge_keys(old: str, new: str, words_dict: dict):

    if words_dict.__contains__(new):
        words_dict[new] = merge_lists(words_dict[new], words_dict[old])
    else:
        words_dict[new] = words_dict[old]

    words_dict.pop(old, None)


def filter_verbs_in_dict(word: str, words_dict: dict):

    # common_base_form_verbs
    word_root = base_form_verb_detector(word, CBF_ROOTS)
    if word_root is not None and not word == word_root:
        merge_keys(word, word_root, words_dict)
        return word_root

    # common_imp_verbs
    word_root = imperative_verb_detector(word, CIV_ROOTS)
    if word_root is not None and not word == word_root:
        merge_keys(word, word_root, words_dict)
        return word_root

    return None


def filter_word_as_verb(word: str):
    # common_base_form_verbs
    word_root = base_form_verb_detector(word, CBF_ROOTS)
    if word_root is not None and not word == word_root:
        return word_root

    # common_imp_verbs
    word_root = imperative_verb_detector(word, CIV_ROOTS)
    if word_root is not None and not word == word_root:
        return word_root

    return None


def filter_dict_from_suffix(word: str, words_dict: dict):
    keys = list(words_dict.keys())
    keys.sort()

    for suf_func in SUFFIX_FUNCTIONS:
        root = suf_func(word, keys)
        if root is not None:
            merge_keys(word, root, words_dict)

            return root

    return None


def filter_word_from_suffix(word: str, words_list: list):

    for suf_func in SUFFIX_FUNCTIONS:
        root = suf_func(word, words_list)
        if root is not None:
            return root

    return None


def filter_dict_from_special_plural_verbs(word: str, words_dict: dict):
    if CSP.__contains__(word):
        merge_keys(word, CSP[word], words_dict)
        return CSP[word]

    return None


def filter_word_of_special_plural_verbs(word: str):
    if CSP.__contains__(word):
        return CSP[word]

    return None


def filter_word(key: str, words_list: list):
    print(key)
    new = replace_letters(key)
    if new is not None:
        key = new

    # removable word
    if key in REMOVABLE_WORDS:
        return None

    # common_special_plural_verbs
    word_root = filter_word_of_special_plural_verbs(key)
    if word_root is not None:
        return word_root

    # filter suffix
    word_root = filter_word_from_suffix(key, words_list)
    if word_root is not None:
        return word_root

    # filter verbs
    filter_word_as_verb(key)
    if word_root is not None:
        return word_root

    return key


def filter_dictionary(words_dict: dict):
    keys = list(words_dict.keys())

    for key in keys:

        new = replace_letters(key)
        if new is not None:
            merge_keys(key, new, words_dict)
            key = new

        # removable word
        if key in REMOVABLE_WORDS:
            words_dict.pop(key, None)
            continue

        # common_special_plural_verbs
        if filter_dict_from_special_plural_verbs(key, words_dict) is not None:
            continue

        # filter suffix
        if filter_dict_from_suffix(key, words_dict) is not None:
            continue

        # filter verbs
        filter_verbs_in_dict(key, words_dict)


if __name__ == '__main__':
    from search_engine import SearchEngine

    se = SearchEngine()
    li = se.show()
    for i in li:
        t = filter_word(i, li)
        print(i, t)
    # filter_word('آید', li)




