import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def predict(file):
    # Index(['id', 'rated', 'variant', 'speed', 'perf', 'createdAt', 'lastMoveAt',
    #    'status', 'players', 'winner', 'opening', 'moves', 'clock',
    #    'tournament'],
    #   dtype='object')
    df = pd.read_csv(file)
    df = df[df['event'] == 2]

    # dropped = df.drop(['winner'], axis=1)
    # x = dropped.loc[:, 'rated':'tournament']
    x = df[['blackelo', 'whiteelo', 'eco']].copy()

    
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
    lst = []
    for k, v in enumerate(models):
        v.fit(x_train, y_train)
        lst.append(v.score(x_test, y_test))

    for i in lst:
        print(f"Score: {i}")
    

def main():
    pass

if __name__ == "__main__":
    main()