import requests
import pandas as pd
import numpy as np

# ## 1. Definindo cabeçalho da requisição

url = 'https://www.fundsexplorer.com.br/ranking'
headers = {
    'User-Agent': 
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36'
        ' (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}


response = requests.get(url, headers=headers)
if response.status_code == 200:
    df = pd.read_html(response.content, encoding='utf-8')[0]



df.sort_values('Código do fundo', inplace=True)


df['Setor'].unique()




df.isna().sum()

categorical_columns = ['Código do fundo','Setor']

idx = df[df['Setor'].isna()].index
df.drop(idx, inplace=True)

df[categorical_columns].isna().sum()

df[categorical_columns] = df[categorical_columns].astype('category')


df.isna().sum()


col_floats = list(df.iloc[:,2:-1].columns)

df[col_floats] = df[col_floats].fillna(value=0)

df[col_floats]

df[col_floats].head()

df[col_floats] = df[col_floats].applymap(lambda x: str(x).replace('R$', '').replace('.0','').replace('.','').replace('%','').replace(',','.'))

df[col_floats] = df[col_floats].astype('float')

# - Dados de P/VPA tem atributos infinitos e está em uma escala diferente


## Check infinity values pandas
df[np.isinf(df[col_floats]).any(1)]


idx = df[np.isinf(df[col_floats]).any(1)].index
df.drop(idx, inplace=True)


df['P/VPA'] = df['P/VPA']/100


# ### Analisando a média por setor


indicadores = ['Código do fundo',
               'Setor', 
               'DY (12M) Acumulado', 
               'Vacância Física', 
               'Vacância Financeira', 
               'P/VPA', 
               'Quantidade Ativos', 
               'Liquidez Diária']


df_aux = df[indicadores]


#media_setor = df_aux.groupby('Setor').agg(['mean','std'])



#media_setor.loc['Residencial', ('DY (12M)Acumulado', 'mean')]

# ### Criando uma função com uma estratégia para oportunidades do mercado


def oportunidade_media_setor(df, setor='Shoppings', label_setor='Setor'):
    
    media_setor = df_aux.groupby('Setor').agg(['mean','std'])
    
    df_setor = df[df[label_setor].isin([setor])]
    
    filter_ = \
            (df_setor['Quantidade Ativos'] > 5) &\
            (df_setor['Liquidez Diária'] > 5000) &\
            (df_setor['P/VPA'] < 1) #&\
           # (df_setor['DY (12M) Acumulado'] > media_setor.loc[setor, ('DY (12M) Acumulado','mean')]) 
            
    print('média do setor Yield: {}'.format(media_setor.loc[setor, ('DY (12M) Acumulado','mean')]))
    print('média do setor p/VPA: {}'.format(media_setor.loc[setor, ('P/VPA','mean')]))
    print('média do setor Ativos: {}'.format(media_setor.loc[setor, ('Quantidade Ativos','mean')]))
    
    return df_setor[filter_]


#list(df['Setor'].unique())



setores_validos_analise = ['Shoppings', 'Logística']

for setor_valido in setores_validos_analise:
    print("########## {} ##########".format(setor_valido))
    oportunidade = oportunidade_media_setor(df_aux, setor=setor_valido)
    oportunidade.sort_values('DY (12M) Acumulado', ascending=False, inplace=True)
    print(oportunidade)
    print("#############################")










