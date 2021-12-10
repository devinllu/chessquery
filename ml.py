import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, LabelBinarizer, OneHotEncoder
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint

def predict(file):
    # Index(['id', 'rated', 'variant', 'speed', 'perf', 'createdAt', 'lastMoveAt',
    #    'status', 'players', 'winner', 'opening', 'moves', 'clock',
    #    'tournament'],
    #   dtype='object')
    # event,site,white,black,result,utcdate,utctime,whiteelo,blackelo,whiteratingdiff,blackratingdiff,eco,opening,timecontrol,termination,moves_played,played_f3,castled,rating_difference,rating_average
    df = pd.read_csv(file)
    df = df[df['event'] == 2]

    # dropped = df.drop(['winner'], axis=1)
    # x = dropped.loc[:, 'rated':'tournament']
    x = df.drop('')

    
    label_encoder = LabelEncoder()

    x['eco'] = label_encoder.fit_transform(x['eco'])
    x['blackelo'] = label_encoder.fit_transform(x['blackelo'])
    x['whiteelo'] = label_encoder.fit_transform(x['whiteelo'])
    # x['status'] = label_encoder.fit_transform(x['status'])

    y = label_encoder.fit_transform(df['result'])

    
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    # need to encode strings to numeric values before training
    rfc = make_pipeline(RandomForestClassifier())
    bayes = make_pipeline(GaussianNB())
    knn = make_pipeline(KNeighborsClassifier())
    mlp = make_pipeline(MLPClassifier(activation='logistic', solver='adam'))

    models = [rfc, bayes, knn, mlp]
    names = ["Random Forest Classifier", "Naive Bayes", "KNN", "MLP"]
    lst = []
    for k, v in enumerate(models):
        v.fit(x_train, y_train)
        lst.append(v.score(x_test, y_test))

    for i, j in zip(lst, names):
        print(f"{j}: {i}")

def predict_castled(file):
    df = pd.read_csv(file)

    df = df[df['castled'] == 1]
    
    # note: selecting only the important features actually increases score substantially for KNN
    x = df.drop(['site', 'result', 'utcdate', 'utctime'], axis=1)
    # x = df.filter(['whiteratingdiff', 'blackratingdiff', 'rating_average', 'rating_difference', 'blackelo', 'whiteelo'], axis=1)
    y = df['result']

    for col in x.columns:
        x[col] = LabelEncoder().fit_transform(x[col])

    train_models(x, y)

def predict_f3(file):

    df = pd.read_csv(file)

    df = df[df['played_f3'] == 1]
    
    # x = df.drop(['site', 'result', 'utcdate', 'utctime'], axis=1)
    x = df.filter(['whiteratingdiff', 'blackratingdiff', 'rating_average', 'rating_difference', 'blackelo', 'whiteelo'], axis=1)
    y = df['result']

    # for col in x.columns:
    #     x[col] = LabelEncoder().fit_transform(x[col])

    train_models(x, y)

def train_models(x, y):
    pprint(x)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    rfc = make_pipeline(RandomForestClassifier())
    bayes = make_pipeline(GaussianNB())
    knn = make_pipeline(KNeighborsClassifier())
    mlp = make_pipeline(MLPClassifier(activation='logistic', solver='adam'))

    models = [rfc, bayes, knn, mlp]
    names = ["Random Forest Classifier", "Naive Bayes", "KNN", "MLP"]
    lst = []
    for k, v in enumerate(models):
        v.fit(x_train, y_train)
        lst.append(v.score(x_test, y_test))

    for i, j in zip(lst, names):
        print(f"{j}: {i}")

def measure_attributes(file):
    df = pd.read_csv(file)
    df = df.drop('site', axis=1)

    x = df.drop('result', axis=1)
    x = x.drop('utcdate', axis=1)
    cols = x.columns

    # note: one hot encoding causes increased dimensionality in feature_importances
    ohe = OneHotEncoder()
    lbe = LabelEncoder()
    y_encoder = LabelBinarizer()

    pprint(x)
    for col in x.columns:
        x[col] = lbe.fit_transform(x[col])
    y = df['result']

    pprint(x)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    model = RandomForestClassifier().fit(x_train, y_train)
    print(f"Gradient Boosting Score: {model.score(x_test, y_test)}")
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
    plt.title('Feature Importances')
    plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    plt.yticks(range(len(indices)), [features[i] for i in indices])
    plt.xlabel('Relative Importance')
    plt.ylabel('Features')
    plt.savefig('feat_importance.png')
    plt.show()
    

def show_vertical(features, importances, indices):
    plt.title('Feature Importances')
    plt.bar(range(len(indices)), importances[indices], color='b')
    plt.xticks(range(len(indices)), [features[i] for i in indices], rotation=45)
    plt.xlabel('Features')
    plt.ylabel('Relative Importance')
    plt.show()
    # plt.savefig('graph.png')
    

def main():
    # measure_attributes("data/lichess-std-big.csv")
    predict_f3("data/lichess-std-big.csv")

if __name__ == "__main__":
    main()