import lichess as li
import ml

def main():

    li.saveLichessDataByPlayerToCSV(username="Lusthetics", max=1000, color='white')
    # ml.rfc(file='data/lusthetics.csv')

if __name__ == "__main__":
    main()