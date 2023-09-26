# -*- coding: utf-8 -*-
"""Testes_challenge_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WtE18zbJR3IszQLBgM1TStK25qwlLc4G
"""
import os
import argparse
import pandas as pd

from persistence.repository import GenericRepository
from action.from_file_to_mongo import from_xlsx_to_mongo, from_csv_to_mongo
from action.from_mongo_to_pd import read_conab_safras_por_estado, read_credito_rural
from utils.clean_key import clean_key
from utils.constants import estados_brasileiros

db_name = 'minsait_challenge'

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--save',  action='store_true', help='save data to mongodb')
parser.add_argument('-l', '--load',  action='store_true', help='load data from mongodb and perform analysis')

args = parser.parse_args()


def popula_credito_rural():
    # instancia um repositório mongodb
    repository = GenericRepository(db_name, 'credito_rural')

    folder_path = "./xlsx/credito_rural"

    file_list = os.listdir(folder_path)

    file_list.remove('__init__.py')

    for file_path in file_list:
        from_xlsx_to_mongo(folder_path, file_path, repository, field_to_change={
            'wrong': 'mes_ano_aprovacao', 
            'right': 'mes_ano_protocolo'
        })
        


# Matheus, trabalhe nesta funcão com o nome que você quiser atribuir a esta nova fonte de dados
def popula_nova_collection():
    collection_name = 'seguro_rural_gov' # atribua o nome da nova collection aqui e cria uma pasta ao lado da nova pasta 'credito_rural' com o mesmo nome, dentro da pasta xlsx

    repository = GenericRepository(db_name, collection_name)

    folder_path = "./xlsx/" + collection_name

    file_list = os.listdir(folder_path)

    file_list.remove('__init__.py')

    for file_path in file_list:
        from_xlsx_to_mongo(folder_path, file_path, repository, no_missings=False) # se quiser manter os missings, deixe o parametro no_missings=False

def popula_sicor_operacao_basica_estado():
    collection_name = 'sicor_operacao_basica_estado'

    repository = GenericRepository(db_name, collection_name)

    folder_path = "./csv/" + collection_name

    file_list = os.listdir(folder_path)

    file_list.remove('__init__.py')

    for file_path in file_list:
        from_csv_to_mongo(folder_path, file_path, repository, no_missings=False, separator=';')

def popula_conab(): 
    dir_name = 'conab_safras'
    sheets = [
        'Área_Brasil', 
        'Área_Brasil_Inverno', 
        'Produtividade_Brasil',
        'Produtividade_Brasil_Inverno',
        'Produção_Brasil',
        'Produção_Brasil_Inverno',
        'Total_UF',
        'Total_Produto',
        'Total_Produto_Inverno',
    ]
    collection_sufix_names = [clean_key(sheet) for sheet in sheets]

    repositories = {
        collection_sufix_name: GenericRepository(db_name, dir_name + "_" + collection_sufix_name) 
        for collection_sufix_name in collection_sufix_names
    }

    for sheet, collection_sufix_name in zip(sheets, collection_sufix_names):
        folder_path = "./xlsx/" + dir_name
        file_list = os.listdir(folder_path)

        file_list.remove('__init__.py')
        
        repository = repositories[collection_sufix_name]

        for file_name in file_list:
            year = file_name.strip('.xlsx')

            from_xlsx_to_mongo(folder_path, file_name, repository, no_missings=False, sheet_name=sheet, field_to_add={'ano': year})


def analisar_credito_por_estado():
    print("analisando crédito por estado")
    
    df = read_credito_rural()

    df['estado'] = df['estado'].apply(clean_key)

    df['valor_comprometido_r$'].fillna(0, inplace=True)
    df['valor_aprovado_r$'].fillna(0, inplace=True)

    df['valor'] = df['valor_comprometido_r$'] + df['valor_aprovado_r$']
    
    filtered_df = df[df['tipo_de_agricultura'] == 'Agricultura Familiar']
    filtered_agg = filtered_df.groupby('estado').agg({'valor': 'sum'}).reset_index()
    list_filtered_agg = filtered_agg.to_dict('records')

    agg = df.groupby('estado').agg({'valor': 'sum', 'n_de_operacoes': 'sum'}).reset_index()

    list_agg = agg.to_dict('records')

    for item in list_agg:

        for filtered_item in list_filtered_agg:
            if item['estado'] == filtered_item['estado']:
                item['valor_agricultura_familiar'] = filtered_item['valor']
                item['porcentagem_agricultura_familiar'] = (item['valor_agricultura_familiar'] / item['valor']) * 100
                break
            item['valor_agricultura_familiar'] = 0
            item['porcentagem_agricultura_familiar'] = 0

    if args.save:
        repository = GenericRepository(db_name, 'credito_por_estado')

        repository.insert_many_documents([item for item in list_agg if item['estado'] != 'interestadual'])

def analisar_safra_por_estado():
    df = read_conab_safras_por_estado()

    df['variacao_produtividade'] = df['produtividade_em_kg_ha_var_%_d_c']

    agg = df.groupby('regiao_uf').agg({'variacao_produtividade': 'sum', }).reset_index()

    agg_list = agg.to_dict('records')

    for item in agg_list:
        item['estado'] = estados_brasileiros[item['regiao_uf']] if item['regiao_uf'] in estados_brasileiros else ""

    final_list = [item for item in agg_list if item['estado'] != ""]    

    if args.save:
        repository = GenericRepository(db_name, 'variacao_da_produtividade_por_estado')
    
        repository.insert_many_documents(final_list)


if args.save:
    # popula_credito_rural()
    # popula_nova_collection()
    # popula_sicor_operacao_basica_estado()
    # popula_conab()
    pass

if args.load:
    analisar_credito_por_estado()
    # analisar_safra_por_estado()
    pass
