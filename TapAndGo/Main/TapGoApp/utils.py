import uuid

def get_random_code():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code

def get_random_code_card():
    code = str(uuid.uuid4())[:15].replace('-', '').lower()
    return code