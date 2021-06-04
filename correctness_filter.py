import re
from search_engine import SearchEngine
from tools import merge_lists

TYPES_SUFFIX = [
        ['ه‌ام', 'ه‌ای', 'ه', 'ه‌ایم', 'ه‌اید', 'ه‌اند'],
        ['یم', 'ید', 'ند'],
        ['م', 'ی'],
        ['د', '']
]

SUFFIX_1 = [
    '‌ها',  # with half-space
    '‌های',  # with half-space
    '‌هایی',  # with half-space
    'ها',
    'های',
    'هایی'
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
    # 'شان'
]

SUFFIX_4 = [
    # 'شان',
    'یان',
    'ان',
]


def suffix_detector_1(txt: str):
    for c in SUFFIX_1:
        root = txt[:-1 * len(c)]
        if c in txt[-1 * len(c):]:
            return root

    return None


def suffix_detector_2(txt: str):
    for c in SUFFIX_2:
        root = txt[:-1 * len(c)]
        if c in txt[-1 * len(c):]:

            return root

    return None


def suffix_detector_3(txt: str):
    for c in SUFFIX_3:
        root = txt[:-1 * len(c)]
        if c in txt[-1 * len(c):]:

            return root

    return None


def suffix_detector_4(txt: str):
    for c in SUFFIX_4:
        root = txt[:-1 * len(c)]
        if c in txt[-1 * len(c):]:

            return root

    return None


def complex_words_detector(txt: str):
    if '\u200c' in txt:
        index = txt.index('\u200c')

        return txt[:index], txt[index+1:]

    return None


def read_file(file_name: str):

    with open(f'{file_name}', 'rb') as f:
        words = (f.read().decode(encoding='utf-8'))
    c = re.compile(r'\w+')

    return c.findall(words)


def remove_words():
    return read_file('removable_words')


def common_base_form_verbs():
    return read_file('common_base_form_verbs')


def common_imp_verbs():
    return read_file('common_imp_verbs')


def common_special_plural_verbs():
    temp = read_file('common_special_plural_verbs')

    return dict(
        list((temp[i+1], temp[i]) for i in range(0, len(temp), 2))
    )


def verb_creator_1(base_form_verbs: list) -> (list, dict):
    """
    it needs base form verbs. -> verbs_list, verbs_dict
    :param base_form_verbs:
    :return:
    """
    verbs_list = []
    verbs_dict = {}
    for word in base_form_verbs:
        for suffix in TYPES_SUFFIX[0] + TYPES_SUFFIX[1] + TYPES_SUFFIX[2]:
            verbs_list.append(f'{word[:-1]}{suffix}')
            verbs_dict[f'{word[:-1]}{suffix}'] = word

        verbs_list.append(word[:-1])
        verbs_dict[word[:-1]] = word

        prefix = ['می', 'می\u200c']
        for suffix in TYPES_SUFFIX[1] + TYPES_SUFFIX[2]:
            verbs_list.append(f'{prefix[0]}{word[:-1]}{suffix}')
            verbs_list.append(f'{prefix[1]}{word[:-1]}{suffix}')
            verbs_dict[f'{prefix[0]}{word[:-1]}{suffix}'] = suffix
            verbs_dict[f'{prefix[1]}{word[:-1]}{suffix}'] = suffix

        verbs_list.append(f'{prefix[0]}{word[:-1]}')
        verbs_list.append(f'{prefix[1]}{word[:-1]}')
        verbs_dict[f'{prefix[0]}{word[:-1]}'] = word
        verbs_dict[f'{prefix[1]}{word[:-1]}'] = word

    return verbs_list, verbs_dict


def verb_creator_2(imperative_verbs: list) -> (list, dict):
    """
    it needs imperative verbs. -> verbs_list ,verbs_dict
    :param imperative_verbs:
    :return:
    """
    verbs_list = []
    verbs_dict = {}
    third_person = ['د']
    for word in imperative_verbs:
        prefix = ['می', 'می\u200c']
        for suffix in TYPES_SUFFIX[1] + TYPES_SUFFIX[2] + third_person:
            verbs_list.append(f'{prefix[0]}{word[1:]}{suffix}')
            verbs_list.append(f'{prefix[1]}{word[1:]}{suffix}')
            verbs_dict[f'{prefix[0]}{word[1:]}{suffix}'] = word
            verbs_dict[f'{prefix[1]}{word[1:]}{suffix}'] = word

        # verbs_list.append(f'{word}')

    return verbs_list, verbs_dict


def filter_dictionary(words_dict: dict):

    cbf_list, cbf_dict = verb_creator_1(common_base_form_verbs())
    civ_list, civ_dict = verb_creator_2(common_imp_verbs())
    csp = common_special_plural_verbs()
    rw = remove_words()

    for key in words_dict.keys():
        if key.count('آ'):
            words_dict[key.replace('آ', 'ا')] = words_dict[key]
            words_dict.pop(key, None)

        # removable keys
        if key in rw:
            words_dict.pop(key, None)
            continue

        # common_special_plural_verbs
        if csp.__contains__(key):
            if words_dict.__contains__(csp[key]):
                words_dict[csp[key]] = merge_lists(words_dict[csp[key]], words_dict[key])
            else:
                words_dict[csp[key]] = words_dict[key]
            words_dict.pop(key, None)
            continue

        # common_base_form_verbs
        if cbf_dict.__contains__(key):
            if words_dict.__contains__(cbf_dict[key]):
                words_dict[cbf_dict[key]] = merge_lists(words_dict[cbf_dict[key]], words_dict[key])
            else:
                words_dict[cbf_dict[key]] = words_dict[key]
            words_dict.pop(key, None)
            continue

        # common_imp_verbs
        if civ_dict.__contains__(key):
            if words_dict.__contains__(civ_dict[key]):
                words_dict[civ_dict[key]] = merge_lists(words_dict[civ_dict[key]], words_dict[key])
            else:
                words_dict[civ_dict[key]] = words_dict[key]
            words_dict.pop(key, None)
            continue


if __name__ == '__main__':
    se = SearchEngine()
    # print(se.show())
    li = se.show()

    # print(common_base_form_verbs())
    # print(common_imp_verbs())
    # print(common_special_plural_verbs())
    # print(remove_words())
    print(verb_creator_1(common_base_form_verbs()))
    print(verb_creator_2(common_imp_verbs()))





