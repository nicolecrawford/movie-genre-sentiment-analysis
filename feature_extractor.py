#all methods for feature extraction

import classes
import parser

# 		- bigrams, unigrams (laplace smooth)
# 		- Average length of speech by a character
# 		- Ratio of personal pronouns in the text (require NLTK)
# 		- number of exclamation points
# 		- Proportion of “We” words (who, where, why, etc.)
# 		- Mentions of locations (cities, countries) or organizations (FBI, KGB, etc.)
# 		- Ratio of positive words: negative words (sentiment analysis)


def num_characters_feat(movie):
    return len(movie.characters)


def num_male_characters_feat(movie):
    male = 0
    for char in movie.characters:
        if char.gender == "m":
            male += 1
    return male


def num_female_characters_feat(movie):
    female = 0
    for char in movie.characters:
        if char.gender == "f":
            female += 1
    return female


def avg_line_length_feat(movie):
    total_length = 0.0
    for line in movie.lines:
        total_length += len(line)

    return total_length/len(movie.lines)


def tot_num_lines_feat(movie):
    return len(movie.lines)



