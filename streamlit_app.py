import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import unicodedata
import ipywidgets as widgets
from IPython.display import display, clear_output

#dados
url = 'https://raw.githubusercontent.com/LuizVicenteJr/dados_atendimentos_educacionais_streamlit/main/ad_planetario.csv'
data = pd.read_csv(url)

renomear_colunas = {
    'Carimbo de data/hora' : 'carimbo',
    'Confirmação co-host' : 'confirmação',
    'Data': 'data',
    'Horário': 'horário',
    'Host' : 'host',
    'Co-host' : 'co-host',
    'Nome da Escola': 'escola',
    'Município' : 'municipio',
    'Estado' : 'estado',
    'Urbana ou rural' : 'urbana_rural',
    'Pública ou privada' : 'publico_privada',
    'Público' : 'segmento', 
    'Público total': 'publico_total',
    'Observações: (caso tenha algum problema na sessão, escreva aqui)' : 'observações',
    'Outra escolas na mesma sessão?' : 'outra_escola',
    'Nome da escola ' :'escola_2',
    'Público ': 'segmento_2',
    'Total de público' : 'publico_total_2',
    'Município ' : 'municipio_2',
    'Estado ' : 'estado_2',
    'Urbana ou rural ' : 'urbana_rural_2',
    'Pública ou privada ' : 'publico_privada_2',
    'Outra escolas na mesma sessão?.1': 'outra_escola_2',
    'Nome da escola .1' : 'escola_3', 
    'Público .1' : 'segmento_3',
    'Total de público.1' : 'publico_total_3',
    'Município .1' : 'municipio_3',
    'Estado .1' : 'estado_3',
    'Urbana ou rural .1' : 'urbana_rural_3',
    'Pública ou privada .1' : 'publica_privada_3',
    'Comentários?' : 'observações_2',
    'Nome da escola .2' :'escola_4',
    'Público .2' : 'segmento_4',
    'Total de público.2' : 'publico_total_4',
    'Município .2' : 'municipio_4',
    'Estado .2' : 'estado_4',
    'Urbana ou rural .2' : 'urbana_rural_4',
    'Pública ou privada .2' : 'publica_privada_4',
    'Comentários?.1' : 'observações_3',
    'Nome da escola .3' : 'escola_4',
    'Público .3' : 'segmento_5', 
    'Total de público.3' : 'publico_total_5',
    'Município .3' : 'municipio_5',
    'Estado .3' : 'estado_5',
    'Urbana ou rural .3' : 'urbana_rural_5',
    'Pública ou privada .3' : 'publico_privada_5',
    'Comentários?.2' : 'observações_4',
    'Outra escolas na mesma sessão?.2' : 'outra_escola_3',
    'Outra escolas na mesma sessão?.3' : 'outra_escola_4',
    'Público TOTAL da sessão' : 'total'
}
# Renomear as colunas no DataFrame
df1 = data.rename(columns=renomear_colunas)

# primeiro filtro de colunas
df1_filtrado = df1.drop(['confirmação','carimbo','observações','observações_2','observações_3','observações_4',
                         'host','co-host','escola','escola_2','escola_3','escola_4','outra_escola',
                         'outra_escola_2','outra_escola_3','outra_escola_4'],axis=1)

#preenche falta de púlbico com zero
df1_filtrado['publico_total'] = df1_filtrado['publico_total'].fillna(0)
df1_filtrado['publico_total_2'] = df1_filtrado['publico_total_2'].fillna(0)
df1_filtrado['publico_total_3'] = df1_filtrado['publico_total_3'].fillna(0)
df1_filtrado['publico_total_4'] = df1_filtrado['publico_total_4'].fillna(0)
df1_filtrado['publico_total_5'] = df1_filtrado['publico_total_5'].fillna(0)
df1_filtrado['total'] = df1_filtrado['total'].fillna(0)

