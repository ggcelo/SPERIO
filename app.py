import streamlit as st


# Configurações gerais da página.
# função deve ser chamada antes de outros elementos do Streamlit.
st.set_page_config(
    page_title="Apoio à Decisão em Periodontia",
    page_icon="🦷",
    layout="wide"
)


# Título principal da aplicação.
st.title("Aplicação de Apoio à Decisão Clínica em Periodontia")

st.write(
    "Sistema para classificação periodontal e integração "
    "de ferramentas de rastreamento de risco."
)

st.divider()


# Escolha temporária apenas para entendermos como os widgets funcionam.
modulo = st.selectbox(
    "Escolha um módulo:",
    [
        "Classificação periodontal",
        "FINDRISC",
        "INTERHEART",
        "Análise radiográfica"
    ]
)

st.write("Módulo selecionado:", modulo)


# Experimento para entendermos a reexecução do Streamlit.
contador = 0

if st.button("Somar 1"):
    contador = contador + 1

st.write("Valor do contador:", contador)