#for running all the box_office models 

from sklearn import svm
from sklearn.linear_model import LogisticRegression as lr
from sklearn.metrics import classification_report

import classes
import feature_extractor
import parser
import utils
import random
import pickle
from collections import Counter


test_train = True
test_dev = True
test_test = False
runSVM = False

# 0 = fail ; 1 = success
target_names = ["fail", "success"]


def test_on_test(movie_test, movie_map, bechdel_map,model,vocab,box_office, bigrams):
    print "-------test_on_TEST-------"
    X = []
    y_true = []
    count = 1
    flops = 0
    hits = 0
    for m_id in movie_test:
        if m_id in box_office:
            if box_office[m_id] != 0:
                # print "test movie", movie_map[m_id].title
                count += 1

                if box_office[m_id] == 1:
                    hits += 1
                    y_true.append(target_names[1])
                    movie_features = feature_extractor.box_office_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
                    X.append(movie_features)
                    
                elif box_office[m_id] == -1:
                    flops += 1
                    y_true.append(target_names[0])
                    movie_features = feature_extractor.box_office_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
                    X.append(movie_features)

    
    print "test count", count
    print "test count: flops", flops
    print "test count: hits", hits

    y_pred = model.predict(X)
    print(classification_report(y_true, y_pred, target_names=target_names))
    print "Accuracy: ", str(utils.get_accuracy(y_pred, y_true))


def test_on_dev(movie_dev, movie_map, bechdel_map,model,vocab,box_office, bigrams):
    print "-------test_on_dev-------"
    X = []
    y_true = []
    count = 1
    hits = 0
    flops = 0
    for m_id in movie_dev:
        if box_office[m_id] != 0:
            # print "dev movie", movie_map[m_id].title
            count += 1
            if box_office[m_id] == 1:
                hits += 1
                y_true.append(target_names[1])
                movie_features = feature_extractor.box_office_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
                X.append(movie_features)
            elif box_office[m_id] == -1:
                flops += 1
                y_true.append(target_names[0])
                movie_features = feature_extractor.box_office_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
                X.append(movie_features)

    print "dev count", count
    print "dev count: flops", flops
    print "dev count: hits", hits

    y_pred = model.predict(X)
    # for i in range(len(y_pred)):
        # if y_pred[i] != y_true[i]:
            # print movie_map[movie_dev[i]].title
            # print 'actual',y_true[i]
            # print 'predicted',y_pred[i]
    print(classification_report(y_true, y_pred, target_names=target_names))
    print "Accuracy: ", str(utils.get_accuracy(y_pred, y_true))


def test_on_train(X, y_true, model,movie_map,movie_train):
    print "-------test_on_train-------"
    y_pred = model.predict(X)
    # for i in range(len(y_pred)):
        # if y_pred[i] != y_true[i]:
            # print movie_map[movie_train[i]].title
            # print 'actual',y_true[i]
            # print 'predicted',y_pred[i]
    print(classification_report(y_true, y_pred, target_names=target_names))
    print "Accuracy: ", str(utils.get_accuracy(y_pred, y_true))

def print_configs():
    print "test_train", test_train
    print "test_dev", test_dev
    print "test_test", test_test
    print "runSVM", runSVM

def main():

    print_configs()
    
    # movie_map = parser.get_parsed_data()
    movie_map = pickle.load(open("pickles/movie_map.p", "rb"))
    movie_train = pickle.load(open("pickles/movie_train.p", "rb"))
    movie_dev = pickle.load(open("pickles/movie_dev.p", "rb"))
    box_office = pickle.load(open("pickles/movie_success_point_five.p", "rb"))
    movie_test = pickle.load(open("pickles/movie_test.p", "rb"))
    bechdel_map = pickle.load(open("pickles/bechdels.p", "rb"))
    vocab = pickle.load(open("pickles/vocab.p", "rb"))
    # bigrams = pickle.load(open("pickles/bigrams.p", "rb"))
    bigrams = []

    print feature_extractor.get_feature_list(vocab)

    # train and fit model
    X = []
    y_true = []
    train_count = 0
    hits = 0
    flops = 0
    for m_id in movie_train:
        if box_office[m_id] != 0:
            # print "train movie:", movie_map[m_id].title
            train_count += 1
            if box_office[m_id] == 1:
                hits += 1
                y_true.append(target_names[1])
                movie_features = feature_extractor.box_office_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
                X.append(movie_features)
            elif box_office[m_id] == -1:
                flops += 1
                y_true.append(target_names[0])
                movie_features = feature_extractor.box_office_extract_all(movie_map[m_id], bechdel_map, vocab, bigrams)
                X.append(movie_features)
    
    print "train count", train_count
    print "hits", hits
    print "flops", flops

    if runSVM:
        model = svm.SVC()
    else:
        model = lr()

    model.fit(X, y_true)

    pickle.dump(model, open("pickles/model.p", "wb"))


    if test_train:
        test_on_train(X, y_true, model,movie_map,movie_train)
    if test_dev:
        test_on_dev(movie_dev, movie_map, bechdel_map, model,vocab, box_office, bigrams)
    if test_test:
        test_on_test(movie_test, movie_map, bechdel_map, model,vocab, box_office, bigrams)

    if not runSVM:
        utils.print_weights(model, feature_extractor.get_feature_list(vocab))



if __name__ == "__main__":
    main()

