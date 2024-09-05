import random
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.feature_selection import RFECV
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd
import numpy as np


Data = pd.read_csv('CompiledHeadToHeadStatsDifference.csv')

y = Data['PointDiff'].to_numpy()
y_class = [1 if x>0 else -1 for x in y]
X = Data.drop(columns=['PointDiff']).to_numpy()


X_train, X_test, y_train, y_test = train_test_split(X, y_class)


X_train1, X_test1, y_train1, y_test1 = train_test_split(X, y)

poly_transformer = PolynomialFeatures(degree=2, interaction_only=True)
X_poly = poly_transformer.fit_transform(X_train, y_train)

feature_selector = RFECV(estimator=LogisticRegression(max_iter=1000000000))
feature_selector.fit_transform(X_poly, y_train)
#print(feature_selector.get_feature_names_out(Data.columns[:-1]))
lr = LogisticRegression(max_iter=100000000)
lr.fit(X_train, y_train)

linReg = LinearRegression()
linReg.fit(X_train1, y_train1)

lrcv = LogisticRegressionCV(max_iter=100000, cv=5)
lrcv.fit(X_train, y_train)

y_pred = lr.predict(X_test)
print('Logistic Regression Accuracy: '+str(np.sum(y_pred == y_test)/len(y_test)))
y_pred = lrcv.predict(X_test)
print('Logistic Regression CV Accuracy: '+str(np.sum(y_pred == y_test)/len(y_test)))
score = linReg.score(X_test, y_test)
print('Linear Regression R2: '+str(score))
y_pred = feature_selector.predict(X_test)
print('Logistic Regression with RFE: '+str(np.sum(y_pred == y_test)/len(y_test)))

testpoint = X_test[random.randint(0, 1000)]
arr = np.array(testpoint).reshape(1, -1)
print(lr.predict_proba(arr))
print(lr.predict(arr))
print(linReg.predict(arr))