# tipo dos dados
df1_filtrado['data'] = pd.to_datetime(df1_filtrado['data'])
df1_filtrado['horário'] = pd.to_datetime(df1_filtrado['horário'], format='%H:%M:%S').dt.strftime('%H')
df1_filtrado['publico_total'] = df1_filtrado['publico_total'].astype(int)
df1_filtrado['publico_total_2'] = df1_filtrado['publico_total_2'].astype(int)
df1_filtrado['publico_total_3'] = df1_filtrado['publico_total_3'].astype(int)
df1_filtrado['publico_total_4'] = df1_filtrado['publico_total_4'].astype(int)
df1_filtrado['publico_total_5'] = df1_filtrado['publico_total_5'].astype(int)
df1_filtrado['total'] = df1_filtrado['total'].astype(int)

#manipulações
df2 = df1_filtrado.copy()

# Concatenar as colunas em uma única série
estado_total = pd.concat([df2['estado'], df2['estado_2'], df2['estado_3'], df2['estado_4'], df2['estado_5']])

# Remover linhas com valores ausentes
estado_total = estado_total.dropna()

# Criar um novo DataFrame com a coluna "estado_total"
estado_total = pd.DataFrame({'estado_total': estado_total})


# Definir a estrutura da página
st.sidebar.title('Menu')
pagina = st.sidebar.selectbox('Selecione uma opção', ['Home', 'Data', 'Horário','Estado',
                                                      'Município','Urbana/Rural','Público/Privada',
                                                      'Segmento Educacional'])


# Página "Home"
if pagina == 'Home':
    st.title('Página Home')
    st.write('Navegue pelas opções a esquerda para visualizações gráficas.')

# Página "Data"
elif pagina == 'Data':
    st.title('Escolha entre analisar os atendimentos por dia da semana ou agrupá-los por mês!')

    # Opções de análise
    opcao_analise = st.selectbox('Escolha uma opção de análise', ['Distribuição dos atendimentos por dia', 'Número de atendimentos virtuais por mês'])

    if opcao_analise == 'Distribuição dos atendimentos por dia':
        # Agrupar os dados por dia da semana e contar o número de atendimentos em cada dia
        atendimentos_por_dia_semana = df2.groupby(df2['data'].dt.day_name()).size()

        # Plotar o gráfico de barras
        fig, ax = plt.subplots()
        ax.bar(atendimentos_por_dia_semana.index, atendimentos_por_dia_semana, color='purple')

        # Adicionar anotações em cima de cada barra
        for i, v in enumerate(atendimentos_por_dia_semana):
            ax.text(i, v, str(v), ha='center', va='bottom')

        # Configurar o título e os rótulos dos eixos
        ax.set_title('Distribuição dos atendimentos por dia')
        ax.set_xlabel('Dia da Semana')
        ax.set_ylabel('Número de atendimentos')
        
        # Definir os rótulos dos dias da semana em português
        dias_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']

        # Criar uma lista com os índices correspondentes aos dias da semana
        indices = np.arange(len(dias_semana))

        # Definir os rótulos e os locais de tick no eixo x
        ax.set_xticks(indices)
        ax.set_xticklabels(dias_semana, rotation=45)
        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

    elif opcao_analise == 'Número de atendimentos virtuais por mês':
        # Agrupar os dados por mês e contar o número de atendimentos em cada mês
        atendimentos_por_mes = df2.groupby(df2['data'].dt.to_period('M')).size()

        # Plotar o gráfico de barras
        fig, ax = plt.subplots()
        ax.bar(atendimentos_por_mes.index.astype(str), atendimentos_por_mes, color='purple')

        # Adicionar anotações em cima de cada barra
        for i, v in enumerate(atendimentos_por_mes):
            ax.text(i, v, str(v), ha='center', va='bottom')

        # Configurar o título e os rótulos dos eixos
        ax.set_title('Número de atendimentos virtuais por mês')
        ax.set_xlabel('Ano-Mês')
        ax.set_ylabel('Número de atendimentos')

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

