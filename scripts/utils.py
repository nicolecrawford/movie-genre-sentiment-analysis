def print_weights(model, feature_list):

    feature_weights = []
    for i in range(len(feature_list)):
        feature_weights.append((feature_list[i], model.coef_[0][i]))

    feature_weights.sort(key=lambda tup: tup[1], reverse=True)

    print "---weights, high to low"
    for w in feature_weights:
        print w[0] + " & " + "{:.4f}".format(w[1])


    feature_weights.sort(key=lambda tup: abs(tup[1]), reverse=True)
    print "---weights (absolute), high to low"
    for w in feature_weights:
        print w[0] + " & " + "{:.4f}".format(w[1])


def get_accuracy(y_pred,y_true):
    correct = 0
    for i in range(len(y_pred)):
        if y_pred[i] == y_true[i]:
            correct += 1
    return float(correct)/len(y_true)


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
