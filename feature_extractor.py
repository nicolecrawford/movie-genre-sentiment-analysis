#all methods for feature extraction

import classes
import parser
import re
import nltk
from nltk.stem.porter import *

# 		- bigrams
#       - tfidf
# 		- number of exclamation points
# 		- Ratio of positive words: negative words (sentiment analysis)


def genre_extract_all(movie, bechdel_map, vocab):
    X = list()
    X.append(num_characters_feat(movie))
    X.append(ratio_male_characters_feat(movie))
    X.append(ratio_female_characters_feat(movie))
    X.append(avg_line_length_feat(movie))
    X.append(tot_num_lines_feat(movie))
    X.append(pass_bechdel(movie, bechdel_map))
    X.append(two_female_leads(movie))
    X.append(main_character_gender(movie))
    X.extend(unigrams(movie, vocab))
    X.append(pronoun_ratio(movie))
    X.append(exclamations(movie))
    X.append(questions(movie))
    return X


def rating_extract_all(movie, bechdel_map, vocab):
    X = list()
    X.append(num_characters_feat(movie))
    X.append(ratio_male_characters_feat(movie))
    X.append(ratio_female_characters_feat(movie))
    X.append(avg_line_length_feat(movie))
    X.append(tot_num_lines_feat(movie))
    X.append(pass_bechdel(movie, bechdel_map))
    X.append(two_female_leads(movie))
    X.append(main_character_gender(movie))
    X.extend(unigrams(movie, vocab))
    X.append(pronoun_ratio(movie))
    X.append(exclamations(movie))
    X.append(questions(movie))
    return X


def box_office_extract_all(movie, bechdel_map, vocab):
    X = list()
    X.append(num_characters_feat(movie))
    X.append(ratio_male_characters_feat(movie))
    X.append(ratio_female_characters_feat(movie))
    X.append(avg_line_length_feat(movie))
    X.append(tot_num_lines_feat(movie))
    X.append(pass_bechdel(movie, bechdel_map))
    X.append(two_female_leads(movie))
    X.append(main_character_gender(movie))
    X.extend(unigrams(movie, vocab))
    X.append(pronoun_ratio(movie))
    X.append(exclamations(movie))
    X.append(questions(movie))
    return X


def questions(movie):
    total_words = 0
    question = 0
    for line in movie.lines:
        words = re.findall(r"[\w']+|[.,!?;]", line.content.lower())
        total_words += len(words)
        for word in words:
            if word == '?':
                question += 1
    return float(question) / total_words


def exclamations(movie):
    total_words = 0
    exclamation = 0
    for line in movie.lines:
        words = re.findall(r"[\w']+|[.,!?;]", line.content.lower())
        total_words += len(words)
        for word in words:
            if word == '!':
                exclamation += 1
    return float(exclamation) / total_words


def pronoun_ratio(movie):
    total_words = 0
    pronouns = 0
    for line in movie.lines:
        words = re.findall(r"[\w']+|[.,!?;]", line.content.lower())
        total_words += len(words)
        tags = nltk.pos_tag(words)
        for (word,tag) in tags:
            if tag == 'PRP':
                pronouns += 1
    return float(pronouns)/total_words


def unigrams(movie, vocab):
    stemmer = PorterStemmer()
    unis = [0]*len(vocab)
    for line in movie.lines:
        words = re.findall(r"[\w']+|[.,!?;]", line.content.lower())
        for w in words:
            word = stemmer.stem(w)
            if word in vocab:
                unis[vocab[word]] += 1
    return unis


def main_character_gender(movie):
    leading_gender = 1
    smallest_position = 1000
    for char in movie.characters:
        if char.position != -1 and char.position < smallest_position:
            smallest_position = char.position
            if char.gender == "m":
                leading_gender = 1
            elif char.gender == "f":
                leading_gender = -1
            else:
                leading_gender = 0
    return leading_gender


def two_male_leads(movie):
    chars = list(movie.characters)
    chars.sort(key=lambda char: char.position)
    mod_chars = filter(lambda char: char.position !=-1, chars)
    if len(mod_chars) >= 2:
        if mod_chars[0].gender == "m" and mod_chars[1].gender == "m":
            return 1
    return 0


def two_female_leads(movie):
    chars = list(movie.characters)
    chars.sort(key=lambda char: char.position)
    mod_chars = filter(lambda char: char.position != -1, chars)

    if len(mod_chars) >= 2:
        if mod_chars[0].gender == "f" and mod_chars[1].gender == "f":
            return 1
    return 0


def pass_bechdel(movie, bechdel_map):
    return bechdel_map[movie.m_id]


def num_characters_feat(movie):
    return len(movie.characters)


def ratio_male_characters_feat(movie):
    male = 0
    for char in movie.characters:
        if char.gender == "m":
            male += 1
    return float(male)/len(movie.characters)


def ratio_female_characters_feat(movie):
    female = 0
    for char in movie.characters:
        if char.gender == "f":
            female += 1
    return float(female)/len(movie.characters)


def avg_line_length_feat(movie):
    total_length = 0.0
    for line in movie.lines:
        total_length += len(line.content)
    return float(total_length)/len(movie.lines)


def tot_num_lines_feat(movie):
    return len(movie.lines)