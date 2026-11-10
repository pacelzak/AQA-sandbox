from faker import Faker

fake = Faker()

class DataGenerator:
    def __init__(self):
        self.username = fake.bothify(text='user_########')
        self.email = fake.email()
        self.password = fake.password()
        self.display_name = fake.name()