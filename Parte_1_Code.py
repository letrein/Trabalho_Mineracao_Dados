# %% [markdown]
# # Dados da Policia Civil

# %% [markdown]
# ### Importando pandas, lendo base de dados original e buscando valores nulos
# 

# %%
import pandas as pd
df_cru = pd.read_csv('../PÓS/2024-04-01_sigesguarda_-_Base_de_Dados.csv',sep = ";", encoding='latin-1')

# %% [markdown]
# ## Avaliando dados inicialmente
# 

# %%
df_cru.head(25)

# %% [markdown]
# # Limpeza de dados

# %% [markdown]
# ### Busca por valores nulos

# %%
df_cru.isnull().sum()

# %% [markdown]
# ## Fazendo novo dataset 

# %% [markdown]
# #### Selecionando as colunas de interesse, sendo estas com menor quantidade de valores nulos 
# 

# %%
colunas_interesse = ['ATENDIMENTO_ANO', 'ATENDIMENTO_BAIRRO_NOME', 'FLAG_FLAGRANTE', 'LOGRADOURO_NOME','NATUREZA1_DESCRICAO','OCORRENCIA_HORA','OCORRENCIA_MES','ORIGEM_CHAMADO_DESCRICAO','REGIONAL_FATO_NOME','SECRETARIA_NOME','SECRETARIA_SIGLA', 'SERVICO_NOME']
df = df_cru[colunas_interesse]
df.to_csv('../PÓS/df_policiacivil_adaptado.csv', index=False)  
df



# %% [markdown]
# #### Reavaliação de valores nulos

# %%
df= pd.read_csv('../PÓS/df_policiacivil_adaptado.csv')
df

# %%
#verificando presença de valores nulos
df.isnull().sum()


# %% [markdown]
# #### Retirada dos Valores nulos

# %%
df = df.dropna()

# %% [markdown]
#  #### Avaliação de valores nulos e Dtype das colunas

# %%
df.info()

# %% [markdown]
# ### Adequação dos dtype das colunas de valor numérico

# %%
#Ajuste das variáveis de ano
df = df[df['ATENDIMENTO_ANO'].apply(lambda x: str(x).isdigit())]
df['ATENDIMENTO_ANO'] = df['ATENDIMENTO_ANO'].astype(int)

#Ajuste das variáveis de mês
df = df[df['OCORRENCIA_MES'].apply(lambda x: str(x).isdigit())]
df['OCORRENCIA_MES'] = df['OCORRENCIA_MES'].astype(int)

#Ajuste das variáveis de hora
df['OCORRENCIA_HORA'] = pd.to_datetime(df['OCORRENCIA_HORA'], format='%H:%M:%S')


# %%
df.info()

# %% [markdown]
# ## Avaliação individual das colunas 

# %% [markdown]
# #### Foi colocado individualmente todas as colunas em busca de valores que não fizessem sentido para a análise. Segue os principais problemas encontrados e adequações realizadas

# %% [markdown]
# ### Avaliação dos Bairros

# %%
df['ATENDIMENTO_BAIRRO_NOME'].unique()

# %% [markdown]
# ####  Sendo encontrado valores inválidos para os bairros (NI, NF, Cajuru), foram adequados deixando todos os dados em maíusculo e  pela retirada dos valores (NI e NF)

# %%
# Deixando todos em maíusculo
df['REGIONAL_FATO_NOME'] = df['REGIONAL_FATO_NOME'].str.upper()

# Remover as linhas com "NF" na coluna "ATENDIMENTO_BAIRRO_NOME"
df = df[df['ATENDIMENTO_BAIRRO_NOME'] != "NF"]

# Remover as linhas com "NI" na coluna "ATENDIMENTO_BAIRRO_NOME"
df = df[df['ATENDIMENTO_BAIRRO_NOME'] != "NI"]


# %% [markdown]
# ### Avaliação Logradouros

# %%
df['LOGRADOURO_NOME'].unique()

# %% [markdown]
# #### Pela dificuldade de visualização, será buscado de forma diferente, através da seleção de colunas que contém "NI" ou "NF"

# %%
df[df['LOGRADOURO_NOME'] == "NI"]


# %%
df[df['LOGRADOURO_NOME'] == "NF"]

# %% [markdown]
# #### Adequando variáveis

# %%
# Deixando todos em maíusculo
df['LOGRADOURO_NOME'] = df['LOGRADOURO_NOME'].str.upper()

# Remover a linha com "NI" na coluna "LOGRADOURO_NOME"
df = df[df['LOGRADOURO_NOME'] != "NI"]



