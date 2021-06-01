import re

def isPasswordValide(password):
    r  = r"^(?=.*?[a-z])(?=.*?[0-9]).{8,}$"
    return re.match(r, password)


print(isPasswordValide('ase12378'))
