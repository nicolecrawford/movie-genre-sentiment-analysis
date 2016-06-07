#for running all the models


from sklearn import svm
from sklearn.metrics import classification_report

import classes
import feature_extractor
import parser
import random
import pickle
import collections
#
#
# clf = svm.SVC()
# clf.fit(X, y)
#
#
# X = [[0, 0], [1, 1]]
# y = [0, 1]
#
# clf.predict([[2., 2.]])
#

# genres
# comedy, family, music, animation, musical (0)
# action. adventure, war, western (1)
# thriller, horror, mystery, crime (2)
# sci-fi, fantasy (3)
# documentary, biography, history (4)
# drama, film-noir, romance, " " (5)


genre_map = {'': 5, 'family': 0, 'adventure': 1, 'fantasy': 3, 'biography': 4, 'crime': 2, 'romance': 5,
             'animation': 0, 'music': 0, 'comedy': 0, 'war': 1, 'sci-fi': 3, 'horror': 2, 'western': 1, 'thriller': 2,
             'mystery': 2, 'film-noir': 5, 'drama': 5, 'action': 1, 'documentary': 4, 'musical': 0, 'history': 4}

target_names = ['comedy', 'action', 'thriller', "sci-fi", "documentary", "drama"]

test_dev = False

def test_on_dev(movie_dev, movie_map, bechdel_map,clf,vocab, bigrams):
    X = []
    y_true = []
    for m_id in movie_dev:
        if (len(movie_map[m_id].genres) > 0):
            best_genre_map = collections.defaultdict(int)
            movie_features = feature_extractor.genre_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
            for genre in movie_map[m_id].genres:
                if genre in genre_map:
                    best_genre_map[genre_map[genre]] += 1
                    # spread_genre[genre_map[genre]] += 1
            X.append(movie_features)
            best_genre, count = max(best_genre_map.iteritems(), key=lambda x: x[1])
            y_true.append(best_genre)
    y_pred = clf.predict(X)

    print(classification_report(y_true, y_pred, target_names=target_names))


def test_on_train(X, y_true, clf,movie_map,movie_train):
    y_pred = clf.predict(X)
    print 'here'
    for i in range(len(y_pred)):
        if y_pred[i] != y_true[i]:
            print movie_map[movie_train[i]].title
            print 'actual',y_true[i]
            print 'predicted',y_pred[i]
    print(classification_report(y_true, y_pred, target_names=target_names))


def main():

    movie_map = pickle.load(open("pickles/movie_map.p", "rb"))

    movie_train = pickle.load(open("pickles/movie_train.p", "rb"))
    movie_dev = pickle.load(open("pickles/movie_dev.p", "rb"))
    # movie_test = pickle.load(open("pickles/movie_test.p", "rb"))
    bechdel_map = parser.parse_bechdel()
    vocab = pickle.load(open("pickles/vocab.p", "rb"))
    bigrams = pickle.load(open("pickles/bigrams.p", "rb"))

    # train and fit model
    X = []
    y_true = []
    # spread_genre = collections.defaultdict(int)
    for m_id in movie_train:
        if len(movie_map[m_id].genres) > 0:
            best_genre_map = collections.defaultdict(int)
            for genre in movie_map[m_id].genres:
                if genre in genre_map:
                    best_genre_map[genre_map[genre]] += 1
                    # spread_genre[genre_map[genre]] += 1
            if best_genre_map:
                best_genre, count = max(best_genre_map.iteritems(), key=lambda x: x[1])
                movie_features = feature_extractor.genre_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
                X.append(movie_features)
                y_true.append(best_genre)



    clf = svm.SVC()
    clf.fit(X, y_true)


    if test_dev:
        test_on_dev(movie_dev, movie_map, bechdel_map, clf, vocab, bigrams)
    else:
        test_on_train(X, y_true, clf,movie_map,movie_train)


#done once
def divide_corpus(movie_map):

    del movie_map["m616"]

    movie_list = list(movie_map.keys())
    random.shuffle(movie_list)

    movie_train = movie_list[0:395]
    movie_test = movie_list[395:519]
    movie_dev = movie_list[519:]

    pickle.dump(movie_train, open("pickles/movie_train.p", "wb"))
    pickle.dump(movie_dev, open("pickles/movie_dev.p", "wb"))
    pickle.dump(movie_test, open("pickles/movie_test.p", "wb"))


if __name__ == "__main__":
    main()

