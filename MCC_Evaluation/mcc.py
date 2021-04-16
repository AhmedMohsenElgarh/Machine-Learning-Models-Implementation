# -*- coding: utf-8 -*-
"""MCC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cHE8VFoVIuCfRojRtrrowvgKPqKU-iAs
"""

import pandas as pd
import numpy as np


from sklearn.model_selection import train_test_split #for splitting data
from sklearn.preprocessing import OneHotEncoder # to handle categorical features
from sklearn.compose import ColumnTransformer #for the transormations of one hot encoders
from sklearn.pipeline import Pipeline # for the model pipeline

from sklearn.ensemble import RandomForestClassifier #tree-based classifier

from sklearn.metrics import f1_score, matthews_corrcoef, plot_confusion_matrix, classification_report

"""# Data

# Task

To predict the product sales based on the historical records.
"""

data = pd.read_csv("SalesKaggle3.csv")

data

data.info()

data['SoldFlag'].value_counts()

"""# Data Preprocessing

- We will remove all the unique identifiers like Order, SKU_number etc.

- We gonna use a tree-based model so no need to scale the data.
"""

def data_preparation(df):
  df = df.copy()

  #only using "Historical" records in File_Type column using query() function
  df = df.query("File_Type == 'Historical'")

  """drop unnecessary columns i.e Unique Identifiers and also File_Type as we only have Horizontal records.
  Remove SoldCount because it is a function for our target SoldFlag i.e we can't give hint to our model so better
  to remove it.
  """
  df = df.drop(["Order", "File_Type", "SKU_number", "SoldCount"], axis=1)

  #Split the data
  X = df.drop("SoldFlag", axis=1)
  y = df['SoldFlag']

  X_train, X_test, y_train, y_test = train_test_split(X,y, train_size=0.7, shuffle=True, random_state=1)

  return X_train, X_test, y_train, y_test

X_train, X_test, y_train, y_test = data_preparation(data)

print(len(X_train))
print(len(X_test))
print(len(y_train))
print(len(y_test))

X_train

y_test

"""# Build the Pipeline for Model Training

- One hot encoder for MarketType and ReleaseNumber.

- Pipeline for defining the steps
"""

def model_pipeline():
    binary_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(sparse=False, drop='if_binary'))
    ])
    
    nominal_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(sparse=False, handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(transformers=[
        ('binary', binary_transformer, ['MarketingType']),
        ('nominal', nominal_transformer, ['ReleaseNumber'])
    ], remainder='passthrough')
    
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=1))
    ])
    
    return model

!pip3 install -U scikit-learn

train_model = model_pipeline()
clf = train_model.fit(X_train, y_train)

"""## Evaluation"""

y_train_pred = clf.predict(X_train)
y_test_pred = clf.predict(X_test)

# Evaluation on the train set
print("Evaluation on training set \n")
print("--------------------------------------")
model_train_f1 = f1_score(y_train, y_train_pred, average='binary')
print("The f1-score for the training set is: ", np.round(model_train_f1*100), "%")
print("--------------------------------------")

model_train_score = clf.score(X_train, y_train)
print("Model score on the train set is: ", np.round(model_train_score*100), "%")
print("--------------------------------------")

model_train_mcc = matthews_corrcoef(y_train, y_train_pred)
print("Model MCC on the test set is: ", np.round(model_train_mcc*100), "%")

# Evaluation on the train set
print("Evaluation on the test set \n")
print("--------------------------------------")
model_test_f1 = f1_score(y_test, y_test_pred, average='binary')
print("The f1-score for the test set is: ", np.round(model_test_f1*100), "%")
print("--------------------------------------")

model_test_score = clf.score(X_test, y_test)
print("Model score on the test set is: ", np.round(model_test_score*100), "%")

print("--------------------------------------")

model_test_mcc = matthews_corrcoef(y_test, y_test_pred)
print("Model MCC on the test set is: ", np.round(model_test_mcc*100), "%")

plot_confusion_matrix(clf, X_test, y_test, labels=clf.classes_)

clr = classification_report(y_test, y_pred)
print(clr)

"""# Conclusion

### We can see that for target value "0", the model is doing good but for "1", it is failing to predict due to class imbalance.

- MCC and f1-score are better to evaluate models when there is a class imbalance in the data.

- MCC is one of the best evaluation metric for "Binary Classification problem"

#### The Matthews correlation coefficient (MCC), instead, is a more reliable statistical rate which produces a high score only if the prediction obtained good results in all of the four confusion matrix categories (true positives, false negatives, true negatives, and false positives), proportionally both to the size of positive elements and the size of negative elements in the dataset.

<a href="https://ibb.co/HDXNgF1"><img src="https://i.ibb.co/jvHV46B/4-Table2-1.png" alt="4-Table2-1" border="0"></a>

<a href="https://imgbb.com/"><img src="https://i.ibb.co/bBtvLG9/download.png" alt="download" border="0"></a>
"""