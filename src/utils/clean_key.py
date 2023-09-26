
def clean_key(key: str):
    key = key.lower() \
        .replace(' ', '_') \
        .replace('/', '_') \
        .replace('ã', 'a') \
        .replace('á', 'a') \
        .replace('é', 'e') \
        .replace('í', 'i') \
        .replace('ó', 'o') \
        .replace('ú', 'u') \
        .replace('ê', 'e') \
        .replace('ô', 'o') \
        .replace('õ', 'o') \
        .replace('ü', 'u') \
        .replace('â', 'a') \
        .replace('à', 'a') \
        .replace('í', 'i') \
        .replace('ú', 'u') \
        .replace('ç', 'c') \
        .replace('(', '') \
        .replace(')', '') \
        .replace('º', '') \
        .replace('ª', '') \
        .replace('?', '') \
        .replace('!', '') \
        .replace(';', '') \
        .replace(':', '') \
        .replace(',', '') \
        .replace('.', '') \
        .replace(' ', '_') \
        .replace('__', '_')
    return key
