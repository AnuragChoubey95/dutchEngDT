#Title: LAB3
#Author: ac2255
#Instructor: Jansen Orfan

import pickle
from sys import argv
from string import punctuation
from dt_utils import FUNC_DUTCH_1
from dt_utils import FUNC_DUTCH_2
from dt_utils import FUNC_ENGLISH
from dt_utils import COMMON_ENGLISH
from dt_utils import has_func_dutch_1
from dt_utils import has_func_dutch_2
from dt_utils import has_func_english
from dt_utils import has_common_english
from dt_utils import has_two_en

DUTCH = "nl"
ENGLISH = "en"
DUTCH_VALUE = -1
ENGLISH_VALUE = 1

script, model, filename = argv

def parse_input_again():
    sentence_list = []
    with open(filename) as file:
        for each in file.readlines():
            str_1 = each.strip()
            str_2 = "".join(char for char in str_1 if char not in punctuation)
            if len(str_2.split(" ")) == 15:
                sentence_list.append([str_2, None, None, None, None, None, None])
    return sentence_list


def traverse(sentence, tree_node):
    if tree_node.value == "nl":
        return "nl"
    if tree_node.value == "en":
        return "en"
    if sentence[tree_node.value]:
        return traverse(sentence, tree_node.left)
    else:
        return traverse(sentence, tree_node.right)
    

def check_ada(alphas, stumps, sentence_list):
    for i in range(len(sentence_list)):
        sum = 0
        for j in range(len(stumps)):
            decision = traverse(sentence_list[i], stumps[j])
            decision_num = ENGLISH_VALUE if decision == ENGLISH else DUTCH_VALUE
            sum += alphas[j] * decision_num
        if sum > 0:
            print(ENGLISH)
        else:
            print(DUTCH)


def predict():
    sentence_list = parse_input_again()
    has_func_dutch_1(sentence_list)
    has_two_en(sentence_list)
    has_func_dutch_2(sentence_list)
    has_func_english(sentence_list)
    has_common_english(sentence_list)

    with open(model, 'rb') as f:
        tree = pickle.load(f)

        if not(isinstance(tree,tuple)):
            for each in sentence_list:
                print(traverse(each, tree))
        else:
            print(tree)
            check_ada(tree[1], tree[0], sentence_list)


def main():
    predict()


if __name__ == "__main__":
    main()
