import berserk

API_TOKEN = "lip_bYPixWzHsRrAjtPMeUwP"

def main():
    session = berserk.TokenSession(API_TOKEN)
    client = berserk.Client(session=session)


    # lst = ['Sasageyo', 'Voinikonis_Nikita', 'Zugzwangerz', 'DOES-NOT-EXIST']

    print(client.users.get_public_data('DrDrunkenstein'))


if __name__ == "__main__":
    main()