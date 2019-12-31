import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model

data = pd.read_csv('nfl-games.csv')

# preprocessing
data = data[['PtsW', 'PtsL', 'YdsW', 'YdsL']]
predict = ['PtsW', 'PtsL']

# set up train/test data
X = np.array(data.drop(predict, 1))
Y = data[predict]
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.2)

linear = linear_model.LinearRegression()

linear.fit(x_train, y_train)
acc = linear.score(x_test, y_test)
print(acc)