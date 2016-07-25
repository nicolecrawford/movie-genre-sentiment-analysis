#for running all the models


from sklearn import svm
from sklearn.linear_model import LogisticRegression as lr
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

# bad=0;good=1
target_names = ['bad', 'good']

#FLAGS
test_dev = True
rumSVM = False


def get_accuracy(y_pred,y_true):
    correct = 0
    for i in range(len(y_pred)):
        if y_pred[i] == y_true[i]:
            correct += 1
    return float(correct)/len(y_true)


def test_on_test(movie_test, movie_map, bechdel_map,model,vocab, bigrams):
    X = []
    y_true = []
    pos = 0
    neg = 0
    for m_id in movie_test:
        rate = float(movie_map[m_id].rating)
        if rate <= 5:
            neg +=1
            movie_features = feature_extractor.rating_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
            X.append(movie_features)
            y_true.append(0)
        elif rate >= 7.5:
            pos += 1
            movie_features = feature_extractor.rating_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
            X.append(movie_features)
            y_true.append(1)
    y_pred = model.predict(X)
    print "pos",pos
    print "neg",neg

    print(classification_report(y_true, y_pred, target_names=target_names))
    print "Accuracy: ", str(get_accuracy(y_pred,y_true))

def test_on_dev(movie_dev, movie_map, bechdel_map,model,vocab, bigrams):
    X = []
    y_true = []
    pos = 0
    neg = 0
    for m_id in movie_dev:
        rate = float(movie_map[m_id].rating)
        if rate <= 5:
            neg +=1
            movie_features = feature_extractor.rating_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
            X.append(movie_features)
            y_true.append(0)
        elif rate >= 7.5:
            pos += 1
            movie_features = feature_extractor.rating_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
            X.append(movie_features)
            y_true.append(1)
    y_pred = model.predict(X)
    for i in range(len(y_pred)):
        if y_pred[i] != y_true[i]:
            print movie_map[movie_dev[i]].title
            print 'actual',y_true[i]
            print 'predicted',y_pred[i]
    print "pos",pos
    print "neg",neg

    print(classification_report(y_true, y_pred, target_names=target_names))
    print "Accuracy: ", str(get_accuracy(y_pred,y_true))


def test_on_train(X, y_true, model):
    y_pred = model.predict(X)

    print(classification_report(y_true, y_pred, target_names=target_names))
    print "Accuracy: ", str(get_accuracy(y_pred, y_true))

def main():

    # movie_map = parser.get_parsed_data()
    movie_map = pickle.load(open("pickles/movie_map.p", "rb"))
    movie_train = pickle.load(open("pickles/movie_train.p", "rb"))
    movie_dev = pickle.load(open("pickles/movie_dev.p", "rb"))
    movie_test = pickle.load(open("pickles/movie_test.p", "rb"))
    bechdel_map = parser.parse_bechdel()
    vocab = pickle.load(open("pickles/vocab.p", "rb"))
    # bigrams = pickle.load(open("pickles/bigrams.p", "rb"))
    bigrams = []

    # rating_distribution = collections.defaultdict(int)
    # for m_id in movie_train:
    #     rate = float(movie_map[m_id].rating)
    #     if rate <= 6.5:
    #         rating_distribution["0:6.5"] += 1
    #     else:
    #         rating_distribution["6.5:10"] += 1
    # print rating_distribution

    # train and fit model
    X = []
    y_true = []
    pos = 0
    neg =0
    for m_id in movie_train:
        # movie_features = feature_extractor.rating_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
        # X.append(movie_features)
        rate = float(movie_map[m_id].rating)
        if rate <= 5:
            movie_features = feature_extractor.rating_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
            X.append(movie_features)
            y_true.append(0)
            neg+=1
        elif rate >= 7.5:
            movie_features = feature_extractor.rating_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
            X.append(movie_features)
            y_true.append(1)
            pos+=1
    print "pos", pos
    print "neg", neg
    model = lr()
    if rumSVM:
        model = svm.SVC()
        model.fit(X, y_true)
    else:
        model = lr()
        model.fit(X, y_true)

    pickle.dump(model, open("pickles/model.p", "wb"))

    if test_dev:
        test_on_dev(movie_dev, movie_map, bechdel_map, model, vocab, bigrams)
    else:
        test_on_train(X, y_true, model)
    test_on_test(movie_test, movie_map, bechdel_map, model, vocab, bigrams)
    # print "weights:", model.coef_


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
