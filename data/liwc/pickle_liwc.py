from nltk.stem.porter import *
import pickle


cat = {}
cat_words = set()
cat_stemmed = {}
cat_stemmed_words = set()
current_cat = ""
stemmer = PorterStemmer()
for line in open("./data/liwc/LIWC2007WordStat Folder/LIWC2007.cat"):
    if (line.count("\t") == 1):
        category = line.strip()
        cat[category] = set()
        cat_stemmed[category] = set()
        current_cat = line.strip()
    elif (line.count("\t") == 2):
        term = line.strip()

        term = term.replace("*", "")

        limit = term.find(" ");
        term = term[:limit].lower()

        # stemmed
        cat_stemmed[current_cat].add(stemmer.stem(term))
        cat_stemmed_words.add(stemmer.stem(term))

        # regular
        cat[current_cat].add(term)
        cat_words.add(term)


print cat_words

# regulr
pickle.dump(cat_words, open("pickles/liwc_not_stemmed_words.p", "wb"))
pickle.dump(cat, open("pickles/liwc_not_stemmed.p", "wb"))

# stemmed
pickle.dump(cat_stemmed_words, open("pickles/liwc_stemmed_words.p", "wb"))
pickle.dump(cat_stemmed, open("pickles/liwc_stemmed.p", "wb"))


keys_dict = {}
i = 0
cat_listed = []
for key in cat:
    cat_listed.append(key)
    keys_dict[key] = i
    i += 1

print cat_listed
pickle.dump(cat_listed, open("pickles/cat_listed.p", "wb"))
pickle.dump(keys_dict, open("pickles/liwc_cat_to_index.p", "wb"))