elif pagina == 'Horário':
    st.title('Escolha entre analisar a distribuição de atendimentos por horário ou agrupar os atendimentos por turno .')

    # Contar o número de atendimentos para cada horário
    contagem_horarios = df2['horário'].value_counts().sort_index()

    # Opções de análise
    opcao_analise = st.selectbox('Escolha uma opção de análise', ['Distribuição de Atendimentos por Turno', 'Número de Atendimentos por Horário'])

    if opcao_analise == 'Distribuição de Atendimentos por Turno':
        # Definir os limites dos turnos
        manha_inicio = 7
        manha_fim = 12
        tarde_inicio = 13
        tarde_fim = 17
        noite_inicio = 18
        noite_fim = 20

        # Criar listas vazias para armazenar as contagens dos turnos
        contagem_manha = []
        contagem_tarde = []
        contagem_noite = []

        # Iterar sobre os horários e contar o número de atendimentos para cada turno
        for horario, contagem in contagem_horarios.items():
            horario = int(horario)
            if manha_inicio <= horario <= manha_fim:
                contagem_manha.append(contagem)
            elif tarde_inicio <= horario <= tarde_fim:
                contagem_tarde.append(contagem)
            elif noite_inicio <= horario <= noite_fim:
                contagem_noite.append(contagem)

        # Plotar o gráfico de barras com a cor roxa
        fig, ax = plt.subplots()
        ax.bar(['Manhã', 'Tarde', 'Noite'], [sum(contagem_manha), sum(contagem_tarde), sum(contagem_noite)], color='purple')

        # Configurar o título e os rótulos dos eixos
        ax.set_title('Distribuição de Atendimentos por Turno')
        ax.set_xlabel('Turno')
        ax.set_ylabel('Número de atendimentos')

        # Adicionar os valores exatos em cima de cada barra
        for i, v in enumerate([sum(contagem_manha), sum(contagem_tarde), sum(contagem_noite)]):
            ax.text(i, v, str(v), ha='center', va='bottom')

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

    elif opcao_analise == 'Número de Atendimentos por Horário':
        # Plotar o gráfico de barras com a cor roxa
        fig, ax = plt.subplots()
        ax.bar(contagem_horarios.index, contagem_horarios.values, color='purple')

        # Configurar o título e os rótulos dos eixos
        ax.set_title('Número de Atendimentos por Horário')
        ax.set_xlabel('Horário')
        ax.set_ylabel('Número de Atendimentos')

        # Adicionar os valores exatos em cima de cada barra
        for i, v in enumerate(contagem_horarios.values):
            ax.text(i, v, str(v), ha='center', va='bottom')

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

