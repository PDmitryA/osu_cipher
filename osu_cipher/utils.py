

def to_int(value, default=None):
    try:
        value = int(value)
    except:
        value = default
    return value