# %% [markdown]
# # Trabalho de Mineração de Dados
# 
# ### Nome: Letícia Trein Medeiros
# 
# ---
# 
# ### Sobre
# Este trabalho foi realizado utilizando as bases de dados públicas da Prefeitura de Curitiba. Os dados são oriundos do SiGesGuarda, que contém as ocorrências atendidas pela Guarda Municipal de Curitiba.
# 
# ---
# 
# ## Pacotes Necessários
# 
# ```python
# 
# 

# %%
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import davies_bouldin_score, silhouette_score #
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from unidecode import unidecode
from scipy.stats import chi2_contingency

# %% [markdown]
# ---
# ## Dados Originais
# ---
# 

# %%
df_cru = pd.read_csv('C:/Users/FOKO-01/Documents/leticia/POS/mineracao dados/trabalho/2024-04-01_sigesguarda_-_Base_de_Dados.csv')


# %% [markdown]
# ---
# ## Limpeza de Dados e Preparação
# ---
# 
# 

# %%
# Selecionar colunas de interesse e salvar o dataset adaptado
colunas_interesse = ['ATENDIMENTO_ANO', 'ATENDIMENTO_BAIRRO_NOME','NATUREZA1_DESCRICAO','OCORRENCIA_MES','REGIONAL_FATO_NOME']
df = df_cru[colunas_interesse]
df.to_csv('C:/Users/FOKO-01/Documents/leticia/POS/mineracao dados/trabalho/df_policiacivil_adaptado.csv', index=False)  

# Carregar o dataset adaptado
df = pd.read_csv('C:/Users/FOKO-01/Documents/leticia/POS/mineracao dados/trabalho/df_policiacivil_adaptado.csv')  

# Limpeza de dados
df = df.dropna()
df = df[df['ATENDIMENTO_ANO'].apply(lambda x: str(x).isdigit())]
df['ATENDIMENTO_ANO'] = df['ATENDIMENTO_ANO'].astype(int)
df = df[df['OCORRENCIA_MES'].apply(lambda x: str(x).isdigit())]
df['OCORRENCIA_MES'] = df['OCORRENCIA_MES'].astype(int)

# Adequação das colunas
df['REGIONAL_FATO_NOME'] = df['REGIONAL_FATO_NOME'].str.upper()
df = df[df['ATENDIMENTO_BAIRRO_NOME'] != "NF"]
df = df[df['ATENDIMENTO_BAIRRO_NOME'] != "NI"]
df['NATUREZA1_DESCRICAO'] = df['NATUREZA1_DESCRICAO'].str.capitalize()

# Salvar dataset limpo
df_limpo = df
df_limpo.to_csv('C:/Users/FOKO-01/Documents/leticia/POS/mineracao dados/trabalho/2024-04-01_sigesguarda_-_Base_de_Dados_limpo.csv', index=False)


# %% [markdown]
# ---
# ## Adicionando Dados de Renda Populacional
# ---
# 
# 

# %%
# Carregar dados de renda
df_renda = pd.read_csv('C:/Users/FOKO-01/Documents/leticia/POS/mineracao dados/trabalho/renda_populacao_bairros.csv')

# Seleção e adequação das colunas
df_renda = df_renda.loc[:, ['Bairros', 'Média de Media latitude', 'Média de media longitude','Rendimento mensal médio por responsáveis dos domicílios (R$)']]
df_renda = df_renda.rename(columns={
    'Bairros': 'ATENDIMENTO_BAIRRO_NOME',
    'Média de Media latitude': 'LATITUDE',
    'Média de media longitude': 'LONGITUDE',
    'Rendimento mensal médio por responsáveis dos domicílios (R$)': 'RENDA'
})
df_renda['ATENDIMENTO_BAIRRO_NOME'] = df_renda['ATENDIMENTO_BAIRRO_NOME'].replace('CIDADE INDUSTRIAL DE CURITIBA', 'CIDADE INDUSTRIAL')
df_renda['ATENDIMENTO_BAIRRO_NOME'] = df_renda['ATENDIMENTO_BAIRRO_NOME'].apply(lambda x: unidecode(x).upper())
df['ATENDIMENTO_BAIRRO_NOME'] = df['ATENDIMENTO_BAIRRO_NOME'].apply(lambda x: unidecode(x).upper())
df_renda.to_csv('C:/Users/FOKO-01/Documents/leticia/POS/mineracao dados/trabalho/df_renda.csv', index=False)
df_renda = pd.read_csv('C:/Users/FOKO-01/Documents/leticia/POS/mineracao dados/trabalho/df_renda.csv')

