#all methods for feature extraction

import classes
import parser
import re
import nltk
from nltk.stem.porter import *
from nltk.corpus import opinion_lexicon
import collections

# 		- bigrams
#       - tfidf
# 		- number of exclamation points
# 		- Ratio of positive words: negative words (sentiment analysis)

genre_map = {'': 5, 'family': 0, 'adventure': 1, 'fantasy': 3, 'biography': 4, 'crime': 2, 'romance': 5,
             'animation': 0, 'music': 0, 'comedy': 0, 'war': 1, 'sci-fi': 3, 'horror': 2, 'western': 1, 'thriller': 2,
             'mystery': 2, 'film-noir': 5, 'drama': 5, 'action': 1, 'documentary': 4, 'musical': 0, 'history': 4}

target_names = ['comedy', 'action', 'thriller', "sci-fi", "documentary", "drama"]



def genre_extract_all(movie, bechdel_map, vocab, bigrams):
    X = list()
    X.append(num_characters_feat(movie))
    X.append(ratio_male_characters_feat(movie))
    X.append(ratio_female_characters_feat(movie))
    X.append(avg_line_length_feat(movie))
    X.append(tot_num_lines_feat(movie))
    X.append(pass_bechdel(movie, bechdel_map))
    X.append(two_female_leads(movie))
    X.append(main_character_gender(movie))
    X.append(movie_vocab_size(movie))
    # X.extend(unigrams(movie, vocab))
    X.append(pronoun_ratio(movie))
    X.append(exclamations(movie))
    X.append(questions(movie))
    # X.append(sentiment(movie))
    return X


def rating_extract_all(movie, bechdel_map, vocab, bigrams):
    X = list()
    # X.append(0) #baseline
    X.append(num_characters_feat(movie))
    X.append(ratio_male_characters_feat(movie))
    X.append(ratio_female_characters_feat(movie))
    X.append(avg_line_length_feat(movie))
    X.append(tot_num_lines_feat(movie))
    X.append(pass_bechdel(movie, bechdel_map))
    X.append(two_female_leads(movie))
    X.append(main_character_gender(movie))
    X.append(movie_vocab_size(movie))
    # X.extend(unigrams(movie, vocab))
    # X.extend(get_bigrams(movie,bigrams))
    # X.append(sentiment(movie))
    X.append(pronoun_ratio(movie))
    X.append(exclamations(movie))
    X.append(questions(movie))
    X.extend(genre_features(movie))
    return X


def box_office_extract_all(movie, bechdel_map, vocab,bigrams):
    X = list()
    # X.append(0) #baseline
    X.append(num_characters_feat(movie))
    X.append(ratio_male_characters_feat(movie))
    X.append(ratio_female_characters_feat(movie))
    X.append(avg_line_length_feat(movie))
    X.append(tot_num_lines_feat(movie))
    X.append(pass_bechdel(movie, bechdel_map))
    X.append(two_female_leads(movie))
    X.append(main_character_gender(movie))
    X.append(movie_vocab_size(movie))
    # X.extend(unigrams(movie, vocab))
    # X.append(sentiment(movie))
    X.append(pronoun_ratio(movie))
    X.append(exclamations(movie))
    X.append(questions(movie))
    X.extend(genre_features(movie))
    return X


# positive = 1; negative = 0
def sentiment(movie):
    stemmer = PorterStemmer()
    pos_count = 0
    neg_count = 0
    for line in movie.lines:
        words = re.findall(r"[\w']+|[.,!?;]", line.content.lower())
        for w in words:
            word = stemmer.stem(w)
            if word in set(opinion_lexicon.negative()):
                neg_count += 1
            elif word in set(opinion_lexicon.negative()):
                pos_count += 1
    if pos_count > neg_count:
        return 1
    else:
        return 0


def genre_features(movie):
    to_return = [0]*len(target_names)
    best_genre_map = collections.defaultdict(int)
    for genre in movie.genres:
        if genre in genre_map:
            best_genre_map[genre_map[genre]] += 1
    best_genre, count = max(best_genre_map.iteritems(), key=lambda x: x[1])
    to_return[best_genre] = 1
    return to_return


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
    norm = [float(i) / sum(unis) for i in unis] #normalize to sum to 1.0
    return norm

def get_bigrams(movie, bigrams):
    stemmer = PorterStemmer()
    bis = [0]*len(bigrams)
    for line in movie.lines:
        words = re.findall(r"[\w']+|[.,!?;]", line.content.lower())
        for j in range (1,len(words)):
            w1 = words[j-1]
            w2 = words[j]
            word1 = stemmer.stem(w1)
            word2 = stemmer.stem(w2)
            if (word1,word2) in bigrams:
                bis[bigrams[word1,word2]] += 1
    norm = [float(i) / sum(bis) for i in bis] #normalize to sum to 1.0
    return norm


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

def movie_vocab_size(movie):
    stemmer = PorterStemmer()
    vocab = set()
    for line in movie.lines:
        words = re.findall(r"[\w']+|[.,!?;]", line.content.lower())
        for w in words:
            word = stemmer.stem(w)
            vocab.add(word)
    return len(vocab)
