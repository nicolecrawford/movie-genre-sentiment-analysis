#for running all the models


from sklearn import svm
from sklearn.linear_model import LogisticRegression as lr
from sklearn.metrics import classification_report

import classes
import feature_extractor
import parser
import random
import pickle
from collections import Counter

test_dev = False
runSVM = False

# 0 = fail ; 1 = success
target_names = ["fail", "success"]

def test_on_dev(movie_dev, movie_map, bechdel_map,model,vocab,box_office, bigrams):
    X = []
    y_true = []
    count = 1
    for m_id in movie_dev:
        if box_office[m_id] != 0:
            print "dev movie", movie_map[m_id].title
            count += 1
            movie_features = feature_extractor.box_office_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
            X.append(movie_features)
            if box_office[m_id] == 1:
                y_true.append(target_names[1])
            else:
                y_true.append(target_names[0])
    print "dev count", count
    y_pred = model.predict(X)
    print(classification_report(y_true, y_pred, target_names=target_names))


def test_on_train(X, y_true, logistic):
    y_pred = logistic.predict(X)
    print(classification_report(y_true, y_pred, target_names=target_names))


def main():

    movie_map = parser.get_parsed_data()

    movie_train = pickle.load(open("pickles/movie_train.p", "rb"))
    movie_dev = pickle.load(open("pickles/movie_dev.p", "rb"))
    box_office = pickle.load(open("pickles/movie_success.p", "rb"))
    # movie_test = pickle.load(open("pickles/movie_test.p", "rb"))
    bechdel_map = pickle.load(open("pickles/bechdels.p", "rb"))
    vocab = pickle.load(open("pickles/vocab.p", "rb"))
    bigrams = pickle.load(open("pickles/bigrams.p", "rb"))

    count = 0
    # train and fit model
    X = []
    y_true = []
    for m_id in movie_train:
        if box_office[m_id] != 0:
            print "train movie", movie_map[m_id].title
            count +=1
            movie_features = feature_extractor.box_office_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
            X.append(movie_features)
            if box_office[m_id] == 1:
                y_true.append(target_names[1])
            else:
                y_true.append(target_names[0])

    model = lr()
    if runSVM:
        model = svm.SVC()
        model.fit(X, y_true)
    else:
        model = lr()
        model.fit(X, y_true)

    pickle.dump(model, open("pickles/model.p", "wb"))

    if test_dev:
        test_on_dev(movie_dev, movie_map, bechdel_map, model,vocab, box_office, bigrams)
    else:
        test_on_train(X, y_true, model)


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

