import pandas as pd

from persistence.repository import GenericRepository


def read_credito_rural(db_name: str = 'minsait_challenge', year: str = ''):
    repository = GenericRepository(db_name, 'credito_rural')
    filter = {}
    
    if year:
        year_pattern = ".*" + year + ".*"
        filter = {"mes_ano_protocolo": {"$regex": year_pattern}}

    print("count")
    print(repository.count_documents(filter))

    return pd.DataFrame(repository.list_all_documents(filter))
