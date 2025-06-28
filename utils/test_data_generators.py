from faker import Faker

fake = Faker()

def generate_email(length=None):
    if length is None:
        return fake.email()
    
    if length < 5:
        length = 5
    
    local_part_length = length - 3
    local_part = fake.pystr(min_chars=local_part_length, max_chars=local_part_length)
    domain_part = fake.pystr(min_chars=1, max_chars=1) + "." + fake.pystr(min_chars=1, max_chars=1)
    
    email = f"{local_part}@{domain_part}"
    
    return email

def generate_password(length=None):
    if length is None:
        return fake.password()
    
    return fake.password(length)

def generate_name(length=None):
    if length is None:
        return fake.user_name()
    
    return fake.user_name()[:length]

def generate_age():
    return fake.random_int(min=0, max=99)
