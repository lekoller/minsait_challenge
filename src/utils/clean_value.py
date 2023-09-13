# if the field is a string, trim it
def clean_value(value):
    if isinstance(value, str):
        return value.strip()
    return value