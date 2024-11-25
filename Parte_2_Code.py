# %% [markdown]
# # PARTE 2 - TRABALHO 

# %% [markdown]
# ### Importação Bibliotecas

# %%
import pandas as pd
from unidecode import unidecode
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler

# %% [markdown]
# ### Lendo dataset limpo e dataset de renda por bairros

# %%

df = pd.read_csv('../PÓS/2024-04-01_sigesguarda_-_Base_de_Dados_limpo.csv', low_memory=False)
df_renda = pd.read_csv('../PÓS/renda_populacao_bairros.csv')
df_renda

# %% [markdown]
# ### Manipulação dos dataset 

# %% [markdown]
# #### Selecionando colunas de interesse em novo dataset

# %%
df_renda = df_renda.loc[:, ['Bairros', 'Rendimento mensal médio por responsáveis dos domicílios (R$)']]
df_renda

# %% [markdown]
# #### Adaptação de nome das colunas

# %%
df_renda = df_renda.rename(columns={
    'Bairros': 'ATENDIMENTO_BAIRRO_NOME',
    'Rendimento mensal médio por responsáveis dos domicílios (R$)': 'RENDA'
})


# %% [markdown]
# ##### Ajuste das variáveis para união dos dataframes

# %%
df_renda['ATENDIMENTO_BAIRRO_NOME'] = df_renda['ATENDIMENTO_BAIRRO_NOME'].replace('CIDADE INDUSTRIAL DE CURITIBA', 'CIDADE INDUSTRIAL')
df_renda['ATENDIMENTO_BAIRRO_NOME'] = df_renda['ATENDIMENTO_BAIRRO_NOME'].apply(lambda x: unidecode(x).upper())
df['ATENDIMENTO_BAIRRO_NOME'] = df['ATENDIMENTO_BAIRRO_NOME'].apply(lambda x: unidecode(x).upper())


# %%
df_renda

# %% [markdown]
# #### Salvando novo dataframe

# %%
df_renda.to_csv('../PÓS/df_renda.csv')


# %%
df_renda = pd.read_csv('../PÓS/df_renda.csv')
df_renda


# %% [markdown]
# ### Criando dataframe único

# %%
df_final = pd.merge(df, df_renda, on='ATENDIMENTO_BAIRRO_NOME', how='left')
df_final = df_final.dropna()
df_final.info()

# %% [markdown]
# ##### Salvando dataset

# %%
df_final.to_csv('../PÓS/df_com_renda.csv', index = False)

# %%
df = pd.read_csv('../PÓS/df_com_renda.csv')
df

# %% [markdown]
# ### Criando coluna Frequência (por tipo de ocorrência)

# %%
df['FREQUENCIA'] = df.groupby(['ATENDIMENTO_BAIRRO_NOME', 'NATUREZA1_DESCRICAO'])['NATUREZA1_DESCRICAO'].transform('count')


# %% [markdown]
# ### Criando dataframe de frequências

# %% [markdown]
# #### Tabela Pivot 

# %%
# Pivot table
df_ocorr = df.pivot_table(index='ATENDIMENTO_BAIRRO_NOME', columns='NATUREZA1_DESCRICAO', values='FREQUENCIA', aggfunc='sum')
df_ocorr.fillna(0, inplace=True)
df_ocorr.drop_duplicates(inplace=True)
df_ocorr


# %% [markdown]
# #### Salvando novo dataset

# %%
df_ocorr.to_csv('../PÓS/df_ocorrencia.csv', index = True)

# %%
df_ocorr = pd.read_csv('../PÓS/df_ocorrencia.csv')
df_ocorr

# %% [markdown]
# ### Modelagem - Cluester

# %% [markdown]
# ##### Adequação de colunas

# %%
# Substituir vírgulas por pontos na coluna 'RENDA'
df_renda['RENDA'] = df_renda['RENDA'].str.replace(',', '.')
# Converter a coluna 'RENDA' para float
df_renda['RENDA'] = df_renda['RENDA'].astype(float)



# %%
df_renda = df_renda.sort_values(by='RENDA', ascending=False)


# %% [markdown]
# #### Utilizando KMeans para criação de cluster por renda
# 

# %%
X = df_renda[['RENDA']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
n_clusters = 7
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(X_scaled)
df_renda['Cluster'] = kmeans.labels_
print(df_renda[['ATENDIMENTO_BAIRRO_NOME', 'RENDA', 'Cluster']])

# %% [markdown]
# #### Criando cluster por frequência de ocorrência

# %%
X = df_ocorr.drop('ATENDIMENTO_BAIRRO_NOME', axis=1)
scaler = StandardScaler()
n_clusters = 7
agglomerative = AgglomerativeClustering(n_clusters=n_clusters)
clusters = agglomerative.fit_predict(X_scaled)
df_ocorr['Cluster'] = clusters
df_ocorr[['ATENDIMENTO_BAIRRO_NOME', 'Cluster']]


# %% [markdown]
# ## Plotagem 

# %%
plt.figure(figsize=(20, 20))
plt.scatter(df_renda['Cluster'], df_renda['ATENDIMENTO_BAIRRO_NOME'], c=df_renda['RENDA'], cmap='viridis')
plt.xlabel('Cluster')
plt.ylabel('Bairro')
plt.title('Clusters dos Bairros')
plt.colorbar(label='RENDA')
bairros_unicos = df_renda['ATENDIMENTO_BAIRRO_NOME'].unique()
for bairro in bairros_unicos:
    plt.axhline(y=bairro, color='gray', linestyle='--', linewidth=0.5)
plt.show()

# %% [markdown]
# ### Por Frequência de Ocorrência

# %%
plt.figure(figsize=(20, 20))
plt.scatter(df_ocorr['Cluster'], df_ocorr['ATENDIMENTO_BAIRRO_NOME'], c=df_ocorr['Cluster'], cmap='viridis')
plt.xlabel('Cluster')
plt.ylabel('Bairro')
plt.title('Clusters dos Bairros')
plt.xticks(rotation=90)  # Rotaciona os rótulos do eixo x para melhor visualização
plt.colorbar(label='Cluster')
bairros_unicos = df_renda['ATENDIMENTO_BAIRRO_NOME'].unique()
for bairro in bairros_unicos:
    plt.axhline(y=bairro, color='gray', linestyle='--', linewidth=0.5)

plt.show()


# %% [markdown]
# ## Análise de Correlação

# %%

plt.scatter(df_renda['Cluster'], df_ocorr['Cluster'])
plt.xlabel('Cluster de Renda')
plt.ylabel('Cluster de Ocorrência')
plt.title('Gráfico de Dispersão dos Clusters')
plt.show()

# %%
correlation = df_renda['Cluster'].corr(df_ocorr['Cluster'])
print("Correlação entre os clusters de renda e ocorrência:", correlation)


