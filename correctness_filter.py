SUFFIX = [
    'تر',
    'ترین',
    'ها',
    'های',
    'هایی',
    'ات',
    'ان'
]

SUFFIX_H_S = [
    '‌تر',  # with half-space
    '‌ترین',  # with half-space
    '‌ها',  # with half-space
    '‌های',  # with half-space
    '‌هایی',  # with half-space
]
# c = re.compile(fr'.+(?={z})')
PREFIX = [
    'می',
    '‌می‌',  # with half-space
    'ب'
]


def find_suffix(txt: str):
    pass


def search():
    pass


def create_modify_verbs(txt: str):
    type_1 = ['م', 'ی', '', 'یم', 'ید', 'ند', 'د']
    type_2 = ['ه‌‌‌ام', 'ه‌‌‌ای', 'ه‌', 'ه‌‌‌ایم', 'ه‌‌‌اید', 'ه‌‌‌اند']
    words_list_1 = []
    for s in type_1+type_2:
        if txt[-1*len(s):] == s:

            if txt[:3] == 'می‌':    # it should be first
                base = txt[:-1*len(s)][3:]
            elif txt[:2] == 'می':
                base = txt[:-1*len(s)][2:]
            elif txt[0] == 'ب':
                base = txt[:-1*len(s)][1:]
            else:
                base = txt[:-1 * len(s)]

            for p in type_1 + type_2:
                words_list_1.append(f'{base}{p}')  # ماضی ساده
                words_list_1.append(f'{"می"}{base}{p}')  # ماضی استمراری
                words_list_1.append(f'{"می‌"}{base}{p}')  # ماضی استمراری با نیم فاصله
                words_list_1.append(f'{"ب"}{base}{p}')  # ماضی استمراری
            search()

    print(words_list_1)
    return list(set(words_list_1))



dict_common_words = {
    'verb': {
            'دارم': 'دارد',
            'داری': 'دارد',
            'دارد': 'دارد',
            'داریم': 'دارد',
            'دارید': 'دارد',
            'دارند': 'دارد',
            'داشتم': 'داشت',
            'داشتی': 'داشت',
            'داشت': 'داشت',
            'داشتیم': 'داشت',
            'داشتید': 'داشت',
            'داشتند': 'داشت',
            'خواهم': 'خواهد',
            'خواهی': 'خواهد',
            'خواهد': 'خواهد',
            'خواهیم': 'خواهد',
            'خواهید': 'خواهد',
            'خواهند': 'خواهد',
            'باشم': 'باشد',
            'باشی': 'باشد',
            'باشد': 'باشد',
            'باشیم': 'باشد',
            'باشید': 'باشد',
            'باشند': 'باشد',
            'بودم': 'بود',
            'بودی': 'بود',
            'بود': 'بود',
            'بودیم': 'بود',
            'بدوید': 'بود',
            'بودند': 'بود'
    }
}


def verb_detect(word: str):
    pass


if __name__ == '__main__':
    a = list(filter(lambda x: x in dict_common_words['verb'].keys(), create_modify_verbs('خواهد')))
    print(a)


