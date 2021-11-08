import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def rfc(file):
    # Index(['id', 'rated', 'variant', 'speed', 'perf', 'createdAt', 'lastMoveAt',
    #    'status', 'players', 'winner', 'opening', 'moves', 'clock',
    #    'tournament'],
    #   dtype='object')
    df = pd.read_csv(file)
    y = df['winner']
    dropped = df.drop(['winner'], axis=1)
    x = dropped.loc[:, 'rated':'tournament']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    # need to encode strings to numeric values before training
    model = RandomForestClassifier().fit(x_train, y_train)

    print(model.score(x_test, y_test))
    

def main():
    pass

if __name__ == "__main__":
    main()