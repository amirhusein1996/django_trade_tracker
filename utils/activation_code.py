from django.utils.crypto import get_random_string
from random import randrange

def create_activation_code():
    # for more security , the lenght of activation code is choosen randomly between 128 and 178
    code_lenght : int = randrange(128 , 178)
    return get_random_string(length=code_lenght)
