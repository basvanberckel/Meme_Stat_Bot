import csv
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from MemeData import MemeData
from numpy import genfromtxt
from joblib import dump, load
import numpy
import copy


class AI:

    def __init__(self):
        #self.train_model()
        self.clf = load('model.joblib')

    def train_model(self):
        meme_data = MemeData()
        data = self.extract_primitive_list(meme_data.get_data())
        labels = self.extract_labels(data)
        self.write_dict_to_csv('data.csv', data)
        my_data = genfromtxt('data.csv', delimiter=',')
        clf = MLPClassifier(solver='lbfgs', alpha=1e-5, max_iter=1000)
        X_train, X_test, y_train, y_test = train_test_split(my_data, labels, test_size=0.33, random_state=42)
        clf.fit(X_train, y_train)
        print(clf.score(X_test, y_test))
        dump(clf, 'model.joblib')
        return clf

    def extract_primitive_list(self, data):
        for index, row in enumerate(data):
            row = self.extract_primitive_meme(row)
            for value in row.values():
                if value == 'null':
                    data.pop(index)
                    return self.extract_primitive_list(data)
        return data

    def extract_primitive_meme(self, row):
        row.pop('flair', None)
        row.pop('upvotes', None)
        row.pop('time_stamp', None)
        row.pop('investements', None)
        ftr = [3600, 60, 1]

        row['time'] = sum([a * b for a, b in zip(ftr, map(int, row['time'].split(':')))]) / (60 * 60)
        row.pop('id', None)
        row.pop('title', None)
        return row

    def extract_labels(self, data):
        labels = []
        for index, row in enumerate(data):
            factor = row.pop('factor', None)
            if factor < 1:
                labels.append([1, 0, 0])
            elif factor < 2:
                labels.append([0, 1, 0])
            else:
                labels.append([0, 0, 1])
        with open('labels.csv', 'w') as f:  # Just use 'w' mode in 3.x
            w = csv.writer(f)
            for i in labels:
                w.writerow(i)
        return genfromtxt('labels.csv', delimiter=',')

    def write_dict_to_csv(self, name, list):
        with open(name, 'w') as f:  # Just use 'w' mode in 3.x
            w = csv.writer(f)
            # w.writerow(list[0].keys())
            for i in list:
                w.writerow(i.values())

    def predict(self, meme):
        meme = self.extract_primitive_meme(copy.copy(meme))
        row = []
        for value in meme.values():
            row.append(float(value))
        row = numpy.array(row).reshape(1, -1)
        prediction = self.clf.predict_proba(row)
        return prediction
