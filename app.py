import streamlit as st

from state import inicializar_session_state
from modulo_radiografico import mostrar_modulo_radiografico
from modulo_findrisc import mostrar_findrisc
from modulo_interheart import mostrar_interheart
from modulo_periodontal import mostrar_modulo_periodontal
from relatorio import mostrar_relatorio


st.set_page_config(
    page_title="Apoio à Decisão em Periodontia",
    page_icon="🦷",
    layout="wide"
)

st.title("Aplicação de Apoio à Decisão Clínica em Periodontia")

st.write(
    "Sistema para classificação periodontal e integração "
    "de ferramentas de rastreamento de risco."
)

st.divider()


# INICIALIZA OS DICIONÁRIOS DO SESSION_STATE
inicializar_session_state()


# MÓDULO RADIOGRÁFICO -> foi retirado daqui, movido tudo para o final da pagina

dados_caso_preenchidos = (
    st.session_state["dados_caso"]["codigo"] is not None
    and st.session_state["dados_caso"]["idade"] is not None
    and st.session_state["dados_caso"]["sexo"] is not None
)

with st.expander(
    "Dados do caso",
    expanded=not dados_caso_preenchidos
):

    with st.form("form_dados_caso"): #tudo dentro do with fica armazenado dentro do formulario

        codigo_digitado = st.text_input(
            "Código do caso:"
        )

        idade_digitada = st.number_input(
            "Idade:",
            min_value=1,
            max_value=120,
            value=None,
            step=1
        )

        sexo_digitado = st.selectbox(
            "Sexo:",
            ["Feminino", "Masculino"],
            index=None,
            placeholder="Selecione"
        )

        salvar_dados = st.form_submit_button(
            "Salvar dados do caso"
        )

#coloca todos os dados do formulario dentro do dados_caso
if salvar_dados:

    if codigo_digitado.strip() == "": #evita a colocar "  "
        st.error("Digite o código do caso.")

    elif idade_digitada is None:
        st.error("Digite a idade.")

    elif sexo_digitado is None:
        st.error("Selecione o sexo.")

    else:
        st.session_state["dados_caso"]["codigo"] = codigo_digitado.strip()
        st.session_state["dados_caso"]["idade"] = idade_digitada
        st.session_state["dados_caso"]["sexo"] = sexo_digitado

        st.success("Dados do caso salvos.")

st.divider()

dados_clinicos_preenchidos = (
    st.session_state["dados_clinicos"]["peso"] is not None
    and st.session_state["dados_clinicos"]["altura"] is not None
    and st.session_state["dados_clinicos"]["cintura"] is not None
    and st.session_state["dados_clinicos"]["quadril"] is not None
    and st.session_state["dados_clinicos"]["diabetes"] is not None
    and st.session_state["dados_clinicos"]["tabagismo"] is not None
)

with st.expander(
    "Dados clínicos compartilhados",
    expanded=not dados_clinicos_preenchidos
):

    with st.form("form_dados_clinicos"):

        peso_digitado = st.number_input(
            "Peso (kg):",
            min_value=1.0,
            max_value=300.0,
            value=None,
            step=0.1
        )

        altura_digitada = st.number_input(
            "Altura (m):",
            min_value=0.5,
            max_value=2.5,
            value=None,
            step=0.01
        )

        cintura_digitada = st.number_input(
            "Circunferência da cintura (cm):",
            min_value=20.0,
            max_value=250.0,
            value=None,
            step=0.1
        )

        quadril_digitado = st.number_input(
            "Circunferência do quadril (cm):",
            min_value=20.0,
            max_value=250.0,
            value=None,
            step=0.1
        )

        diabetes_digitado = st.selectbox(
            "Possui diabetes diagnosticado?",
            ["Sim", "Não", "Não sabe"],
            index=None,
            placeholder="Selecione"
        )

        tabagismo_digitado = st.selectbox(
            "Situação de tabagismo:",
            [
                "Nunca fumou",
                "Ex-fumante há mais de 12 meses",
                "Fumante atual ou nos últimos 12 meses"
            ],
            index=None,
            placeholder="Selecione"
        )

        cigarros_dia_digitado = st.number_input(
            "Média de cigarros por dia:",
            min_value=0,
            max_value=100,
            value=None,
            step=1
        )

        salvar_clinicos = st.form_submit_button(
            "Salvar dados clínicos"
        )


if salvar_clinicos:

    if peso_digitado is None:
        st.error("Digite o peso.")

    elif altura_digitada is None:
        st.error("Digite a altura.")

    elif cintura_digitada is None:
        st.error("Digite a circunferência da cintura.")

    elif quadril_digitado is None:
        st.error("Digite a circunferência do quadril.")

    elif diabetes_digitado is None:
        st.error("Informe a situação de diabetes.")

    elif tabagismo_digitado is None:
        st.error("Informe a situação de tabagismo.")

    elif (
        tabagismo_digitado == "Fumante atual ou nos últimos 12 meses"
        and cigarros_dia_digitado is None
    ):
        st.error("Informe a média de cigarros por dia.")
    
    else:
        imc = round(
            peso_digitado / (altura_digitada ** 2),
            2
        )

        st.session_state["dados_clinicos"]["peso"] = peso_digitado
        st.session_state["dados_clinicos"]["altura"] = altura_digitada
        st.session_state["dados_clinicos"]["cintura"] = cintura_digitada
        st.session_state["dados_clinicos"]["quadril"] = quadril_digitado
        st.session_state["dados_clinicos"]["imc"] = imc
        st.session_state["dados_clinicos"]["diabetes"] = diabetes_digitado
        st.session_state["dados_clinicos"]["tabagismo"] = tabagismo_digitado
        st.session_state["dados_clinicos"]["cigarros_dia"] = cigarros_dia_digitado

        st.success("Dados clínicos salvos.")


st.divider()

modulo = st.selectbox(
    "Escolha um módulo:",
    [
        "Análise radiográfica",
        "Classificação periodontal",
        "FINDRISC",
        "INTERHEART",
        "Relatório"
    ]
)

st.write("Módulo selecionado:", modulo)

# -------------------------
# EXIBIÇÃO DOS MÓDULOS  
# -------------------------

if modulo == "Análise radiográfica":
    mostrar_modulo_radiografico()

elif modulo == "Classificação periodontal":
    mostrar_modulo_periodontal()

elif modulo == "FINDRISC":
    mostrar_findrisc()

elif modulo == "INTERHEART":
    mostrar_interheart()

elif modulo == "Relatório":
    mostrar_relatorio()