# Unir datasets
df_final = pd.merge(df, df_renda, on='ATENDIMENTO_BAIRRO_NOME', how='left')
df_final = df_final.dropna()
df_final.to_csv('C:/Users/FOKO-01/Documents/leticia/POS/mineracao dados/trabalho/df_com_renda.csv', index=False)
df = pd.read_csv('C:/Users/FOKO-01/Documents/leticia/POS/mineracao dados/trabalho/df_com_renda.csv')


# %% [markdown]
# ---
# ## Criação de Dataset de Frequência dos Tipos de Ocorrência por Bairro
# ---

# %%
# Calcular a frequência de ocorrências por bairro
df['FREQUENCIA'] = df.groupby(['ATENDIMENTO_BAIRRO_NOME', 'NATUREZA1_DESCRICAO'])['NATUREZA1_DESCRICAO'].transform('count')
df_ocorr = df.pivot_table(index='ATENDIMENTO_BAIRRO_NOME', columns='NATUREZA1_DESCRICAO', values='FREQUENCIA', aggfunc='sum')
df_ocorr.fillna(0, inplace=True)
df_ocorr.drop_duplicates(inplace=True)
df_ocorr.to_csv('C:/Users/FOKO-01/Documents/leticia/POS/mineracao dados/trabalho/df_ocorrencia.csv', index=True)


# %% [markdown]
# ---
# ## Análise de Clusterização
# ---
# ### Clusterização de Crimes

# %%
# Criar a matriz de frequência de crimes por bairro
crime_matrix = df.pivot_table(index='ATENDIMENTO_BAIRRO_NOME', 
                              columns='NATUREZA1_DESCRICAO', 
                              values='FREQUENCIA', 
                              aggfunc='sum', 
                              fill_value=0)

# Aplicar K-Means
kmeans = KMeans(n_clusters=7, random_state=0)
crime_matrix['cluster'] = kmeans.fit_predict(crime_matrix)


# Adicionar as coordenadas de latitude e longitude
coordinates = df[['ATENDIMENTO_BAIRRO_NOME', 'LATITUDE', 'LONGITUDE']].drop_duplicates()
coordinates['LATITUDE'] = coordinates['LATITUDE'].str.replace(',', '.').astype(float)
coordinates['LONGITUDE'] = coordinates['LONGITUDE'].str.replace(',', '.').astype(float)

# Mesclar as coordenadas com os clusters
crime_matrix = crime_matrix.merge(coordinates, left_index=True, right_on='ATENDIMENTO_BAIRRO_NOME')

# Criar um mapa
mapa = folium.Map(location=[-25.4411, -49.2765], zoom_start=12)
colors = sns.color_palette('tab10', n_colors=10).as_hex()

# Adicionar os bairros ao mapa
for _, row in crime_matrix.iterrows():
    folium.CircleMarker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        radius=8,
        popup=row['ATENDIMENTO_BAIRRO_NOME'],
        color=colors[row['cluster']],
        fill=True,
        fill_color=colors[row['cluster']]
    ).add_to(mapa)

# Salvar e exibir o mapa
mapa.save('mapa_clusters_crimes.html')
mapa


# %% [markdown]
# ---
# 
# ### Clusterização por Renda

# %%
df['RENDA'] = df['RENDA'].str.replace('.', '').str.replace(',', '.').astype(float)

# %%
# Agrupar os dados para calcular a renda média por bairro
renda = df.groupby('ATENDIMENTO_BAIRRO_NOME')['RENDA'].mean().reset_index()

# Aplicar o KMeans para clustering baseado na renda
kmeans_renda = KMeans(n_clusters=7, random_state=0)
renda['cluster'] = kmeans_renda.fit_predict(renda[['RENDA']])

# Adicionar as coordenadas de latitude e longitude
coordinates = df[['ATENDIMENTO_BAIRRO_NOME', 'LATITUDE', 'LONGITUDE']].drop_duplicates()
coordinates['LATITUDE'] = coordinates['LATITUDE'].str.replace(',', '.').astype(float)
coordinates['LONGITUDE'] = coordinates['LONGITUDE'].str.replace(',', '.').astype(float)

# Mesclar os clusters de renda com as coordenadas
renda = renda.merge(coordinates, on='ATENDIMENTO_BAIRRO_NOME')

# Criar um mapa
mapa = folium.Map(location=[-25.4411, -49.2765], zoom_start=12)
# Check if the number of unique clusters is greater than the number of colors
if len(renda['cluster'].unique()) > len(colors):
    colors = sns.color_palette('tab10', n_colors=len(renda['cluster'].unique())).as_hex()

# Adicionar os bairros ao mapa
for _, row in renda.iterrows():
    folium.CircleMarker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        radius=8,
        popup=row['ATENDIMENTO_BAIRRO_NOME'],
        color=colors[row['cluster']],
        fill=True,
        fill_color=colors[row['cluster']]
    ).add_to(mapa)

# Salvar e exibir o mapa
mapa.save('mapa_clusters_renda.html')
mapa


