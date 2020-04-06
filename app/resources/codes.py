import random

def get_codes_radom(count = 3):
    codes = list()
    for i in range(count):
        codes.append(str(random.randint(1000, 9999)))
    return codes