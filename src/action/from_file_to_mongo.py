import pandas as pd

from utils.clean_key import clean_key
from utils.clean_value import clean_value
from persistence.repository import GenericRepository

def from_file_to_mongo(folder_path: str, file_path: str, repository: GenericRepository):
    df = pd.read_excel(folder_path + '/' + file_path)

    num_rows_with_missing = (df.isna().sum(axis=1) > 0).sum()

    df = df.dropna()

    print("se livrando de", num_rows_with_missing, "linhas com valores faltantes (missings)")

    list_of_dicts = df.to_dict(orient='records')

    new_list_of_dicts = [{clean_key(key): clean_value(value) for key, value in item.items()} for item in list_of_dicts]

    repository.insert_many_documents(new_list_of_dicts)