# Página Estado
elif pagina == 'Estado':
    st.title('Escolha entre analisar a distribuição de atendimentos por estado ou por região.')

    # Opções de análise
    opcao_analise = st.selectbox('Escolha uma opção de análise', ['Distribuição de Atendimentos por estado', 'Distribuição de Atendimentos por região'])

    if opcao_analise == 'Distribuição de Atendimentos por estado':
        # Concatenar as colunas em uma única série
        estado_total = pd.concat([df2['estado'], df2['estado_2'], df2['estado_3'], df2['estado_4'], df2['estado_5']])

        # Remover linhas com valores ausentes
        estado_total = estado_total.dropna()

        # Criar um novo DataFrame com a coluna "estado_total"
        estado_total = pd.DataFrame({'estado_total': estado_total})

        # Contar a frequência de cada estado
        contagem_estados = estado_total['estado_total'].value_counts()

        # Plotar o gráfico de barras com a cor roxa
        fig, ax = plt.subplots()
        ax.bar(contagem_estados.index, contagem_estados.values, color='purple')

        # Adicionar os valores numéricos em cima das barras
        for i, v in enumerate(contagem_estados):
            ax.text(i, v, str(v), ha='center', va='bottom')

        # Configurar o título e os rótulos dos eixos
        ax.set_title('Número de Atendimentos Virtuais por Estado')
        ax.set_xlabel('Estado')
        ax.set_ylabel('Número de Atendimentos')

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

    elif opcao_analise == 'Distribuição de Atendimentos por região':
        # Mapear os estados para as regiões correspondentes
        regioes = {
            'NORTE': ['AC', 'AP', 'AM', 'PA', 'RR', 'RO', 'TO'],
            'SUL': ['PR', 'RS', 'SC'],
            'CENTRO-OESTE': ['GO', 'MT', 'MS', 'DF'],
            'NORDESTE': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
            'SUDESTE': ['ES', 'MG', 'RJ', 'SP']
        }
        # Criar a coluna 'regiao' com base nos estados
        estado_total['regiao'] = estado_total['estado_total'].map({estado: regiao for regiao, estados in regioes.items() for estado in estados})

        # Contar o número de atendimentos por região
        contagem_regioes = estado_total['regiao'].value_counts()

        # Plotar o gráfico de barras com a cor roxa
        fig, ax = plt.subplots()
        ax.bar(contagem_regioes.index, contagem_regioes.values, color='purple')

        # Adicionar os valores numéricos em cima das barras
        for i, v in enumerate(contagem_regioes):
            ax.text(i, v, str(v), ha='center', va='bottom')

        # Configurar o título e os rótulos dos eixos
        ax.set_title('Número de Atendimentos Virtuais por Região')
        ax.set_xlabel('Região')
        ax.set_ylabel('Número de Atendimentos')

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)
# Página "Município"
elif pagina == 'Município':
    st.title('Gráfico de Atendimentos por Município')

    # Concatenar as colunas em uma única série
    municipio_total = pd.concat([df2['municipio'], df2['municipio_2'], df2['municipio_3'], df2['municipio_4'], df2['municipio_5']])

    # Remover linhas com valores ausentes
    municipio_total = municipio_total.dropna()

    # Criar um novo DataFrame com a coluna "municipio_total"
    municipio_total = pd.DataFrame({'municipio_total': municipio_total})

    # Limpar e padronizar os valores da coluna 'municipio_total'
    municipio_total['municipio_total'] = municipio_total['municipio_total'].str.lower().str.strip()

    def remover_acentos(texto):
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        return texto

    municipio_total['municipio_total'] = municipio_total['municipio_total'].apply(remover_acentos)

    # Concatenar estado e município
    concatenado = pd.concat([estado_total['estado_total'], municipio_total['municipio_total']], axis=1)

    # Criar o dropdown com as opções de estado
    dropdown_estado = st.sidebar.selectbox('Selecione o estado:', concatenado['estado_total'].unique())

    def atualizar_grafico():
        estado_selecionado = dropdown_estado

        # Filtrar os dados para o estado selecionado
        dados_estado = concatenado[concatenado['estado_total'] == estado_selecionado]

        # Contar o número de atendimentos por município
        contagem_municipio = dados_estado['municipio_total'].value_counts()

        # Plotar o gráfico de barras
        plt.clf()  # Limpar o gráfico anterior
        ax = contagem_municipio.plot(kind='bar', color='purple')
        plt.xlabel('Município')
        plt.ylabel('Número de Atendimentos')
        plt.title(f'Atendimentos por Município - {estado_selecionado}')

        # Exibir o número de atendimentos acima de cada barra
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')

        st.pyplot(plt)

    # Exibir o gráfico inicial
    atualizar_grafico()

    # Página "Urbana/Rural"