# %% [markdown]
# ### Avaliação Origem do chamado

# %%
df['ORIGEM_CHAMADO_DESCRICAO'].unique()

# %% [markdown]
# #### Retirada de valores inválidos

# %%
df = df[df['ORIGEM_CHAMADO_DESCRICAO'] != "."]

# %% [markdown]
# ### Avaliação Tipos de ocorrência

# %%
df['NATUREZA1_DESCRICAO'].unique()

# %% [markdown]
# #### Adequando para apenas primeira letra em maísculo

# %%
df['NATUREZA1_DESCRICAO'] = df['NATUREZA1_DESCRICAO'].str.capitalize()


# %% [markdown]
# ### Avaliação demais colunas

# %%
df['SECRETARIA_NOME'].unique()

# %%
df['REGIONAL_FATO_NOME'].unique()

# %%
df['SERVICO_NOME'].unique()

# %%
df['FLAG_FLAGRANTE'].unique()

# %%
df['SECRETARIA_SIGLA'].unique()

# %% [markdown]
# ## Salvando novo dataset 

# %%
df_limpo = df

df_limpo.to_csv('../PÓS/2024-04-01_sigesguarda_-_Base_de_Dados.csv', index=False)

# %%


# %%
    

# %%


# %% [markdown]
# Analise de dados
# 

# %%
import seaborn as sns
import matplotlib.pyplot as plt

# Aplicando configurações de estilo padrão (tema, escala e cores)
sns.set()

# %%

# Contagem de ocorrências por ano
ocorrencias_por_ano = df['ATENDIMENTO_ANO'].value_counts().sort_index()

# Criar gráfico de barras
plt.figure(figsize=(10, 6))
sns.barplot(x=ocorrencias_por_ano.index, y=ocorrencias_por_ano.values, color='skyblue')
plt.title('Número de Ocorrências Policiais por Ano')
plt.xlabel('Ano')
plt.ylabel('Número de Ocorrências')
plt.xticks(rotation=45)  # Rotacionar os rótulos do eixo x para melhor visualização
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo y
plt.show()


# %%
ocorrencias_flagrante = df['FLAG_FLAGRANTE'].value_counts()
plt.figure(figsize=(6, 6))
sns.barplot(x=ocorrencias_flagrante.index, y=ocorrencias_flagrante.values, palette='Set2')
plt.title('Distribuição de Ocorrências com Flagrante')
plt.xlabel('Flagrante')
plt.ylabel('Número de Ocorrências')
plt.show()

# %%
plt.figure(figsize=(6, 6))
plt.pie(ocorrencias_flagrante, labels=ocorrencias_flagrante.index, autopct='%1.1f%%', colors=['lightblue', 'lightgreen'], startangle=140)
plt.title('Distribuição de Ocorrências com Flagrante')
plt.show()

# %%
ocorrencias_por_mes = df['OCORRENCIA_MES'].value_counts().sort_index()

# Criar gráfico de barras
plt.figure(figsize=(10, 6))
sns.barplot(x=ocorrencias_por_mes.index, y=ocorrencias_por_mes.values, color='lightblue')
plt.title('Número de Ocorrências Policiais por Mês')
plt.xlabel('Mês')
plt.ylabel('Número de Ocorrências')
plt.xticks(rotation=45)  # Rotacionar os rótulos do eixo x para melhor visualização
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo y
plt.show()

# %%
origens_chamados = df['ORIGEM_CHAMADO_DESCRICAO'].value_counts()

