from vowpalwabbit import pyvw
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import spacy
import csv
import os
import re


def get_opinion_params(_opinion):
    _opinion = _opinion.lower()
    doc = nlp(_opinion)
    tokens = []
    for token in doc:
        tokens.append(token.lemma_)
    tokens = [token for token in tokens if not re.match(r'\W+', token)]
    tokens = list(dict.fromkeys(tokens))
    tokens = [token for token in tokens if token not in stop_words]
    return tokens


model = None
nlp = spacy.load("pl_core_news_lg")
star_opinion_datasets = ["book_stars.csv", "book_stars1.csv"]
stop_words_txt = open("polish_stopwords.txt", "r", encoding='utf-8')
stop_words = [line.rstrip() for line in stop_words_txt]
stop_words_txt.close()
if os.path.isfile("model.vwmodel"):
    model = pyvw.vw('--quiet -i model.vwmodel')
else:
    data = []
    for dataset in star_opinion_datasets:
        with open(dataset, newline='', encoding='utf-8') as book_stars:
            reader = csv.reader(book_stars, delimiter=',', quotechar='"')
            for star, opinion in reader:
                params = get_opinion_params(opinion)
                data.append(star + " | " + " ".join(params))
    train_data, test_data = train_test_split(data, train_size=0.9, test_size=0.1, shuffle=True)
    model = pyvw.vw('--quiet -c -f model.vwmodel')
    for elem in train_data:
        model.learn(elem)
    stars, predicts = [], []
    for elem in test_data:
        stars.append(int(elem.split(" | ")[0]))
        predicts.append(model.predict("| " + elem.split(" | ")[1]))
    model.finish()
    print("rmse: " + str(mean_squared_error(stars, predicts, squared=False)))
print("wpisz opinię o książce: ")
opinion = input()
print("")
params = get_opinion_params(opinion)
book_star = model.predict("| " + " ".join(params))
print("ilość gwiazdek: " + str(round((book_star / 2), 2)) + '/5')
