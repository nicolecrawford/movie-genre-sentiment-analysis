class Movie:
    def __init__(self, m_id, title, year, rating, num_votes):
        self.m_id = m_id
        self.title = title
        self.year = year
        self.rating = rating
        self.num_votes = num_votes
        self.genres = set()
        self.lines = []
        self.characters = set()

    def set_genres(self, genres):
        self.genres = genres

    def set_lines(self, lines):
        self.lines = lines

    def add_character(self, character):
        self.characters.add(character)

    def to_string(self):
        print "m_id: ", self.m_id
        print "title: ", self.title
        print "rating: ", self.rating
        print "genres: ", list(self.genres)


class Line:
    def __init__(self, line_num, content, character_id):
        self.line_num = line_num
        self.content = content
        self.character_id = character_id


class Character:
        def __init__(self, character_id, name, gender, position):
            self.character_id = character_id
            self.name = name
            self.gender = gender
            self.position = position