# Criar gráfico de barras
plt.figure(figsize=(10, 6))
sns.barplot(x=origens_chamados.values, y=origens_chamados.index, palette='viridis')
plt.title('Distribuição das Origens dos Chamados')
plt.xlabel('Número de Chamados')
plt.ylabel('Origem do Chamado')
plt.grid(axis='x', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo x
plt.show()

# %%
ocorrencias_por_regional = df['REGIONAL_FATO_NOME'].value_counts()

# Criar gráfico de barras
plt.figure(figsize=(12, 6))
sns.barplot(x=ocorrencias_por_regional.values, y=ocorrencias_por_regional.index, palette='muted')
plt.title('Número de Ocorrências Policiais por Regional')
plt.xlabel('Número de Ocorrências')
plt.ylabel('Regional')
plt.grid(axis='x', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo x
plt.show()


# %%
# Contagem dos serviços mais frequentes
servicos_mais_frequentes = df['SERVICO_NOME'].value_counts()

# Criar gráfico de barras
plt.figure(figsize=(12, 6))
sns.barplot(x=servicos_mais_frequentes.values, y=servicos_mais_frequentes.index, palette='pastel')
plt.title('Serviços Mais Frequentes Realizados pela Polícia')
plt.xlabel('Número de Ocorrências')
plt.ylabel('Serviço')
plt.grid(axis='x', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo x
plt.show()

# %%
ocorrencias_por_bairro = df['ATENDIMENTO_BAIRRO_NOME'].value_counts().head(35)  # Vamos considerar apenas os 10 primeiros bairros

# Criar gráfico de barras horizontais
plt.figure(figsize=(10, 6))
sns.barplot(x=ocorrencias_por_bairro.values, y=ocorrencias_por_bairro.index, palette='rocket')
plt.title('Top 10 Bairros com Maior Número de Ocorrências')
plt.xlabel('Número de Ocorrências')
plt.ylabel('Bairro')
plt.grid(axis='x', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo x
plt.show()

# %%
ocorrencias_por_tipo = df['NATUREZA1_DESCRICAO'].value_counts().head(30)  # Vamos considerar apenas os 10 primeiros tipos de ocorrência

# Criar gráfico de barras horizontais
plt.figure(figsize=(10, 6))
sns.barplot(x=ocorrencias_por_tipo.values, y=ocorrencias_por_tipo.index, palette='mako')
plt.title('Top 10 Tipos de Ocorrência')
plt.xlabel('Número de Ocorrências')
plt.ylabel('Tipo de Ocorrência')
plt.grid(axis='x', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo x
plt.show()

# %%
ocorrencias_por_regional_bairro = df.groupby(['REGIONAL_FATO_NOME', 'ATENDIMENTO_BAIRRO_NOME']).size().reset_index(name='ocorrencias')

# Para cada regional, identificar o bairro com mais ocorrências
bairros_mais_ocorrencias_por_regional = ocorrencias_por_regional_bairro.groupby('REGIONAL_FATO_NOME').apply(lambda x: x.nlargest(5, 'ocorrencias'))

# Criar gráficos de barras horizontais para cada regional
for regional, data in bairros_mais_ocorrencias_por_regional.groupby(level=0):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='ocorrencias', y='ATENDIMENTO_BAIRRO_NOME', data=data, palette='muted')
    plt.title(f'Top 5 Bairros com Mais Ocorrências em {regional}')
    plt.xlabel('Número de Ocorrências')
    plt.ylabel('Bairro')
    plt.grid(axis='x', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo x
    plt.show()

# %%
# Filtrar as ocorrências relacionadas a roubo, furto ou crimes contra o patrimônio
ocorrencias_patrimonio = df[df['NATUREZA1_DESCRICAO'].str.contains('roubo|furto|patrimônio', case=False)]

# Agrupar os dados por bairro e contar o número de ocorrências de crimes contra o patrimônio em cada bairro
ocorrencias_por_bairro_patrimonio = ocorrencias_patrimonio['ATENDIMENTO_BAIRRO_NOME'].value_counts().head(10)

# Criar gráfico de barras horizontais
plt.figure(figsize=(10, 6))
sns.barplot(x=ocorrencias_por_bairro_patrimonio.values, y=ocorrencias_por_bairro_patrimonio.index, palette='muted')
plt.title('Top 10 Bairros com Mais Ocorrências de Crimes contra o Patrimônio')
plt.xlabel('Número de Ocorrências')
plt.ylabel('Bairro')
plt.grid(axis='x', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo x
plt.show()

# %%

# Supondo que você já carregou seus dados em um DataFrame chamado df

# Filtrar as ocorrências relacionadas a "apoio"
ocorrencias_apoio = df[df['NATUREZA1_DESCRICAO'].str.contains('Animais', case=False)]

# Agrupar os dados por bairro e contar o número de ocorrências de "apoio" em cada bairro
ocorrencias_por_bairro_apoio = ocorrencias_apoio['ATENDIMENTO_BAIRRO_NOME'].value_counts().head(10)

# Criar gráfico de barras horizontais
plt.figure(figsize=(10, 6))
sns.barplot(x=ocorrencias_por_bairro_apoio.values, y=ocorrencias_por_bairro_apoio.index, palette='muted')
plt.title('Top 10 Bairros com Mais Ocorrências de "Animais"')
plt.xlabel('Número de Ocorrências')
plt.ylabel('Bairro')
plt.grid(axis='x', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo x
plt.show()

# %%

df['HORA'] = pd.to_datetime(df['OCORRENCIA_HORA']).dt.hour

# Contagem das ocorrências por hora
ocorrencias_por_hora = df['HORA'].value_counts().sort_index()

# Criar gráfico de barras
plt.figure(figsize=(10, 6))
sns.barplot(x=ocorrencias_por_hora.index, y=ocorrencias_por_hora.values, color='skyblue')
plt.title('Número de Ocorrências por Hora do Dia')
plt.xlabel('Hora do Dia')
plt.ylabel('Número de Ocorrências')
plt.xticks(rotation=45)  # Rotacionar os rótulos do eixo x para facilitar a leitura
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo y
plt.show()

# %%
# Filtrar o DataFrame apenas para as ocorrências que ocorreram no centro
ocorrencias_centro = df[df['ATENDIMENTO_BAIRRO_NOME'] == 'CIDADE INDUSTRIAL']

# Verificar se há dados no DataFrame filtrado
if ocorrencias_centro.empty:
    print("Não há dados para o bairro Centro.")
else:
    # Converter a coluna 'OCORRENCIA_HORA' para o formato de data e hora
    ocorrencias_centro['OCORRENCIA_HORA'] = pd.to_datetime(ocorrencias_centro['OCORRENCIA_HORA'])

    # Extrair a hora do horário das ocorrências no centro
    ocorrencias_centro['HORA'] = ocorrencias_centro['OCORRENCIA_HORA'].dt.hour

    # Criar gráfico de distribuição das ocorrências por hora
    plt.figure(figsize=(10, 6))
    sns.histplot(data=ocorrencias_centro, x='HORA', bins=24, kde=True, color='skyblue')
    plt.title('Distribuição das Ocorrências no Centro por Hora do Dia')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Número de Ocorrências')
    plt.xticks(range(24))  # Definir os ticks do eixo x para representar as horas do dia
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo y
    plt.show()

# %%
# Filtrar o DataFrame para incluir apenas as ocorrências que contenham a palavra "óbito" na descrição
ocorrencias_obito = df[df['NATUREZA1_DESCRICAO'].str.contains('Vadiagem', case=False)]

# Contar o número de ocorrências por bairro
ocorrencias_por_bairro = ocorrencias_obito['ATENDIMENTO_BAIRRO_NOME'].value_counts()

# Criar gráfico de barras para visualizar a distribuição das ocorrências por bairro
plt.figure(figsize=(10, 6))
sns.barplot(x=ocorrencias_por_bairro.values, y=ocorrencias_por_bairro.index, palette='viridis')
plt.title('Distribuição de Ocorrências com Palavras Contendo "Óbito" por Bairro')
plt.xlabel('Número de Ocorrências')
plt.ylabel('Bairro')
plt.grid(axis='x', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo x
plt.show()

# %%
ocorrencias_batel = df[df['ATENDIMENTO_BAIRRO_NOME'] == 'PRADO VELHO']

# Verificar se há dados no DataFrame filtrado
if ocorrencias_batel.empty:
    print("Não há ocorrências no bairro JARDIM SOCIAL.")
else:
    # Contar o número de ocorrências por categoria ou descrição
    ocorrencias_por_categoria = ocorrencias_batel['NATUREZA1_DESCRICAO'].value_counts().head(5)

    # Criar gráfico de barras para visualizar a distribuição das ocorrências por categoria
    plt.figure(figsize=(12, 8))
    sns.barplot(y=ocorrencias_por_categoria.index, x=ocorrencias_por_categoria.values, palette='magma')
    plt.title('Top 5 ocorrências no bairro PRADO VELHO',fontsize=25)
    plt.xlabel('Número de Ocorrências')
    plt.ylabel(' ')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=20)
    plt.grid(axis='x', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo x
    plt.show()

ocorrencias_batel = df[df['ATENDIMENTO_BAIRRO_NOME'] == 'CABRAL']

# Verificar se há dados no DataFrame filtrado
if ocorrencias_batel.empty:
    print("Não há ocorrências no bairro JARDIM SOCIAL.")
else:
    # Contar o número de ocorrências por categoria ou descrição
    ocorrencias_por_categoria = ocorrencias_batel['NATUREZA1_DESCRICAO'].value_counts().head(5)

    # Criar gráfico de barras para visualizar a distribuição das ocorrências por categoria
    plt.figure(figsize=(12, 8))
    sns.barplot(y=ocorrencias_por_categoria.index, x=ocorrencias_por_categoria.values, palette='magma')
    plt.title('Top 5 ocorrências no bairro CABRAL',fontsize=25)
    plt.xlabel('Número de Ocorrências')
    plt.ylabel(' ')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=20)
    plt.grid(axis='x', linestyle='--', alpha=0.7)  # Adicionar linhas de grade no eixo x
    plt.show()


