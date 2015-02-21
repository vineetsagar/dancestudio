import re

phone_re = re.compile(r'\d{10}$')
name_re=re.compile(r'^[A-Za-z ]*$')
spcl_char_re=re.compile(r"[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]")

def validate_name_field(name):
    if name_re.match(name):
        return True
    else:
        return False
    
def validate_phone_number(number):
    if phone_re.match(number):
        return True
    else:
        return False
    
def validate_address(addr):
    if spcl_char_re.match(addr):
        return False    #as spcl characters are not allowed
    else:
        return True        