import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from pprint import pprint

def predict(file):
    df = pd.read_csv(file)
    
    x = df.filter(['blackelo', 'whiteelo', 'eco', 'timecontrol'], axis=1)
    y = df['result']

    x['eco'] = LabelEncoder().fit_transform(x['eco'])
    x['timecontrol'] = LabelEncoder().fit_transform(x['timecontrol'])
    print(x.dtypes)

    # train_models(x, y)

def train_models(x, y):
    pprint(x)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    # for i in range(500, 1000, 100):
    #     rfc = RandomForestClassifier(n_estimators=i, random_state=42).fit(x_train, y_train)
    #     pprint(f'Score for {i} is: {rfc.score(x_test, y_test)}')

    rfc = make_pipeline(RandomForestClassifier())
    bayes = make_pipeline(GaussianNB())
    mlp = make_pipeline(MLPClassifier())

    models = [rfc, bayes, mlp]
    
    names = ["Random Forest Classifier", "Naive Bayes", "MLP"]
    lst = []
    for k, v in enumerate(models):
        v.fit(x_train, y_train)
        lst.append(v.score(x_test, y_test))

    for i, j in zip(lst, names):
        print(f"{j}: {i}")

def measure_attributes(file):
    df = pd.read_csv(file, nrows=100000)
    df = df.drop('site', axis=1)
    df = df[df['event'] == 2]
    x = df.drop(['result', 'event', 'whiteratingdiff', 'blackratingdiff'], axis=1)    

    # note: one hot encoding causes increased dimensionality in feature_importances
    lbe = LabelEncoder()
    

    for col in x.columns:
        print(col)
        x[col] = lbe.fit_transform(x[col])
    y = df['result']

    

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    model = RandomForestClassifier().fit(x_train, y_train)
    print(f"Random Forest Score: {model.score(x_test, y_test)}")
    print(f"Feature Importances: {model.feature_importances_}")
    print(f"Length: {len(model.feature_importances_)}")

    features = x.columns
    importances = model.feature_importances_
    indices = np.argsort(importances)

    show_horizontal(features, importances, indices)

    # features = ['event',"white","black","utcdate","utctime","whiteelo","blackelo","whiteratingdiff","blackratingdiff","eco","opening","timecontrol","termination","moves_played","played_f3","castled","rating_difference","rating_average"]
    # importances = pd.Series(model.feature_importances_, index=cols)
    # importances.nlargest(10).plot(kind='barv')

def show_horizontal(features, importances, indices):
    figure(num=None, figsize=(11, 7), dpi=80, facecolor='w', edgecolor='k')
    plt.title('Feature Importances')
    plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    plt.yticks(range(len(indices)), [features[i] for i in indices])
    plt.xlabel('Relative Importance')
    plt.ylabel('Features')
    # plt.savefig('feat_importance.png')
    plt.show()
    

def main():
    predict("data/lichess-2021-10.csv")

if __name__ == "__main__":
    main()