elif pagina == 'Urbana/Rural':
    st.title('Gráfico de Atendimentos por área urbana e rural')

    # Concatenar as colunas em uma única série
    urbana_rural = pd.concat([df2['urbana_rural'], df2['urbana_rural_2'], df2['urbana_rural_3'], df2['urbana_rural_4'], df2['urbana_rural_5']])

    # Remover linhas com valores ausentes
    urbana_rural = urbana_rural.dropna()

    # Criar um novo DataFrame com a coluna "urbana_rural"
    urbana_rural = pd.DataFrame({'urbana_rural': urbana_rural})

    # Concatenar estado e zona
    concat_estado_zona = pd.concat([estado_total['estado_total'], urbana_rural['urbana_rural']], axis=1)

    # Criar a barra lateral
    st.sidebar.title('Opções')

    # Criar o selectbox com os estados dentro da barra lateral
    estado_selecionado = st.sidebar.selectbox('Estado:', ['Todos os Estados'] + list(concat_estado_zona['estado_total'].unique()))

    if estado_selecionado == 'Todos os Estados':
        # Calcular a contagem de atendimentos em zona rural e urbana para todos os estados
        contagem_geral = concat_estado_zona['urbana_rural'].value_counts()

        # Criar o gráfico de barras para a análise geral
        fig_geral, ax_geral = plt.subplots(figsize=(8, 6))
        ax_geral.bar(contagem_geral.index, contagem_geral.values, color='purple')

        # Adicionar o número de atendimentos em cima das barras
        for i, valor in enumerate(contagem_geral.values):
            ax_geral.text(i, valor, str(valor), ha='center', va='bottom')

        # Configurar os rótulos e o título do gráfico para a análise geral
        ax_geral.set_xlabel('Zona')
        ax_geral.set_ylabel('Número de Atendimentos')
        ax_geral.set_title('Contagem de Atendimentos por Zona - Análise Geral')

        # Exibir o gráfico no Streamlit para a análise geral
        st.pyplot(fig_geral)
    else:
        # Filtrar os dados pelo estado selecionado
        dados_estado_selecionado = concat_estado_zona[concat_estado_zona['estado_total'] == estado_selecionado]

        # Calcular a contagem de atendimentos em zona rural e urbana para o estado selecionado
        contagem_estado_selecionado = dados_estado_selecionado['urbana_rural'].value_counts()

        # Criar o gráfico de barras para o estado selecionado
        fig_estado_selecionado, ax_estado_selecionado = plt.subplots(figsize=(8, 6))
        ax_estado_selecionado.bar(contagem_estado_selecionado.index, contagem_estado_selecionado.values, color='purple')

        # Adicionar o número de atendimentos em cima das barras
        for i, valor in enumerate(contagem_estado_selecionado.values):
            ax_estado_selecionado.text(i, valor, str(valor), ha='center', va='bottom')

        # Configurar os rótulos e o título do gráfico para o estado selecionado
        ax_estado_selecionado.set_xlabel('Zona')
        ax_estado_selecionado.set_ylabel('Número de Atendimentos')
        ax_estado_selecionado.set_title(f'Contagem de Atendimentos por Zona - {estado_selecionado}')

        # Exibir o gráfico no Streamlit para o estado selecionado
        st.pyplot(fig_estado_selecionado)

        # Página "Urbana/Rural"
elif pagina == 'Público/Privada':
    st.title('Gráfico de Atendimentos por instituição público ou privada')
    # Concatenar as colunas em uma única série
    publico_privada = pd.concat([df2['publico_privada'], df2['publico_privada_2'], df2['publica_privada_3'], df2['publica_privada_4'], df2['publico_privada_5']])

    # Remover linhas com valores ausentes
    publico_privada = publico_privada.dropna()

    # Criar um novo DataFrame com a coluna "publico_privada"
    publico_privada = pd.DataFrame({'publico_privada': publico_privada})

    # Concatenar estado e tipo de instituição
    concat_estado_instituicao = pd.concat([estado_total['estado_total'], publico_privada['publico_privada']], axis=1)
    
    # Criar a barra lateral
    st.sidebar.title('Opções')

    # Criar o selectbox com os estados dentro da barra lateral
    estado_selecionado = st.sidebar.selectbox('Estado:', ['Todos os Estados'] + list(concat_estado_instituicao['estado_total'].unique()))
    
    if estado_selecionado == 'Todos os Estados':
        # Calcular a contagem de atendimentos em zona rural e urbana para todos os estados
        contagem_geral = concat_estado_instituicao['publico_privada'].value_counts()

        # Criar o gráfico de barras para a análise geral
        fig_geral, ax_geral = plt.subplots(figsize=(8, 6))
        ax_geral.bar(contagem_geral.index, contagem_geral.values, color='purple')

        # Adicionar o número de atendimentos em cima das barras
        for i, valor in enumerate(contagem_geral.values):
            ax_geral.text(i, valor, str(valor), ha='center', va='bottom')

        # Configurar os rótulos e o título do gráfico para a análise geral
        ax_geral.set_xlabel('Instituição')
        ax_geral.set_ylabel('Número de atendimentos')
        ax_geral.set_title('Contagem de atendimentos por instituição- pública ou privada')

        # Exibir o gráfico no Streamlit para a análise geral
        st.pyplot(fig_geral)
    else:
        # Filtrar os dados pelo estado selecionado
        dados_estado_selecionado = concat_estado_instituicao[concat_estado_instituicao['estado_total'] == estado_selecionado]

        # Calcular a contagem de atendimentos em instituição pública e privada para o estado selecionado
        contagem_estado_selecionado = dados_estado_selecionado['publico_privada'].value_counts()

        # Criar o gráfico de barras para o estado selecionado
        fig_estado_selecionado, ax_estado_selecionado = plt.subplots(figsize=(8, 6))
        ax_estado_selecionado.bar(contagem_estado_selecionado.index, contagem_estado_selecionado.values, color='purple')

        # Adicionar o número de atendimentos em cima das barras
        for i, valor in enumerate(contagem_estado_selecionado.values):
            ax_estado_selecionado.text(i, valor, str(valor), ha='center', va='bottom')

        # Configurar os rótulos e o título do gráfico para o estado selecionado
        ax_estado_selecionado.set_xlabel('Instituição')
        ax_estado_selecionado.set_ylabel('Número de Atendimentos')
        ax_estado_selecionado.set_title(f'Contagem de Atendimentos por Instituição - {estado_selecionado}')

        # Exibir o gráfico no Streamlit para o estado selecionado
        st.pyplot(fig_estado_selecionado)

