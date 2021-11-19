import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def predict(file):
    # Index(['id', 'rated', 'variant', 'speed', 'perf', 'createdAt', 'lastMoveAt',
    #    'status', 'players', 'winner', 'opening', 'moves', 'clock',
    #    'tournament'],
    #   dtype='object')
    df = pd.read_csv(file)

    # dropped = df.drop(['winner'], axis=1)
    # x = dropped.loc[:, 'rated':'tournament']
    x = df[['moves', 'opening', 'clock', 'status']].copy()

    
    label_encoder = LabelEncoder()

    x['moves'] = label_encoder.fit_transform(x['moves'])
    x['opening'] = label_encoder.fit_transform(x['opening'])
    x['clock'] = label_encoder.fit_transform(x['clock'])
    x['status'] = label_encoder.fit_transform(x['status'])

    y = label_encoder.fit_transform(df['winner'])

    
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    # need to encode strings to numeric values before training
    rfc = make_pipeline(RandomForestClassifier())
    bayes = make_pipeline(GaussianNB())
    knn = make_pipeline(KNeighborsClassifier())

    models = [rfc, bayes, knn]
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