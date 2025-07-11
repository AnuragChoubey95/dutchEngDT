#Title: LAB3
#Author: ac2255
#Instructor: Jansen Orfan

import pickle
from copy import deepcopy
from random import uniform
from bisect import bisect_right
from sys import argv
from math import log2, log, e, pow
from dtNode import dtNode
from dt_utils import *

script, filename, outfile, learn_type = argv

TRAINING = learn_type

features = [2,3,4,5,6]

def calculate_entropy(sentence_list):
    nl_count, en_count , total= 0, 0, len(sentence_list)
    for each in sentence_list:
        if each[1] == DUTCH:
            nl_count += 1
        elif each[1] == ENGLISH:
            en_count += 1
    expression_nl , expression_en = None, None
    try:
        expression_nl = ((float(nl_count)/total) * log2(float(nl_count)/total))
    except Exception:
        expression_nl = 0
    try:
        expression_en = ((float(en_count)/total) * log2(float(en_count)/total))
    except Exception:
        expression_en = 0

    entropy =  expression_nl + expression_en 
    entropy *= -1

    return entropy 


def calulate_info_gain(sentence_list, feature_num):
    arr_true = [x for x in sentence_list if x[feature_num] is True]
    arr_false = [x for x in sentence_list if x[feature_num] is False]

    info_gain = calculate_entropy(sentence_list) - ((float(len(arr_true))/len(sentence_list)) * calculate_entropy(arr_true)) - ((float(len(arr_false))/len(sentence_list)) * calculate_entropy(arr_false))

    return info_gain


def get_max_info_gain(sentence_list, features):

    gain_list = []
    for each in features:
        gain_list.append((calulate_info_gain(sentence_list, each), each))

    max_info_gain = max(gain_list, key=lambda x:x[0])
    return max_info_gain
    

def build_tree(sentence_list, features, parent_list):
    # if examples is empty then return PLURALITY-VALUE (parent examples)
    if len(sentence_list) == 0 or sentence_list is None:
        return dtNode(get_plurality(parent_list), None, None)
    
    # else if all examples have the same classification then return the classification
    if has_all_same(sentence_list):
        return dtNode(sentence_list[0][1], None, None)
    
    # else if attributes is empty then return PLURALITY-VALUE (examples)
    if len(features) == 0 or features is None:
        return dtNode(get_plurality(sentence_list), None, None) 
    
    root = dtNode(None, None, None)

    root.value = get_max_info_gain(sentence_list, features)[1]
    # print(root.value)
    arr_true = [x for x in sentence_list if x[root.value] is True]
    arr_false = [x for x in sentence_list if x[root.value] is False]

    features.remove(root.value)
    print(features)
    #left is for when condition is True
    root.left = build_tree(arr_true, features, sentence_list)
    #right is for when condition is False
    root.right = build_tree(arr_false, features, sentence_list)

    return root


def build_stump(sentence_list, feature, parent_list):
        return build_tree(sentence_list, [feature], parent_list)


def build_once(sentence_list):
    stump_feature = get_max_info_gain(sentence_list, features)[1]
    stump = build_stump(sentence_list, stump_feature, sentence_list)
    return stump


def get_weighted_error(stump, training_data, weights):
    error = 0 
    for each in training_data:
        if isinstance(stump.value, int):
            if each[stump.value]:
                if each[1] != stump.left.value:
                    error += weights[training_data.index(each)]
            if not(each[stump.value]):
                if each[1] != stump.right.value:
                    error += weights[training_data.index(each)]
    return error


def update_weights(stump, training_data, weights, alpha):
    for each in training_data:
        if each[stump.value]:
            if each[1] != stump.left.value: #error
                weights[training_data.index(each)] *= pow(e, alpha)
            else:
                weights[training_data.index(each)] *= pow(e, -1 * alpha)
        if not(each[stump.value]):
            if each[1] != stump.right.value: #error
                weights[training_data.index(each)] *= pow(e, alpha)
            else:
                weights[training_data.index(each)] *= pow(e, -1 * alpha)
    return weights


def normalize_weights(weights):
    sum_weights = sum(weights)

    for i in range(len(weights)):
        weights[i] /= sum_weights

    return weights


def get_refined_data(training_data, cumulative_weights):
    new_data = []

    for i in range(len(training_data)):
        token = round(uniform(0.0001, 0.9999), 3)
        position = bisect_right(cumulative_weights, token)
        if position > 99:
            position = 99
        try:
            new_data.append(training_data[position])
        except IndexError:
            print(position)

    return new_data


def train_ada(sentence_list, iterations):
    training_data = deepcopy(sentence_list)
    stump_list = []
    weights = [float(1)/len(sentence_list) for _ in range(len(sentence_list))]
    alphas = []

    for this in range(iterations):
        this_stump = build_once(training_data)
        this_error = get_weighted_error(this_stump, training_data, weights)
        if this_error == 0:
            break
        try:
            this_alpha = 0.5 * log(float(1 - this_error) / this_error)
        except:
            print(this_error)

        alphas.append(this_alpha)
        weights = update_weights(this_stump, training_data, weights, this_alpha)
        weights = normalize_weights(weights)
        for i in weights:
            print(i)
        stump_list.append(this_stump)

        cumulative_weights = [sum(weights[:i+1]) for i in range(len(weights))]
        training_data = get_refined_data(training_data, cumulative_weights)
    return stump_list, alphas


def write_out(filename, outfile):
    sentence_list = test(filename)

    if TRAINING == "dt":
        tree = build_tree(sentence_list,features,sentence_list) 
        with open(outfile, 'wb') as file:
            # Serialize the object and write it to the file
            pickle.dump(tree, file)
    elif TRAINING == "ada":
        tree = train_ada(sentence_list, 5)
        with open(outfile, 'wb') as file:
            # Serialize the object and write it to the file
            pickle.dump(tree, file)

  
def main():
    write_out(filename, outfile)


if __name__ == "__main__":
    main()