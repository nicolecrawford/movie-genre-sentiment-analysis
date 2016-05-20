#for running all the models


from sklearn import svm
import classes
import feature_extractor
import parser
import random
import pickle

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


def main():

    movie_map = parser.get_parsed_data()

    movie_train = pickle.load(open("movie_train.p", "rb"))
    # movie_dev = pickle.load(open("movie_dev.p", "rb"))
    # movie_test = pickle.load(open("movie_test.p", "rb"))


    X = []
    y = []
    for m_id in movie_train:
        movie_features = feature_extractor.extract_all(movie_train[m_id]))
        for genre in movie_map[m_id].genres
            X.append(movie_features)
            y.append(genre)


def divide_corpus(movie_map):

    movie_list = list(movie_map.keys())
    random.shuffle(movie_list)

    movie_train = movie_list[0:395]
    movie_test = movie_list[395:519]
    movie_dev = movie_list[519:]

    pickle.dump(movie_train, open("movie_train.p", "wb"))
    pickle.dump(movie_dev, open("movie_dev.p", "wb"))
    pickle.dump(movie_test, open("movie_test.p", "wb"))


if __name__ == "__main__":
    main()
