from classes import Movie, Line, Character



# might want to move this to model.py
def main():
    movie_map = parse_movie_title()
    parse_characters(movie_map)
    parse_lines(movie_map)

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

main()