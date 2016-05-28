#all methods for feature extraction

import classes
import parser

# 		- bigrams, unigrams (laplace smooth)
# 		- Average length of speech by a character
# 		- Ratio of personal pronouns in the text (require NLTK)
# 		- number of exclamation points
#       - GloVe (?)
#       - proportion of we words (who, where, why etc.)
# 		- Ratio of positive words: negative words (sentiment analysis)


def extract_all(movie, bechdel_map):
    X = list()
    X.append(num_characters_feat(movie))
    X.append(ratio_male_characters_feat(movie))
    X.append(ratio_female_characters_feat(movie))
    X.append(avg_line_length_feat(movie))
    X.append(tot_num_lines_feat(movie))
    X.append(pass_bechdel(movie, bechdel_map))
    X.append(two_female_leads(movie))
    X.append(main_character_gender(movie))

    return X


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