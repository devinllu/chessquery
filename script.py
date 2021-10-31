import berserk

API_TOKEN = "lip_bYPixWzHsRrAjtPMeUwP"

def main():
    session = berserk.TokenSession(API_TOKEN)
    client = berserk.Client(session=session)

    print(client.account.get())


if __name__ == "__main__":
    main()