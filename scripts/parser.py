from classes import Movie, Line, Character
import pickle
import re
from nltk.stem.porter import *


# might want to move this to model.py
def get_parsed_data():
    movie_map = parse_movie_title()
    parse_characters(movie_map)
    parse_lines(movie_map)
    return movie_map


# only run once
def get_unigrams():
    stemmer = PorterStemmer()
    vocab_counter = {}
    vocab = {}
    index = 0
    for line in open("cornell-movie-dialogs-corpus/movie_lines.txt"):
        cats = line.split(" +++$+++ ")
        content = re.findall(r"[\w']+|[.,!?;]", cats[4].lower())
        for w in content:
            word = stemmer.stem(w)
            if word in vocab_counter:
                vocab_counter[word] += 1
            else:
                vocab_counter[word] = 1
    for w in vocab_counter:
        if vocab_counter[w] > 0:
            vocab[w] = index
            index +=1
    # vocab['UNK'] = index
    pickle.dump(vocab, open("pickles/vocab.p", "wb"))


def get_bigrams():
    stemmer = PorterStemmer()
    vocab_counter = {}
    vocab = {}
    index = 0
    for line in open("cornell-movie-dialogs-corpus/movie_lines.txt"):
        cats = line.split(" +++$+++ ")
        content = re.findall(r"[\w']+|[.,!?;]", cats[4].lower())
        for i in range (1, len(content)):
            w2 = content[i]
            w1 = content[i-1]
            word1 = stemmer.stem(w1)
            word2 = stemmer.stem(w2)
            if (word1,word2) in vocab_counter:
                vocab_counter[(word1,word2)] += 1
            else:
                vocab_counter[(word1, word2)] = 1
    for pair in vocab_counter:
        if vocab_counter[pair] > 0:
            vocab[pair] = index
            index +=1
    # vocab['UNK'] = index
    pickle.dump(vocab, open("pickles/bigrams.p", "wb"))


def parse_movie_title():
    movie_map = {}
    for line in open("cornell-movie-dialogs-corpus/movie_titles_metadata.txt"):
        cats = line.split(" +++$+++ ")
        m_id = cats[0].strip().lower()
        title = cats[1].strip().lower()
        year = cats[2].strip().lower()
        rating = cats[3].strip().lower()
        num_votes = cats[4].strip().lower()

        # genre parsing
        genre_string = cats[5][2:-3]
        genres = set(genre_string.split("', '"))

        # add to movie map
        movie = Movie(m_id, title, year, rating, num_votes)
        movie.set_genres(genres)
        movie_map[m_id] = movie
    return movie_map


def parse_characters(movie_map):
    for line in open("cornell-movie-dialogs-corpus/movie_characters_metadata.txt"):
        cats = line.split(" +++$+++ ")
        character_id = cats[0].strip().lower()
        name = cats[1].strip().lower()
        m_id = cats[2].strip().lower()
        gender = cats[4].strip().lower()
        position = -1 if cats[5].strip() == '?' else int(cats[5].strip())
        char = Character(character_id, name, gender, position)
        movie_map[m_id].add_character(char)


def parse_lines(movie_map):
    prev_m_id = "m0"
    cur_movie_lines = []
    for line in open("cornell-movie-dialogs-corpus/movie_lines.txt"):
        cats = line.split(" +++$+++ ")
        line_num = int(cats[0].strip()[1:])
        character_id = cats[1]
        m_id = cats[2]
        content = cats[4]
        if m_id != prev_m_id:
            # sort based on line number
            cur_movie_lines.sort(key=lambda x: x.line_num)

            # add to movie_map
            movie_map[prev_m_id].set_lines(cur_movie_lines)

            # clear for next movie
            cur_movie_lines = []
            prev_m_id = m_id

        cur_movie_lines.append(Line(line_num, content, character_id))

#map of movie titles to their bechdel scores (0 = no info; -1 = not pass; 1 = pass)
def parse_bechdel():
    return pickle.load(open("pickles/bechdels.p", "rb"))

# get_unigrams()
get_bigrams()