# %% [markdown]
# ---
# ## Análise Comparativa dos Clusters
# 
# 

# %%

# Clusterização baseada em crimes
crime_matrix = df.pivot_table(index='ATENDIMENTO_BAIRRO_NOME', 
                              columns='NATUREZA1_DESCRICAO', 
                              values='FREQUENCIA', 
                              aggfunc='sum', 
                              fill_value=0)
kmeans_crime = KMeans(n_clusters=7, random_state=0)
crime_matrix['cluster_crime'] = kmeans_crime.fit_predict(crime_matrix)

# Clusterização baseada em renda
renda = df.groupby('ATENDIMENTO_BAIRRO_NOME')['RENDA'].mean().reset_index()
kmeans_renda = KMeans(n_clusters=7, random_state=0)
renda['cluster_renda'] = kmeans_renda.fit_predict(renda[['RENDA']])

# Adicionar as coordenadas de latitude e longitude
coordinates = df[['ATENDIMENTO_BAIRRO_NOME', 'LATITUDE', 'LONGITUDE']].drop_duplicates()
coordinates['LATITUDE'] = coordinates['LATITUDE'].str.replace(',', '.').astype(float)
coordinates['LONGITUDE'] = coordinates['LONGITUDE'].str.replace(',', '.').astype(float)

# Mesclar os clusters de crimes e de renda com as coordenadas
crime_matrix = crime_matrix.merge(coordinates, left_index=True, right_on='ATENDIMENTO_BAIRRO_NOME')
renda = renda.merge(coordinates, on='ATENDIMENTO_BAIRRO_NOME')

# Mesclar os clusters de crimes e de renda em um único DataFrame
comparison_df = crime_matrix[['ATENDIMENTO_BAIRRO_NOME', 'cluster_crime', 'LATITUDE', 'LONGITUDE']].merge(
    renda[['ATENDIMENTO_BAIRRO_NOME', 'cluster_renda']], on='ATENDIMENTO_BAIRRO_NOME')

# Filtrar apenas os bairros que não mudaram de cluster
similar_clusters = comparison_df[comparison_df['cluster_crime'] == comparison_df['cluster_renda']]

# Criar um mapa centrado na cidade de Curitiba
mapa = folium.Map(location=[-25.4411, -49.2765], zoom_start=12)

# Definir cores para os clusters
colors = sns.color_palette('tab10', n_colors=7).as_hex()

# Adicionar os bairros ao mapa
for _, row in similar_clusters.iterrows():
    color = colors[row['cluster_crime']]
    folium.CircleMarker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        radius=8,
        popup=row['ATENDIMENTO_BAIRRO_NOME'],
        color=color,
        fill=True,
        fill_color=color
    ).add_to(mapa)

# Exibir o mapa
mapa


# %% [markdown]
# ---
# ## Análise de contingéncia 
# 
# 

# %%
# Criar a tabela de contingência
contingency_table = pd.crosstab(comparison_df['cluster_crime'], comparison_df['cluster_renda'])

# Exibir a tabela de contingência
print(contingency_table)

# Aplicar o teste do qui-quadrado
chi2, p, dof, expected = chi2_contingency(contingency_table)

# Exibir os resultados
print(f"Qui-quadrado: {chi2}")
print(f"p-valor: {p}")
print(f"Graus de liberdade: {dof}")
print("Frequências esperadas:")
print(expected)

# %% [markdown]
# --- 
# ## Resultados e Discussões
# ---
# 
# 
# 

# %% [markdown]
# 1) O trabalho iniciou com a pergunta "Será que a renda influencia o perfil das ocorrências policiais no bairro?", para isso foi necessário a utilização de 2 bases de dados, tanto a da SiGesGuarda quando das informações de renda média da população de cada bairro.  
# 
# 2) Após a união dos datasets, foi criado um novo dataset contendo as frequências de cada tipo de ocorrência para utilização na modelagem de clusterização.  
# 
# 3) Foram utilizados modelos de clusterização (por modelo KMeans) para unir os bairros em grupos mais semelhantes, primeiramente unindo-os pelos tipos de ocorrência mais frequentes e depois pela semelhança da renda populacional
# 
# 4) Após entendido como os grupos se comportariam de forma independente, foi realizada a análise comparativa dos clusters formados, unindo apenas aqueles que se assemelharam nas modelagens anteriores, resultando em apenas 10 grupos semelhantes em ambas clusterizações
# 
# 5) Para validação do resultado obtido, foi realizado a análise de contigência (pelo qui-quadrado) para validar ou negar a hipotese nula ("A renda do bairro influencia no perfil dos principais tipos de ocorrência policiais" ). 
# - Com um p-valor: 0.7413111492453468, temos que a hipotese nula é rejeitada e concluimos que a renda não é influenciadora no perfil dos principais tipos de ocorrências policiais. 


