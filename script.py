import lichess as li
import ml

def main():

    li.save_by_player(username="Lusthetics", max=1000, color='white')
    # ml.rfc(file='data/lusthetics.csv')

if __name__ == "__main__":
    main()