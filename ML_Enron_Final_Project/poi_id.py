#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.

import pandas as pd
import numpy as np

# converting dataset to dataframe for outlier analysis
df = pd.DataFrame.from_dict(data_dict, orient = 'index')

df = df.replace('NaN', np.nan)

# dropping outliers
df = df.drop('TOTAL')

# creating new features
df['salary_sqrt'] = np.sqrt(df.salary)
df['bonus_sqrt'] = np.sqrt(df.bonus)
df['total_payments_sqrt'] = np.sqrt(df.total_payments)
df['total_stock_value_sqrt'] = np.sqrt(df.total_stock_value)
df['salary_to_bonus_ratio'] = df.salary / df.bonus
df['msgs_sent_to_poi_ratio'] = df.from_this_person_to_poi / df.to_messages
df['msgs_received_from_poi_ratio'] = df.from_poi_to_this_person / df.from_messages

# List of all features, and the poi label
financial_features = ['salary', 'total_payments', 'bonus', 'total_stock_value', 
                      'expenses', 'exercised_stock_options', 'salary_to_bonus_ratio']
poi_label = ['poi']
features_list = poi_label + financial_features

# convert dataframe back into dict
df = df.replace(np.nan, 'NaN')
my_dataset = df[features_list].to_dict(orient = 'index')

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation
from sklearn import preprocessing
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

#from sklearn.naive_bayes import GaussianNB
#gnbc_clf = GaussianNB()
#test_classifier(gnbc_clf, my_dataset, features_list)

#from sklearn.ensemble import RandomForestClassifier
#rf_clf = RandomForestClassifier(n_estimators = 50, random_state = 202)
#test_classifier(rf_clf, my_dataset, features_list)

#from sklearn.cluster import KMeans
#km_clf = KMeans(n_clusters=2)
#test_classifier(km_clf, my_dataset, features_list)

from sklearn.ensemble import AdaBoostClassifier
ab_clf = AdaBoostClassifier(n_estimators = 60, random_state = 202)
test_classifier(ab_clf, my_dataset, features_list)

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

def TuneAdaBoostParams(n_estimators, learning_rate, rs):
    from sklearn.ensemble import AdaBoostClassifier
    for i in n_estimators:
        for j in learning_rate:
            print "\nn_estimators = ", i, ", learning_rate = ", j, "\n"
            ab_clf = AdaBoostClassifier(n_estimators = i, learning_rate = j, random_state = rs)
            test_classifier(ab_clf, my_dataset, features_list)

# limiting the values in the 2 lists for tester.py as they each take a while to run
n_estimators_list = [50, 60]
learning_rate_list = [0.7, 0.9]
TuneAdaBoostParams(n_estimators_list, learning_rate_list, 202)

# best performance
ab_clf = AdaBoostClassifier(n_estimators = 60, learning_rate = 0.99, random_state = 202)
test_classifier(ab_clf, my_dataset, features_list)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(ab_clf, my_dataset, features_list)
