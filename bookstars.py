from vowpalwabbit import pyvw
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import csv
import os
import pickle

model = None
if os.path.isfile("model.vwmodel"):
    model = pyvw.vw('--quiet -i model.vwmodel')
else:
    data = []
    if os.path.isfile("bookstars.pkl"):
        book_stars_pkl = open("bookstars.pkl", "rb")
        data = pickle.load(book_stars_pkl)
        book_stars_pkl.close()
    else:
        with open("book_stars.csv", newline='', encoding='utf-8') as book_stars:
            reader = csv.reader(book_stars, delimiter=',', quotechar='"')
            for star, opinion in reader:
                data.append(star + " |" + opinion)
        with open("book_stars1.csv", newline='', encoding='utf-8') as book_stars:
            reader = csv.reader(book_stars, delimiter=',', quotechar='"')
            for star, opinion in reader:
                data.append(star + " |" + opinion)
    book_stars_pkl = open("bookstars.pkl", "wb")
    pickle.dump(data, book_stars_pkl)
    book_stars_pkl.close()
    train_data, test_data = train_test_split(data, train_size=0.4, test_size=0.1, shuffle=True)

    model = pyvw.vw('--quiet -c -f model.vwmodel')
    for elem in train_data:
        model.learn(elem)
    stars, predicts = [], []
    for elem in test_data:
        stars.append(int(elem.split(" | ")[0]))
        predicts.append(model.predict("| " + elem.split(" | ")[1]))
    model.finish()
    print("rmse: " + str(mean_squared_error(stars, predicts, squared=False)))
print("wpisz opinię o książce:")
opinion = input()
book_star = model.predict("| " + opinion)
print("ilość gwiazdek: " + str(round((book_star / 2), 2)) + '/5')
