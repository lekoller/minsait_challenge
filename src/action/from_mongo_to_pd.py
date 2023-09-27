import pandas as pd

from persistence.repository import GenericRepository


def read_credito_rural(db_name: str = 'minsait_challenge', year: str = ''):
    repository = GenericRepository(db_name, 'credito_rural')
    filter = {}
    
    if year:
        year_pattern = ".*" + year + ".*"
        filter = {"mes_ano_protocolo": {"$regex": year_pattern}}

    return pd.DataFrame(repository.list_all_documents(filter))

def read_conab_safras_por_estado(db_name: str = 'minsait_challenge', year: str = ''):
    repository = GenericRepository(db_name, 'conab_safras_total_uf')

    filter = {}
    
    if year:
        filter = {"ano": {"$regex": year}}

    return pd.DataFrame(repository.list_all_documents(filter))