import string
import random


def generate_uid(count=24):
    characters = string.ascii_letters + string.digits + '-_'
    return ''.join(random.sample(characters, count))


