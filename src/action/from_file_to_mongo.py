import pandas as pd

from utils.clean_key import clean_key
from utils.clean_value import clean_value
from persistence.repository import GenericRepository

def from_xlsx_to_mongo(
        folder_path: str, 
        file_path: str, 
        repository: GenericRepository, 
        no_missings: bool = True, 
        sheet_name: str = '',
        field_to_add: dict = None,
        field_to_change: dict = None
    ):
    if sheet_name:
        df = pd.read_excel(folder_path + '/' + file_path, sheet_name=sheet_name)
    else:
        df = pd.read_excel(folder_path + '/' + file_path)

    if field_to_add:
        df = df.assign(**field_to_add)

    if no_missings:
        df = get_rid_of_missings(df)

    if 'Unnamed: 8' in df.columns:
        df = df.drop(columns=['Unnamed: 8'])

    list_of_dicts = df.to_dict(orient='records')

    new_list_of_dicts = [{clean_key(key): clean_value(value) for key, value in item.items()} for item in list_of_dicts]

    # print("sheet_name", sheet_name)
    # print(len(new_list_of_dicts))

    repository.insert_many_documents(new_list_of_dicts)
    
    if field_to_change:
        print("field_to_change", field_to_change)
        wrong = field_to_change['wrong']
        right = field_to_change['right']

        update_operation = {
            "$rename": {
                wrong: right
            }
        }

        repository.update_many({}, update_operation)

def from_csv_to_mongo(
        folder_path: str, 
        file_path: str, 
        repository: GenericRepository, 
        no_missings: bool = True,
        separator: str = ';'
    ):
    df_iterator = pd.read_csv(folder_path + '/' + file_path, sep=separator, encoding='utf8', chunksize=100000)

    for df in df_iterator:
        if no_missings:
            df = get_rid_of_missings(df)

        # print("after reading csv, df.shape is", df.shape)

        list_of_dicts = df.to_dict(orient='records')

        # print("after converting to dict, len(list_of_dicts) is", len(list_of_dicts))

        new_list_of_dicts = [{clean_key(key): clean_value(value) for key, value in item.items()} for item in list_of_dicts]

        print("after cleaning keys and values, len(new_list_of_dicts) is", len(new_list_of_dicts))

        repository.insert_many_documents(new_list_of_dicts)

def get_rid_of_missings(df: pd.DataFrame) -> pd.DataFrame:
    num_rows_with_missing = (df.isna().sum(axis=1) > 0).sum()

    df = df.dropna()

    print("se livrando de", num_rows_with_missing, "linhas com valores faltantes (missings)")

    return df