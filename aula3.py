import pandas as pd
import streamlit as st

# Carregar os nossos acidentes
df_acidentes = pd.read_csv("./acidentes_2022.csv")
df_localidades = pd.read_csv("./localidades_2022.csv")

# Filtrar os dados de Rondônia
df_acidentes = df_acidentes[df_acidentes['uf_acidente'] == 'RO']
df_localidades = df_localidades[df_localidades['uf'] == 'RO']

# Agrupar os dados por município, para realizar a contagem de acidentes
df_acidentes_por_cidade = df_acidentes.groupby('codigo_ibge').size().reset_index(name='total_acidentes')

# Exclusão dos registros duplicados
munipios_unicos = df_localidades[['codigo_ibge', 'municipio']].drop_duplicates(subset=['codigo_ibge'])

# Junção das duas tabelas
df_acidentes_por_cidade = pd.merge(
    df_acidentes_por_cidade,
    munipios_unicos,
    on='codigo_ibge'
)

# Ordenação dos municípios pela quantidade de acidentes
df_acidentes_por_cidade.sort_values(by='total_acidentes', ascending=False, inplace=True)

top5 = df_acidentes_por_cidade.head(5)

# df_acidentes_por_cidade
# Começando a montar o gráfico para exibição no Streamlit
st.header("Top 5 cidades com mais acidentes de trânsito em Rondônia")
st.bar_chart(top5.set_index('municipio')['total_acidentes'])
