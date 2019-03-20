import csv
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from MemeData import MemeData
from joblib import dump
import numpy
import copy
import pandas as pd


class AI:

    def __init__(self):
        self.clf = self.train_model()

    def train_model(self):
        meme_data = MemeData()
        #self.extract_primitive_list(meme_data.get_data())
        my_data = pd.read_csv('data.csv')
        bins = (-10, 25, 100,1000,10000,100000)
        group_names = ['bad', 'ok','good','awesome','top']
        my_data['upvotes'] = pd.cut(my_data['upvotes'], bins=bins, labels=group_names,include_lowest=True)
        print(my_data['upvotes'].unique())
        label_factor = LabelEncoder()
        my_data['upvotes'] = label_factor.fit_transform(my_data['upvotes'])
        X = my_data.drop('upvotes', axis=1)
        y = my_data['upvotes']
        clf = MLPClassifier(solver='adam', alpha=1e-500, max_iter=1000, hidden_layer_sizes=(11, 11, 11))
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)
        print(classification_report(y_test, preds))
        dump(clf, 'model.joblib')
        return clf

    def extract_primitive_list(self, data):
        for index, row in enumerate(data):
            row = self.extract_primitive_meme(row)
            for value in row.values():
                if value == 'null':
                    data.pop(index)
                    return self.extract_primitive_list(data)
        with open('data.csv', 'w') as f:  # Just use 'w' mode in 3.x
            w = csv.writer(f)
            w.writerow(data[0].keys())
            for i in data:
                w.writerow(i.values())

    def extract_primitive_meme(self, row):
        row.pop('flair', None)
        row.pop('factor', None)
        row.pop('time_stamp', None)
        row.pop('ratio', None)
        ftr = [3600, 60, 1]
        row['time'] = sum([a * b for a, b in zip(ftr, map(int, row['time'].split(':')))]) / (60 * 60)
        #row.pop('time', None)
        row.pop('id', None)
        row.pop('title', None)
        return row

    def predict(self, meme):
        meme = self.extract_primitive_meme(copy.copy(meme))
        row = []
        for value in meme.values():
            row.append(float(value))
        print(row)
        row = numpy.array(row).reshape(1, -1)
        prediction = self.clf.predict_proba(row)
        return prediction