elif pagina == 'Segmento Educacional':
    st.title('Gráfico de atendimentos por segmento')
    # Concatenar as colunas em uma única série
    
    segmento_total = pd.concat([df2['segmento'], df2['segmento_2'], df2['segmento_3'], df2['segmento_4'], df2['segmento_5']])

    # Remover linhas com valores ausentes
    segmento_total = segmento_total.dropna()

    # Criar um novo DataFrame com a coluna "segmento_total"
    segmento = pd.DataFrame({'segmento': segmento_total})

    # Redefinir o índice do DataFrame
    segmento = segmento.reset_index(drop=True)
    estado_total = estado_total.reset_index(drop=True)

    # Concatenar segmento e estados
    segmento_estado = pd.concat([segmento, estado_total['estado_total']], axis=1)

    # Criar a barra lateral
    st.sidebar.title('Opções')

    # Criar o selectbox com os estados dentro da barra lateral
    estado_selecionado = st.sidebar.selectbox('Estado:', ['Todos os Estados'] + list(segmento_estado['estado_total'].unique()))
    if estado_selecionado == 'Todos os Estados':
        # Contar a frequência de cada segmento
        contagem_segmento = segmento_estado['segmento'].value_counts()

        # Definir uma paleta de cores
        cores = ['purple', 'blue', 'green', 'yellow', 'orange']

        # Plotar o gráfico de barras com cores variadas
        fig, ax = plt.subplots(figsize=(8, 6))
        contagem_segmento.plot(kind='bar', color=cores, ax=ax)

        # Adicionar o número de atendimentos em cima de cada barra
        for i, v in enumerate(contagem_segmento):
            ax.text(i, v + 1, str(v), ha='center', va='bottom')

        # Configurar título e rótulos dos eixos
        plt.title('Atendimentos no Planetário por Segmento')
        plt.xlabel('Segmento')
        plt.ylabel('Número de Atendimentos')

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)
    else:
        # Filtrar os dados pelo estado selecionado
        dados_estado_selecionado = segmento_estado[segmento_estado['estado_total'] == estado_selecionado]

        # Calcular a contagem de atendimentos por segmento educacional
        contagem_estado_selecionado = dados_estado_selecionado['segmento'].value_counts()

        # Criar o gráfico de barras para o estado selecionado
        fig_estado_selecionado, ax_estado_selecionado = plt.subplots(figsize=(8, 6))
        ax_estado_selecionado.bar(contagem_estado_selecionado.index, contagem_estado_selecionado.values, color='purple')

        # Adicionar o número de atendimentos em cima das barras
        for i, valor in enumerate(contagem_estado_selecionado.values):
            ax_estado_selecionado.text(i, valor, str(valor), ha='center', va='bottom')

        # Configurar os rótulos e o título do gráfico para o estado selecionado
        ax_estado_selecionado.set_xlabel('Segmento')
        ax_estado_selecionado.set_ylabel('Número de Atendimentos')
        ax_estado_selecionado.set_title(f'Contagem de Atendimentos por segmento - {estado_selecionado}')

        # Exibir o gráfico no Streamlit para o estado selecionado
        st.pyplot(fig_estado_selecionado)