# -*- coding: utf-8 -*-
"""Testes_challenge_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WtE18zbJR3IszQLBgM1TStK25qwlLc4G
"""
import os

from persistence.repository import GenericRepository
from action.from_file_to_mongo import from_xlsx_to_mongo, from_csv_to_mongo
from utils.clean_key import clean_key

db_name = 'minsait_challenge'


def popula_credito_rural():
    # instancia um repositório mongodb
    repository = GenericRepository(db_name, 'credito_rural')

    folder_path = "./xlsx/credito_rural"

    file_list = os.listdir(folder_path)

    file_list.remove('__init__.py')

    for file_path in file_list:
        from_xlsx_to_mongo(folder_path, file_path, repository)


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
        'Producão_Brasil_Inverno',
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


# popula_credito_rural()
# popula_nova_collection()
# popula_sicor_operacao_basica_estado()
popula_conab()

#####################################

# import glob
# import numpy as np
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import pingouin as pg
# import random as rd
# from scipy import stats as st
# from sklearn.model_selection import train_test_split

# from utils.clean_key import clean_key
# from utils.clean_value import clean_value

# df_filtrado.shape

# df_filtrado.describe()

# df_filtrado.head(3)

# df_filtrado['Linha/Programa'].value_counts().to_frame()



# df_filtrado['Agente Financeiro'].value_counts().to_frame()

# df_filtrado['Tipo de Agricultura'].value_counts().to_frame()

# df_filtrado['Beneficiários'].value_counts().to_frame()

# df_filtrado['Estado'].value_counts().to_frame()

# df_filtrado['Região'].value_counts().to_frame()

# df_filtrado['Nº de Operações'].value_counts().to_frame()

# """## ESTATISTICAS EM RELAÇÃO À REGIÃO DO PAÍS:"""

# #calculo de moda dos valores aprovados por região:
# df_filtrado.groupby('Região')['Valor Aprovado R$'].apply(lambda x: x.mode().iloc[0]).to_frame().reset_index()

# #calculo de maximo, minimo e media dos valores aprovados por região:
# df_filtrado.groupby('Região').agg(min_idh = pd.NamedAgg('Valor Aprovado R$', 'min'),max_idh = pd.NamedAgg('Valor Aprovado R$', 'max'),media_idh = pd.NamedAgg('Valor Aprovado R$', 'mean')).reset_index()

# #calculo das medianas dos valores aprovados por região:
# df_filtrado.groupby('Região').agg(median_idh = pd.NamedAgg('Valor Aprovado R$', 'median')).reset_index()

# #calculo dos quartis dos valores aprovados por região:
# df_filtrado.groupby('Região')['Valor Aprovado R$'].apply(lambda x: x.quantile([0.25, 0.5, 0.75])).to_frame().reset_index().rename(columns={'level_1': 'quartil'})

# #calculo de variacia e desvio padrão dos valores aprovados por região:
# df_filtrado.groupby('Região').agg(variancia_idh = pd.NamedAgg('Valor Aprovado R$', 'var'),dp_idh = pd.NamedAgg('Valor Aprovado R$', 'std')).reset_index()

# """## ESTATISTICAS EM RELAÇÃO AO TIPO DE AGRICULTURA:"""

# #calculo de moda dos valores aprovados por tipo de agricultura:
# df_filtrado.groupby('Tipo de Agricultura')['Valor Aprovado R$'].apply(lambda x: x.mode().iloc[0]).to_frame().reset_index()

# #calculo de maximo, minimo e media dos valores aprovados por tipo de agricultura:
# df_filtrado.groupby('Tipo de Agricultura').agg(min_idh = pd.NamedAgg('Valor Aprovado R$', 'min'),max_idh = pd.NamedAgg('Valor Aprovado R$', 'max'),media_idh = pd.NamedAgg('Valor Aprovado R$', 'mean')).reset_index()

# #calculo das medianas dos valores aprovados por tipo de agricultura:
# df_filtrado.groupby('Tipo de Agricultura').agg(median_idh = pd.NamedAgg('Valor Aprovado R$', 'median')).reset_index()

# #calculo dos quartis dos valores aprovados por tipo de agricultura:
# df_filtrado.groupby('Tipo de Agricultura')['Valor Aprovado R$'].apply(lambda x: x.quantile([0.25, 0.5, 0.75])).to_frame().reset_index().rename(columns={'level_1': 'quartil'})

# #calculo de variacia e desvio padrão dos valores aprovados por tipo de agricultura:
# df_filtrado.groupby('Tipo de Agricultura').agg(variancia_idh = pd.NamedAgg('Valor Aprovado R$', 'var'),dp_idh = pd.NamedAgg('Valor Aprovado R$', 'std')).reset_index()

# """## ESTATISTICAS EM RELAÇÃO AO TIPO DE LINHA/PROGRAMA:"""

# #calculo de moda dos valores aprovados por tipo linha/programa:
# df_filtrado.groupby('Linha/Programa')['Valor Aprovado R$'].apply(lambda x: x.mode().iloc[0]).to_frame().reset_index()

# #calculo de maximo, minimo e media dos valores aprovados por tipo linha/programa:
# df_filtrado.groupby('Linha/Programa').agg(min_idh = pd.NamedAgg('Valor Aprovado R$', 'min'),max_idh = pd.NamedAgg('Valor Aprovado R$', 'max'),media_idh = pd.NamedAgg('Valor Aprovado R$', 'mean')).reset_index()

# #calculo das medianas dos valores aprovados por tipo linha/programa:
# df_filtrado.groupby('Linha/Programa').agg(median_idh = pd.NamedAgg('Valor Aprovado R$', 'median')).reset_index()

# #calculo de variacia e desvio padrão dos valores aprovados por tipo linha/programa:
# df_filtrado.groupby('Linha/Programa').agg(variancia_idh = pd.NamedAgg('Valor Aprovado R$', 'var'),dp_idh = pd.NamedAgg('Valor Aprovado R$', 'std')).reset_index()