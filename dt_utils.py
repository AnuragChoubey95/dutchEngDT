#Title: LAB3
#Author: ac2255
#Instructor: Jansen Orfan

from string import punctuation

DUTCH = "nl"
ENGLISH = "en"

#ENTRY : SENTENCE; LABEL; HAS_FUNC_DUTCH_1 >= 2; WORDS ENDING WITH "EN" >= 2; HAS_FUNC_DUTCH_2 >= 2 ; HAS_FUNC_ENGLISH > 2; HAS_COMMON_ENGLISH > 2

FUNC_DUTCH_1 = ['aan', 'af', 'al', 'alle', 'alles', 'als', 'bij', 'daar', 'dan', 'dat', 'de', 'der', 'des', 'die',
    'dit', 'doch', 'doen', 'door', 'een', 'eens', 'en', 'er', 'geen', 'geweest', 'haar' 'heb',
    'hebben', 'heeft', 'hem', 'het', 'hier', 'hij', 'hoe', 'hun', 'ik', 'je', 'jij', 'jou',
    'jullie', 'kan', 'kon', 'kunnen', 'maar'] 

FUNC_DUTCH_2 = ['me', 'meer', 'men', 'met', 'mij', 'mijn', 'moet', 'na',
    'naar', 'niet', 'niets', 'nog', 'nu', 'om', 'ons', 'ook', 'op', 'over', 'reeds', 'te', 'tegen',
    'toch', 'toen', 'tot', 'uit', 'uw', 'van', 'veel', 'voor', 'want', 'waren', 'wat', 'we', 'wel',
    'werd', 'wezen', 'wie', 'wij', 'wil', 'worden', 'zal', 'ze', 'zei', 'zelf', 'zich', 'zij', 'zijn',
    'zo', 'zonder', 'zou']

FUNC_ENGLISH = ['a', 'and', 'the','about', 'above', 'across', 'after', 'against', 'along', 'among', 'around', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'but', 'by', 'concerning', 'considering', 'despite', 'down', 'during', 'except', 'for', 'from', 'inside', 'into', 'like', 'near', 'of', 'off', 'on', 'onto', 'out', 'outside', 'over', 'past', 'regarding', 'round', 'since', 'through', 'throughout', 'till', 'to', 'toward', 'under', 'underneath', 'until', 'unto', 'up', 'upon', 'with', 'within', 'without']

COMMON_ENGLISH = ['the', 'be', 'to', 'of', 'and', 'a', 'that', 'have', 'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'person', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us']


def parse_input(filename):
    sentence_list = []
    with open(filename) as file:
        for each in file.readlines():
            str_1 = each.strip()
            str_2 = "".join(char for char in str_1 if char not in punctuation)
            if len(str_2.split(" ")) > 0:
                sentence_list.append([str_2[2:], str_2[0:2], None, None, None, None, None])
    return sentence_list


# HAS_FUNC_DUTCH >= 2 , FEATURE 1
def has_func_dutch_1( sentence_list ) -> None:
    global FUNC_DUTCH_1
    for each in sentence_list:
        func_dutch_counter = 0
        for word in each[0].split(" "):
            if word in FUNC_DUTCH_1:
                func_dutch_counter += 1
        if func_dutch_counter >= 2:
            each[2] = True
        else:
            each[2] = False


# WORDS ENDING WITH "EN" >= 2 , FEATURE 2
def has_two_en( sentence_list ) -> None:
    for each in sentence_list:
        en_counter = 0
        for word in each[0].split(" "):
            if word.endswith("en"):
                en_counter += 1
        if en_counter >= 2:
            each[3] = True
        else:
            each[3] = False


# HAS_FUNC_DUTCH >= 2 , FEATURE 3
def has_func_dutch_2( sentence_list ) -> None:
    global FUNC_DUTCH_2
    for each in sentence_list:
        func_dutch_counter = 0
        for word in each[0].split(" "):
            if word in FUNC_DUTCH_2:
                func_dutch_counter += 1
        if func_dutch_counter >= 2:
            each[4] = True
        else:
            each[4] = False


# HAS_FUNC_ENGLISH >= 2, FEATURE 4
def has_func_english( sentence_list ):
    global FUNC_ENGLISH
    for each in sentence_list:
        func_english_counter = 0
        for word in each[0].split(" "):
            if word in FUNC_ENGLISH:
                func_english_counter += 1
        if func_english_counter >= 2:
            each[5] = True
        else:
            each[5] = False


# HAS_COMMON_ENGLISH >= 2, FEATURE 5
def has_common_english( sentence_list ):
    global COMMON_ENGLISH
    for each in sentence_list:
        common_english_counter = 0
        for word in each[0].split(" "):
            if word in COMMON_ENGLISH:
                common_english_counter += 1
        if common_english_counter >= 2:
            each[6] = True
        else:
            each[6] = False


def has_all_same( sentence_list ):
    initial = sentence_list[0][1]
    for each in sentence_list:
        if each[1] != initial:
            return False
    return True


def get_plurality( sentence_list ):
    ENGLISH_local = ENGLISH
    DUTCH_local = DUTCH
    en_count = 0
    nl_count = 0
    for s in sentence_list:
        lang = s[1]
        if lang == ENGLISH_local:
            en_count += 1
        elif lang == DUTCH_local:
            nl_count += 1
    ans = ENGLISH_local if en_count > nl_count else DUTCH_local
    return ans


def test(filename):
    sentence_list = parse_input(filename)
    has_func_dutch_1(sentence_list)
    has_two_en(sentence_list)
    has_func_dutch_2(sentence_list)
    has_func_english(sentence_list)
    has_common_english(sentence_list)

    return sentence_list