# mine-your-own
IDE's
	- PyCharm

TRAIN/TEST/DEV SPLIT
395/124/98 = 617 total movies
	- split into sets before genre expansion

GENRE EXPANSION
	- every movie is put into the set for each genre it has

PARSING
	
		- class Movie (MOVIE_TITLES_META)
			- movieID (int)
			- movie title (string)
			- movie year (int)
		   	- IMDB rating (double)
			- no. IMDB votes (int)
	 		- genres (set)
	 		- sorted list of Lines (list)
	 		- set of Characters (set)
	 	- class Line (MOVIE_LINES)
			- character ID
			- text (string)
		- class Character (MOVIE_CHARACTERS_META)
			- characterID (int)
			- character name (string)
			- gender ("?" for unlabeled cases) (string)
			- position in credits ("?" for unlabeled cases) (int)


MILESTONES

TASK 1: GENRE PREDICTION
	- FEATURES
		- ratio of female to male characters (or actual numbers)
		- number of characters
		- average line lengths
		- bigrams, unigrams (laplace smooth)
		- Average length of speech by a character
		- Ratio of personal pronouns in the text (require NLTK)
		- number of exclamation points
		- Proportion of “We” words (who, where, why, etc.)
		- Mentions of locations (cities, countries) or organizations (FBI, KGB, etc.)
		- Ratio of positive words: negative words (sentiment analysis)
