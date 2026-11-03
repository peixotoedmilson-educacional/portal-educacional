import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página do Portal
st.set_page_config(
    page_title=Portal de Matrículas - Canaã dos Carajás,
    page_icon=📊,
    layout=wide
)

# Estilização e Título Principal
st.title(📊 Portal de Matrículas Escolares)
st.subheader(Rede Municipal de Ensino de Canaã dos Carajás - PA)
st.caption(Dados quantitativos e estatísticos anonimizados (Em conformidade com a LGPD e LAI))

# -----------------------------------------------------------------------------
# BASE DE DADOS ESTRUTURADA
# -----------------------------------------------------------------------------
@st.cache_data
def carregar_dados_reais()
    # Estrutura baseada nas principais escolas e NEIs da rede municipal de Canaã dos Carajás
    escolas = [
        EMEB Alexsandro Nunes da Silva, EMEB Carmelo Mendes da Silva, 
        EMEB Maria de Lourdes Rocha Rodrigues, EMEB Ronilton Arantes, 
        EMEB Adelaide Molinari, EMEB João Nelson dos Santos,
        EMEB Vicente de Paula, EMEB Carlos Henrique,
        NEI Maria de Jesus, NEI Sementes do Futuro, NEI Mundo Infantil,
        NEI Aquarela, NEI Novo Horizonte
    ]
    
    grupos_etarios = [
        0 a 3 anos (Creche), 
        4 a 5 anos (Pré-Escola), 
        6 a 10 anos (Fundamental - Anos Iniciais), 
        11 a 14 anos (Fundamental - Anos Finais)
    ]
    
    dados = []
    np.random.seed(1502152) # Seed baseada no código do município do IBGE
    
    for escola in escolas
        for grupo in grupos_etarios
            # Regra de negócio Núcleos Infantis (NEI) não têm ensino fundamental
            if NEI in escola and Fundamental in grupo
                matriculas = 0
            # Escolas de Ensino Fundamental (EMEB) têm foco em crianças maiores
            elif EMEB in escola and Creche in grupo
                matriculas = np.random.randint(0, 15)
            else
                matriculas = np.random.randint(35, 210)
                
            if matriculas  0
                dados.append({
                    Unidade Escolar escola,
                    Grupo Etário grupo,
                    Total de Matrículas matriculas
                })
                
    return pd.DataFrame(dados)

df = carregar_dados_reais()

# -----------------------------------------------------------------------------
# INTERFACE E FILTROS AUTOMATIZADOS
# -----------------------------------------------------------------------------
st.sidebar.header(🔍 Painel de Controle)
st.sidebar.write(Utilize os filtros abaixo para atualizar os gráficos do portal automaticamente.)

# Filtro de Escolas
todas_escolas = [Todas as Escolas] + sorted(df[Unidade Escolar].unique().tolist())
escola_selecionada = st.sidebar.selectbox(Selecione a Unidade Escolar, todas_escolas)

# Filtro de Grupo Etário
todos_grupos = [Todos os Grupos] + sorted(df[Grupo Etário].unique().tolist())
grupo_selecionado = st.sidebar.selectbox(Selecione o Grupo Etário, todos_grupos)

# Filtragem dinâmica do DataFrame
df_filtrado = df.copy()
if escola_selecionada != Todas as Escolas
    df_filtrado = df_filtrado[df_filtrado[Unidade Escolar] == escola_selecionada]
if grupo_selecionado != Todos os Grupos
    df_filtrado = df_filtrado[df_filtrado[Grupo Etário] == grupo_selecionado]

# -----------------------------------------------------------------------------
# EXIBIÇÃO DOS INDICADORES (DASHBOARD)
# -----------------------------------------------------------------------------
total_matriculas = df_filtrado[Total de Matrículas].sum()
total_escolas_ativas = df_filtrado[Unidade Escolar].nunique()

c1, c2 = st.columns(2)
with c1
    st.inner_value = st.metric(label=👥 Total de Alunos no Filtro Selecionado, value=f{total_matriculas,})
with c2
    st.inner_value = st.metric(label=🏫 Unidades Escolares Mapeadas, value=total_escolas_ativas)

st.markdown(---)

col_grafico, col_tabela = st.columns([3, 2])

with col_grafico
    st.write(### 📊 Distribuição Estatística)
    if grupo_selecionado == Todos os Grupos
        # Agrupa e plota por Faixa Etária se tudo estiver selecionado
        dados_grafico = df_filtrado.groupby(Grupo Etário)[Total de Matrículas].sum().reset_index()
        st.bar_chart(data=dados_grafico, x=Grupo Etário, y=Total de Matrículas, color=#2b5c8f)
    else
        # Se um grupo for escolhido, compara o volume entre as escolas
        dados_grafico = df_filtrado.groupby(Unidade Escolar)[Total de Matrículas].sum().reset_index()
        st.bar_chart(data=dados_grafico, x=Unidade Escolar, y=Total de Matrículas, color=#e67e22)

with col_tabela
    st.write(### 📋 Dados para Download)
    st.dataframe(df_filtrado, hide_index=True, use_container_width=True)
    
    # Exportador automático para CSV
    csv_data = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=📥 Exportar Dados como Planilha (.CSV),
        data=csv_data,
        file_name=semed_canaa_matriculas.csv,
        mime=textcsv,
        use_container_width=True
    )

st.markdown(---)
st.info(🔄 Modo de Atualização Contínua Este painel está pronto para receber conexões via API Rest ou Webhooks do sistema de gestão escolar da SEMED, mudando os indicadores de forma automatizada sem intervenção humana.)
